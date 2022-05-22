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
        return data
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
    def __init__(self) -> None:
        self.pos = settings.PLAYER_INIT_POS
        self.captured_list = []
        self.moviemon = {}
        self.movieballCount = settings.PLAYER_INIT_MOVBALL
        self.map = []

    def get_movie(self, moviemon_id):
        return self.moviemon[moviemon_id]

    def get_random_movie(self):
        id_list = [
            m for m in self.moviemon.keys() if not m in self.captured_list
        ]
        return random.choice(id_list)

    def get_strength(self) -> int:
        # return average of best six moviemon ratings
        ratings = sorted(
            [
                self.moviemon[i].rating
                for i in self.load(load_session_data()).captured_list
            ],
            reverse=True,
        )

        if ratings:
            numsend = min(6, len(ratings))
            return int(sum(ratings[:numsend]) / numsend)
        else:
            return 1

    def dump(self):
        return {
            "pos": self.pos,
            "captured_list": self.captured_list,
            "moviemon": self.moviemon,
            "movieballCount": self.movieballCount,
            "map": self.map,
        }

    @staticmethod
    def load(data):
        result = GameData()
        result.pos = data["pos"]
        result.captured_list = data["captured_list"]
        result.moviemon = data["moviemon"]
        result.movieballCount = data["movieballCount"]
        result.map = data["map"]
        return result

    @staticmethod
    def load_default_settings():
        result = GameData()

        for id in settings.IMDB_LIST:
            move = Moviemon.get_move_by_imdb_id(id)
            if move is not None:
                result.moviemon[id] = move

        x, y = settings.GRID_SIZE
        total = min(
            int(x * y * random.randint(7, 11) / 80),
            len(result.moviemon.keys()),
        )
        result.moviemon = get_suitable(
            total,
            result.moviemon,
            max(3, int(total / 3)),
            4,
            max(3, int(total / 3)),
            7,
        )
        result.map = init_map(
            *settings.GRID_SIZE,
            int(random.uniform(0.5, 1) * len(result.moviemon)),
        )

        return result
