import os
import shutil
from django.conf import settings

from game.game_logic.moviemon import Moviemon
from game.views import *

import json
import pickle
import random




def save_session_data(data):
    if not os.path.isdir("saves"):
        os.mkdir("saves")
    try:
        with open("saves/data.bin", "wb") as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(e)
        return None


def load_session_data():
    try:
        with open("saves/data.bin", "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(e)
        return None


def load_slot_info():
    try:
        if os.path.isfile("saves/slots.bin"):
            with open("saves/slots.bin", "rb") as f:
                return pickle.load(f)
        return {}
    except Exception as e:
        print(e)
        return {}


def save_slot(slot):
    data = load_session_data()
    if data is None:
        return False
    slots = load_slot_info()
    try:
        score = f"{len(data['captured_list'])}/{len(data['moviemon'])}"
        if slots.get(f"{slot}", None) is not None:
            if os.path.isfile(slots[f"{slot}"]["file"]):
                os.remove(slots[f"{slot}"]["file"])
        file = f"saves/slot{slot}_{len(data['captured_list'])}_{len(data['moviemon'])}.mmg"
        with open(file, "wb") as f:
            pickle.dump(data, f)
        slots[f"{slot}"] = {
            "score": score,
            "file": file,
        }
        with open("saves/slots.bin", "wb") as f:
            pickle.dump(slots, f)
        return True
    except Exception as e:
        print(e)


def load_slot(slot):
    slots = load_slot_info()
    slot = slots.get(slot, None)
    if slot == None:
        return False
    try:
        shutil.copy(slot["file"], "saves/data.bin")
        return True
    except:
        return False


class GameData:
    def __init__(self, load="file"):
        self.state = "init"
        self.lvl = 1
        self.pos = [0, 0]
        self.rows, self.cols = 0, 0
        self.balls = 0
        self.cautchs = {}
        self.moviemons: dict[str, Moviemon] = {}
        self.map = []
        self.moviemon: str = None

        if load == "file":
            self.load(load_session_data())
        elif load == "default":
            print("Load new game")
            self.load_default_settings()
        print("\n\t game staete ", self.state)
        save_session_data(self.dump())
        
    def dump(self):
        return {
            "state": self.state,
            "pos": self.pos,
            "cautchs": self.cautchs,
            "moviemons": self.moviemons,
            "balls": self.balls,
            "map": self.map,
            "rows": self.rows,
            "cols": self.cols,
            "lvl": self.lvl,
            "moviemon": self.moviemon
        }
    
    def load(self, data):
        self.state = data["state"]
        self.pos = data["pos"]
        self.cautchs = data["cautchs"]
        self.moviemons = data["moviemons"]
        self.balls = data["balls"]
        self.map = data["map"]
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.lvl = data["lvl"]
        self.moviemon = data["moviemon"]
        return self
    

    def load_default_settings(self):
        self.state = "worldmap"
        self.pos = list(settings.PLAYER_INIT_POS)
        self.rows, self.cols = settings.GRID_SIZE
        self.balls = settings.PLAYER_INIT_MOVBALL
        self.cautchs = {}
        self.moviemons = {}

        for id in settings.IMDB_LIST:
            move = Moviemon.get_move_by_imdb_id(id)
            if move is not None:
                self.moviemons[id] = move

        self.map = [["#"] * self.cols for _ in range(self.rows)]
        self.map[self.pos[0]][self.pos[1]] = "@"
        

        for _ in range(len(self.moviemons) * 2):
            while True:
                x, y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
                if self.map[x][y] == "#":
                    self.map[x][y] = "?"
                    break
        
        print(self.map)