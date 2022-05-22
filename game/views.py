from random import randint, choice
from telnetlib import GA
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .game_logic.moviemon import Moviemon
from .game_logic.my_data import GameData, save_session_data

JOISTIK = {"left", "right", "up", "down"}
STARSEL = {"start", "select"}
BTN_A_B = {"btn_a", "btn_b"}

def index(request):
    game = GameData(load=False)

    return render(None, 'game/index.html', {"disabled": JOISTIK | STARSEL})

def move(request, direction):
    game = GameData()
    match game.state:
        case "worldmap" | "found_moveball":
            row, col  = game.pos
            game.pos[0] += direction == "down"
            game.pos[0] -= direction == "up"
            game.pos[1] -= direction == "left"
            game.pos[1] += direction == "right"
            if not (0 <= game.pos[0] < game.rows and 0 <= game.pos[1] < game.cols):
                return redirect("game:worldmap")
            game.map[row][col] = " "
            cell = game.map[game.pos[0]][game.pos[1]]
            game.map[game.pos[0]][game.pos[1]] = "@"
            if cell == "#":
                game.state = "worldmap"
            if cell == "?":
                if randint(0, 1):
                    # нашли шар
                    game.balls += 3
                    game.state = "found_moveball"
                else:
                    # нашли покемона
                    game.state = "found_movemon"
                pass # TODO
            save_session_data(game.dump())
            return redirect("game:worldmap")


    return HttpResponse("move to the " + direction)

def start(request):
    return HttpResponse("pressed start")

def select(request):
    return HttpResponse("pressed select")

def btn_a(request):
    game = GameData()
    match game.state:
        case "init":
            game = GameData("default")
            return redirect('game:worldmap')
        case "found_movemon":
            game.state = "catch_movemon"
            game.moviemon = choice(list(game.moviemons.keys()))
            save_session_data(game.dump())
            return redirect("game:battle")
        case "catch_movemon" | "miss" | "gotcha":
            if game.balls <= 0 or game.state == "gotcha":
                game.state = "worldmap"
                game.moviemon = None
                save_session_data(game.dump())
                return redirect('game:worldmap')
            game.balls -= 1
            Mov = game.moviemons[game.moviemon]
            print(Mov)

            if game.lvl + randint(1, 10) >= Mov.rating:
                game.state = "gotcha"
                game.cautchs[game.moviemon] = game.moviemons.pop(game.moviemon)
                game.moviemon = None
                game.lvl += Mov.rating / 10
            else:
                game.state = "miss"
            save_session_data(game.dump())
            return redirect("game:battle")
                      
        case _:
            return HttpResponse("todo btn_a")
        
    return HttpResponse("pressed A")

def btn_b(request):
    return HttpResponse("pressed B")

def worldmap(request):
    game = GameData()
    print(len(game.moviemons), "\n", game.cautchs)
    disabled = set() | BTN_A_B
    if game.state == "found_movemon":
        disabled -= {"btn_a"}
        disabled |= JOISTIK | STARSEL 
    return render(None, 'game/worldmap.html', {"game": game.dump(), "disabled": disabled})


def battle(request):
    game = GameData()
    disabled = BTN_A_B
    match game.state:
        case "catch_movemon":
            pass        
        case "gotcha":
            pass
        case "miss":
            pass

    disabled = JOISTIK | STARSEL
    mov = game.moviemons.get(game.moviemon)
    return render(None, 'game/battle.html', {"game": game.dump(), "disabled": disabled, "mov": mov})