window.onload = function() {

    const cardDisplay = document.getElementById('card-display');

    const cards = ['Beso De A 3.jpg', 'Twerkeá.jpg', 'Frotate Con Alguien.jpg', 'Telefono Descompuesto De Besos.jpg', 'Mostrá Tu Elasticidad.jpg', 'Ronda De Nalgadas.jpg', 'Recibí Cosquillas.jpg', 'Un Beso, Una Boca.jpg', 'Nalgueadas Y Cosquillas (30S).jpg', 'Volvé Sexual Algo.jpg', 'Dale De Tomar A Alguien.jpg', 'Elegí A Quién Le Hacés Un Lapdance.jpg', 'Finjan Un Orgasmo.jpg', 'Masaje A Otra Persona Donde Quiera.jpg', 'Shot De Adrenalina.jpg', 'Chupá Dedos.jpg', 'Sacate Una Prenda.jpg', 'Ahorcadura.jpg', 'Beso En Ronda.jpg', 'Algo Sucio Al Oido.jpg', 'Cuántos Dedos Entran En La Boca.jpg', 'Mostrá Todo Tu Outfit.jpg', 'Acercamiento De Labios (60S).jpg', 'Adivina Quién Te Besó.jpg', 'Mirarse Fijo (30S).jpg', 'Hacé De Mesita Por Un Turno.jpg', 'Recibi Nalgadas.jpg', 'Tenés Dos Turnos.jpg', 'Elegí 2 Que Se Besen.jpg', 'Bailar Pegadito.jpg', 'Intercambiar Una Prenda.jpg', 'Object, Pet O Age Play (30S).jpg', 'Contar Una Fantasía.jpg', 'Que Te Hagan Upa Entre Todes.jpg', 'Mandá Una Nude.jpg', 'Describir El Olor De Otra Persona.jpg', 'Mordiditas.jpg', 'Recibí Mimos.jpg', 'Worship De Tetas.jpg'];
    const usedCards = [];
    const neutralCard = 'images/neutral-card.jpg'; // Path to your neutral card image

    function getRandomCard() {
        if (cards.length === 0) {
            alert("No quedan mas cartas. Arrancando nueva partida.");
            startGame();
            return;
        }
        const index = Math.floor(Math.random() * cards.length);
        const card = cards.splice(index, 1)[0];
        usedCards.push(card);
        return card;
    }

    function updateCardDisplay(cardPath) {
        cardDisplay.src = `deck_light/${cardPath}`;
    }

    cardDisplay.addEventListener('click', function() {
        const card = getRandomCard();
        if (card) {
            updateCardDisplay(card);
        }
    });

    function startGame() {
        cards.push(...usedCards);
        usedCards.length = 0;
        cardDisplay.src = neutralCard;
    }

    // Initialize game state
    startGame();
}