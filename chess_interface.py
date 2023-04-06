import engine
import random

in_fen = input('fen: ')
if in_fen == '':
    in_fen = engine.STARTING_FEN

b = engine.Board(in_fen)
for i in range(15):
    move = random.choice(b.moves())
    b.push(move)