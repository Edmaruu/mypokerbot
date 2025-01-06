import pypokerengine
from pypokerengine.api.game import setup_config, start_poker
from fish_player import FishPlayer
from console_player import ConsolePlayer
from random_player import RandomPlayer
from bluffer_player import BlufferPlayer

config = setup_config(max_round=10, initial_stack=100, small_blind_amount=20)
config.register_player(name="f1", algorithm=FishPlayer())
config.register_player(name="f2", algorithm=FishPlayer())
config.register_player(name="f3", algorithm=FishPlayer())
config.register_player(name="BTC", algorithm=BlufferPlayer())
config.register_player(name="f5", algorithm=RandomPlayer())
config.register_player(name="r1", algorithm=RandomPlayer())
config.register_player(name="r2", algorithm=RandomPlayer())
config.register_player(name="r3", algorithm=RandomPlayer())
config.register_player(name="r4", algorithm=RandomPlayer())
config.register_player(name="r5", algorithm=RandomPlayer())
game_result = start_poker(config, verbose=1)