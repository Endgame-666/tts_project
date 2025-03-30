const tg = window.Telegram.WebApp;
let currentAudio = null;
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

function updateFavorites() {
    const favoritesContainer = document.querySelector('.favorites-scroll');
    const favoritesSection = document.getElementById('favorites-section');
    const allFavoriteBtns = document.querySelectorAll('.btn-favorite');

    if(favorites.length > 3) {
        favorites = favorites.slice(-3);
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }

    allFavoriteBtns.forEach(btn => {
        const characterId = btn.closest('.character-card').dataset.characterId;
        btn.classList.toggle('active', favorites.includes(characterId));
    });

    favoritesContainer.innerHTML = '';

    if(favorites.length > 0) {
        favoritesSection.style.display = 'block';
        favorites.forEach(id => {
            const originalCard = document.querySelector(`.character-card[data-character-id="${id}"]`);
            if(originalCard) {
                const clone = createFavoriteCard(originalCard);
                favoritesContainer.appendChild(clone);
            }
        });
    } else {
        favoritesSection.style.display = 'none';
    }
}

function createFavoriteCard(originalCard) {
    const card = document.createElement('div');
    card.className = 'favorite-card';
    card.dataset.characterId = originalCard.dataset.characterId;

    const image = originalCard.querySelector('.character-image').cloneNode();
    image.className = 'favorite-image';

    const name = originalCard.querySelector('.character-name').cloneNode(true);
    name.className = 'favorite-name';

    const selectBtn = document.createElement('button');
    selectBtn.className = 'favorite-select-btn';
    selectBtn.textContent = 'Выбрать';

    selectBtn.addEventListener('click', function() {
        tg.sendData(JSON.stringify({
            characterId: parseInt(card.dataset.characterId)
        }));
        tg.close();
    });

    card.appendChild(image);
    card.appendChild(name);
    card.appendChild(selectBtn);

    return card;
}

document.querySelectorAll('.btn-favorite').forEach(btn => {
    const card = btn.closest('.character-card');
    const id = card.dataset.characterId;

    btn.classList.toggle('active', favorites.includes(id));

    btn.addEventListener('click', (e) => {
        e.stopPropagation();

        const index = favorites.indexOf(id);
        const wasActive = btn.classList.contains('active');
        
        if(!wasActive) {
            if(favorites.length >= 3) {
                const removedId = favorites.shift();
                document.querySelectorAll(`.btn-favorite[data-character-id="${removedId}"]`)
                    .forEach(b => b.classList.remove('active'));
            }
            favorites.push(id);
        } else {
            favorites.splice(index, 1);
        }

        localStorage.setItem('favorites', JSON.stringify(favorites));
        btn.classList.toggle('active');
        updateFavorites();
    });
});

updateFavorites();

document.querySelectorAll('.btn-select').forEach(button => {
    button.addEventListener('click', function() {
        const characterCard = this.closest('.character-card');
        const characterId = characterCard.getAttribute('data-character-id');
        tg.sendData(JSON.stringify({
            characterId: parseInt(characterId)
        }));
        tg.close();
    });
});

document.querySelectorAll('.btn-play').forEach(button => {
    button.addEventListener('click', function() {
        const characterCard = this.closest('.character-card');
        const audio = characterCard.querySelector('audio');

        if(currentAudio && currentAudio !== audio) {
            currentAudio.pause();
            const prevButton = currentAudio.parentElement.querySelector('.btn-play');
            prevButton.classList.remove('playing');
        }

        if(audio.paused) {
            audio.play();
            this.classList.add('playing');
            currentAudio = audio;
        } else {
            audio.pause();
            this.classList.remove('playing');
            currentAudio = null;
        }

        audio.onended = () => {
            this.classList.remove('playing');
            currentAudio = null;
        };
    });
});

