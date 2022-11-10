### IMPORTS
import json
from typing import List
from thumb_scraper import get_thumb

### CLASS
class Joke:
    joke = ''
    guest = ''
    episode = ''
    thumbnail = ''

    def __init__(self, joke:str, guest:str, episode:str, thumbnail:str) -> None:
        self.joke = self._parse_joke(joke)
        self.guest = guest
        self.episode = episode
        self.thumbnail = thumbnail
    
    # def __repr__(self) -> str:
    #     print (self.joke)
    
    def _parse_joke(self, joke:str):
        return joke.replace('<i>', '*').replace('</i>', '*').replace('<p>', '\n').replace('</p>', '')


### Getting the jokes
def load_jokes() -> dict:
    '''
    Loads jokes JSON file from disk
    '''
    with open('jokes.json', 'r') as f:
        jokes_json = json.load(f)

        return jokes_json

def parse_jokes(jokes_json: List[dict]) -> List[Joke]:
    '''
    Converts joke dictionary items into Joke class objects
    '''
    jokes = []
    thumbs = {}

    for j in jokes_json:
        joke, episode, guest, id = j.values()

        if guest not in thumbs:
            thumbs[guest] = get_thumb(guest)

        jokes.append(Joke(joke, guest, episode, thumbs[guest]))
    
    return jokes

def get_jokes() -> List[Joke]:
    '''
    Returns all jokes on disk as Joke objects.
    '''
    jokes_json = load_jokes()
    jokes = parse_jokes(jokes_json)
    return jokes
