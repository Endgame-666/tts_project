const tg = window.Telegram.WebApp;
let currentAudio = null;

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