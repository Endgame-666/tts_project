from pymongo import MongoClient
import certifi
from typing import Optional, Dict, Any, List
import datetime
import hashlib


class MongoDBManager:
    def __init__(self,
                 mongo_url: str,
                 db_name: str = "voice_bot",
                 collection_name: str = "voice_messages"):
        self.client = MongoClient(mongo_url, tlsCAFile=certifi.where())
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        try:
            self.client.admin.command('ismaster')
            print("MongoDB connection successful")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            raise

    def generate_message_id(self, audio_path: str) -> str:
        return hashlib.md5(audio_path.encode()).hexdigest()

    def save_voice_message(self,
                           user_id: int,
                           character_id: int,
                           audio_path: str,
                           message_text: str) -> str:
        message_id = self.generate_message_id(audio_path)

        voice_doc = {
            "_id": message_id,
            "user_id": user_id,
            "character_id": character_id,
            "audio_path": audio_path,
            "message_text": message_text,
            "timestamp": datetime.datetime.now(),
            "favorite_by": []
        }

        self.collection.insert_one(voice_doc)
        return message_id

    def get_voice_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({"_id": message_id})

    def get_user_messages(self,
                          user_id: int,
                          skip: int = 0,
                          limit: int = 10) -> tuple[List[Dict[str, Any]], bool]:
        total = self.collection.count_documents({"user_id": user_id})

        cursor = self.collection.find({"user_id": user_id}) \
            .sort("timestamp", -1) \
            .skip(skip) \
            .limit(limit)

        messages = list(cursor)
        has_more = total > skip + limit

        return messages, has_more

    def toggle_favorite(self, message_id: str, user_id: int) -> bool:
        message = self.collection.find_one({"_id": message_id})
        if not message:
            return False

        if user_id in message['favorite_by']:
            self.collection.update_one(
                {"_id": message_id},
                {"$pull": {"favorite_by": user_id}}
            )
            return False
        else:
            self.collection.update_one(
                {"_id": message_id},
                {"$push": {"favorite_by": user_id}}
            )
            return True

    def is_favorite(self, message_id: str, user_id: int) -> bool:
        message = self.collection.find_one({"_id": message_id})
        return message and user_id in message.get('favorite_by', [])

    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        return list(self.collection.find({"favorite_by": user_id}))

    def get_character_messages(self,
                               user_id: int,
                               character_id: int) -> List[Dict[str, Any]]:
        return list(self.collection.find({
            "user_id": user_id,
            "character_id": character_id
        }).sort("timestamp", -1))

    def close(self):
        self.client.close()