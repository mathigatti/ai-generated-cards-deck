# AI Generated Cards Deck

These are scripts used to create a deck of cards [and website](https://consignashot.netlify.app/).


![Card example](https://raw.githubusercontent.com/mathigatti/ai-generated-cards-deck/master/website/deck_light/Besar%20En%20Un%20Lugar%20Nuevo.jpg)

## Technical details

- From a list of challenges/card titles I used `prompt-chatgpt.txt` to generate cards.csv
- `cards.csv`
    It the card titles + the visual description necessary to generate the illustrations + an optional text description in case the card requires extra explanation
- `generate-illustration.py`
    It generates the cards for each visual description in cards.py and saves them at `images` folder
- `generate-final-card.py`
    It goes through the `images` folder and puts that together with the optional descriptions in `cards.csv`, the card frames at `frames` and some prefered font in the `fonts` folder. 
- `resize.py`
    This converts all images to a smaller size and jpg format so they are lighter and the website is fast.
