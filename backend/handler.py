from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton  # type: ignore
import re
from aiogram.filters.callback_data import CallbackData

class MessageCallback(CallbackData, prefix="recipe"):
    action: str
    id: str

class Handler:
    def __init__(self):
        self.user_data = {}  # Local dictionary to simulate user data storage
        self.recipes = {}  # Local dictionary to store recipes
        self.favorites = {}  # Local dictionary for favorite recipes

    async def get_recipe_history(self, user_id, offset: int = 0, limit: int = 3):
        """Get paginated recipe history for user from local storage"""
        user_recipes = self.recipes.get(user_id, [])
        has_more = len(user_recipes) > offset + limit
        return user_recipes[offset:offset + limit], has_more

    async def new_recipe_handler(self, user_id, recipe_data):
        product_links = {}
        total_cost = 0

        if 'links' in recipe_data:
            for category, products in recipe_data['links'].items():
                if category == "total_cost" or category == "message":
                    continue

                if not isinstance(products, list):
                    continue

                for product in products:
                    if not isinstance(product, dict):
                        continue

                    if 'message' in product:
                        product_links[category] = product['message']
                        continue

                    if product.get('name') and product.get('link'):
                        product_links[product['name']] = {
                            'link': product['link'],
                            'price': product.get('price', 'Цена не указана')
                        }
                        if isinstance(product.get('price'), (int, float)):
                            total_cost += float(product['price'])

            product_links['total_cost'] = total_cost

            if "message" in recipe_data['links']:
                product_links['message'] = recipe_data['links']['message']

        recipe_id = len(self.recipes.get(user_id, [])) + 1
        recipe_entry = {
            "id": recipe_id,
            "request": recipe_data['request'],
            "text": recipe_data['text'],
            "ingredients": recipe_data['ingredients'],
            "product_links": product_links
        }
        self.recipes.setdefault(user_id, []).append(recipe_entry)
        return recipe_id

    async def format_recipe_with_links(self, recipe: dict) -> str:
        base_text = f"{recipe['text']}"

        if recipe.get('product_links'):
            base_text += "\n\nСсылки на продукты:\n"

            portions_match = re.search(r'на (\d+) порци[юие]', recipe.get('request', ''))
            portions = portions_match.group(1) if portions_match else "1"

            for product_name, info in recipe['product_links'].items():
                if product_name in ['total_cost', 'message']:
                    continue

                base_text += f"\n{product_name.replace('+', ' ')}\n"
                if isinstance(info, str):
                    base_text += f"{info}\n"
                else:
                    base_text += f"Цена: {info.get('price', 'Цена не указана')}\n"
                    base_text += f"Ссылка: {info.get('link', 'Ссылка отсутствует')}\n"

            if 'total_cost' in recipe['product_links']:
                portions_in_russian = "порций"
                if 2 <= int(portions) <= 4:
                    portions_in_russian = "порции"
                if int(portions) == 1:
                    portions_in_russian = "порцию"

                total_cost = float(recipe['product_links']['total_cost']) * int(portions)
                base_text += f"\n💰 Приблизительная итоговая стоимость на {portions} {portions_in_russian}: {total_cost:.2f} RUB"

            if 'message' in recipe['product_links']:
                base_text += f"\n\n⚠️ {recipe['product_links']['message']}"

        return base_text

    async def toggle_favorite_recipe(self, user_id: int, recipe_id: str) -> bool:
        self.favorites.setdefault(user_id, set())
        if recipe_id in self.favorites[user_id]:
            self.favorites[user_id].remove(recipe_id)
            return False
        else:
            self.favorites[user_id].add(recipe_id)
            return True

    async def is_recipe_favorite(self, user_id: int, recipe_id: str) -> bool:
        return recipe_id in self.favorites.get(user_id, set())

    async def get_favorite_recipes(self, user_id: int) -> list:
        favorite_ids = self.favorites.get(user_id, set())
        return [recipe for recipe in self.recipes.get(user_id, []) if str(recipe['id']) in favorite_ids]

    async def get_recipe_by_id(self, recipe_id: str):
        for user_recipes in self.recipes.values():
            for recipe in user_recipes:
                if str(recipe['id']) == recipe_id:
                    return recipe
        return None

    async def add_new_user(self, user_id, user_name: str = "", language: str = "en"):
        self.user_data[user_id] = {"name": user_name, "language": language}

    async def get_user_preferences(self, user_id):
        return self.user_data.get(user_id, {})

    async def update_user_allergies(self, user_id: int, allergies: list):
        self.user_data.setdefault(user_id, {})['allergies'] = allergies

    async def update_price_limit(self, user_id: int, price_limit: int):
        self.user_data.setdefault(user_id, {})['max_price'] = price_limit

    async def update_disliked_products(self, user_id: int, disliked_products: list):
        self.user_data.setdefault(user_id, {})['unliked_products'] = disliked_products

    async def get_formatted_preferences(self, user_id: int) -> str:
        user_data = self.user_data.get(user_id, {})
        if not user_data:
            return "Предпочтения не найдены"

        allergies = user_data.get('allergies', [])
        allergies_text = "Аллергия:\n" + "\n".join(allergies) if allergies else "Аллергия:\nНе указано"

        unliked = user_data.get('unliked_products', [])
        unliked_text = "\n\nНелюбимые продукты:\n" + "\n".join(unliked) if unliked else "\n\nНелюбимые продукты:\nНе указано"

        price_text = f"\n\nОграничение цены:\n{user_data.get('max_price', 'Не указано')} руб."

        return allergies_text + unliked_text + price_text

    def create_recipe_keyboard(self, recipe_id: str, user_id: int, show_full=True) -> InlineKeyboardMarkup:
        is_favorite = self.is_recipe_favorite(user_id, recipe_id)
        favorite_text = "❌ Убрать из избранного" if is_favorite else "⭐️ Добавить в избранное"

        buttons = []
        if show_full:
            buttons.append([
                InlineKeyboardButton(
                    text="Получить полный рецепт",
                    callback_data=MessageCallback(action="get_full", id=recipe_id).pack()
                )
            ])

        buttons.append([
            InlineKeyboardButton(
                text=favorite_text,
                callback_data=MessageCallback(action="toggle_favorite", id=recipe_id).pack()
            )
        ])

        return InlineKeyboardMarkup(inline_keyboard=buttons)
