'''
interface requirements:
Classes:
    Board:
        legal_moves()
        is_checkmate()
        is_game_over()
        is_en_passant(<Move>)
        push(<Move>)
        pop()
        piece_at(index: int)
    Move
    Piece

Functions:
    move_value(<Board>, <Move>, end_game: bool)

other stuff:
    idk, made by me (https://github.com/ethandhunt)
    made for CASIO fx-9860 giii μpython
'''

debug = True

def drint(*args):
    if debug:
        print(*args)
        
drint(__file__, 'tl...') # top level initialisation

# thanks https://stackoverflow.com/questions/16808384/what-is-the-implementation-detail-for-enumerate
def enumerate(iterable, start=0):
    count = start
    for elem in iterable:
        yield count, elem
        count += 1

    
WHITE = True # a1:h2, K
BLACK = False # a8:h7, k

PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING = range(1, 7)
PIECE_TO_CHAR = dict(zip(range(1, 7), 'PRNBQK'))
CHAR_TO_PIECE = dict(zip('PRNBQK', range(1, 7)))

piece_value = {
    PAWN: 100,
    ROOK: 500,
    KNIGHT: 320,
    BISHOP: 330,
    QUEEN: 900,
    KING: 20000
}

pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = pawnEvalWhite
pawnEvalBlack.reverse()

knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = bishopEvalWhite
bishopEvalBlack.reverse()

rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = rookEvalWhite
rookEvalBlack.reverse()

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = kingEvalWhite
kingEvalBlack.reverse()

kingEvalEndGameWhite = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
kingEvalEndGameBlack = kingEvalEndGameWhite
kingEvalEndGameBlack.reverse()

Square = int
SQUARES = [
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8,
] = list(range(8*8))

SQUARE_NAMES = [x+y for y in '12345678' for x in 'ABCDEFGH'] # ['A1', 'A2', 'A3', ..., 'H6', 'H7', 'H8']

RANKS = [
    RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8
] = [list(range(8*i, 8*i+8)) for i in range(8)]

# bitmask
BB_SQUARES = [
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7,
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8,
] = [1 << sq for sq in SQUARES] # [0b1, 0b10, 0b100, ...]

BB_ALL = 0xffffffffffffffff

BB_RANKS = [
    BB_RANK_1, BB_RANK_2, BB_RANK_3, BB_RANK_4, BB_RANK_5, BB_RANK_6, BB_RANK_7, BB_RANK_8
] = [0xff for _ in range(8)] # [0xff, 0xff00, 0xff0000, ...]

BB_FILES = [
    BB_FILE_A, BB_FILE_B, BB_FILE_C, BB_FILE_D, BB_FILE_E, BB_FILE_F, BB_FILE_G, BB_FILE_H
] = [0x0101010101010101 << i for i in range(8)]


STARTING_FEN = 'RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr w KQkq - 0 1'
class Board:
    def __init__(self, fen_string=STARTING_FEN):
        self.pieces = []
        self.move_stack = []

        fen_board, fen_turn, fen_castle, fen_en_passant, fen_half_move, fen_full_move = fen_string.split(' ')
        self.turn = fen_turn == 'w'
        self.castling_rights = (BB_A1 * ('k' in fen_castle) | BB_H1 * ('q' in fen_castle) | BB_A8 * ('K' in fen_castle) | BB_H8 * ('Q' in fen_castle))
        
        self.occupied_mask = {WHITE:BB_RANK_1, BLACK:BB_RANK_8}
        
        # populate 
        sq = A1
        for y, row in enumerate(fen_board.split('/')):
            c = 0
            for x, p in enumerate(row):
                if p.isdigit():
                    c += int(p) - 1 # 1 is ignored
                    continue

                self.pieces.append(Piece(p, x+c+y*8))

        def set_endgame(self):
            # Set if both sides have no queens, or sides w/ queens only have max 1 extra pawn

            if 'Q' in self.pieces:
                if len(self.pieces_of(WHITE)) > 2:
                    return False
                # must now be w.pieces == ['Q', ?]
                
                if not 'P' in self.pieces:
                    return False
                # w.pieces == ['Q', 'P']
            # w.pieces == ['Q', 'P'] or 'Q' not in w.pieces
            
            if 'q' in self.pieces:
                if len(self.pieces_of(BLACK)) > 2:
                    return False
                # must now be b.pieces == ['q', ?]

                if not 'p' in self.pieces:
                    return False
                # b.pieces == ['q', 'p']
            # b.pieces == ['q', 'p'] or 'q' not in b.pieces
            
            return True # (w.pieces == ['Q', 'P'] or 'Q' not in w.pieces) and (b.pieces == ['q', 'p'] or 'q' not in b.pieces)

        self.endgame = set_endgame(self)
            

    def piece_at(self, x, y):
        for p in self.pieces:
            if p.square == x + y * 8:
                return p
        
        return None

    def pieces_of(self, side):
        ret = []
        for p in self.pieces:
            if p.side == side:
                ret.append(p)
        
        return ret

    def show_moves(self):
        for p in b.pieces:
            print(p, end=' -> ')
            available = []
            pmove_mask = p.passive_move_mask([0, 0])
            for x in range(64):
                if pmove_mask & 2**x:
                    available.append(SQUARE_NAMES[x])

            print(', '.join(available))

class Move:
    def __init__(self, from_square: Square, to_square: Square, promotion=None):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion = promotion
    
    def uci(self):
        promotion = PIECE_TO_CHAR[self.promotion] if self.promotion else ''
        return SQUARE_NAMES[self.from_square] + SQUARE_NAMES[self.to_square] + promotion
        # examples:
        # A1B1 (any piece that was on A1 moved to B1)
        # D7D8Q (piece at D7 goes to D8 and turns into a queeen)
    
    def from_uci(uci: str):
        try:
            from_square = SQUARE_NAMES.index(uci[0:2])
            to_square = SQUARE_NAMES.index(uci[2:4])
            promotion = CHAR_TO_PIECE[uci[4]] if len(uci) == 5 else None
            
            return Move(from_square, to_square, promotion)
            
        except ValueError:
            raise ValueError('Invalid UCI string: ' + repr(uci))
    
    def __repr__(self):
        return self.uci()

class Piece:
    def __init__(self, piece_as_char, square):
        self.piece_type = CHAR_TO_PIECE[piece_as_char.upper()]
        self.side = WHITE if piece_as_char.isupper() else BLACK
        self.square = square
        self.bb_square = 2**square
    
    def __eq__(self, piece_type):
        return self.piece_type == piece_type

    def __repr__(self):
        ret = PIECE_TO_CHAR[self.piece_type]
        ret = ret.upper() if self.side == WHITE else ret.lower()
        return ret + '@' + SQUARE_NAMES[self.square]

    def passive_move_mask(self, occupied_mask):
        '''
        Generates move mask
        Ignores discovered check
        Continuous moves are constrained by the presence of pieces in the way
        '''
        move_mask = 0
        MY = 8 # Move Y axis
        MX = 1 # Move X axis
        
        can_exit = False
        # Noncontinuous pass
        if self.piece_type == PAWN:
            can_exit = True
            
            # on bitboard, [x+8] is y+1
            starting_rank = RANK_2 if self.side == WHITE else RANK_7
            
            if self.square in starting_rank:
                move_mask |= (self.bb_square << (2*MY)) if self.side == WHITE else (self.bb_square >> (2*MY))
            
            move_mask |= (self.bb_square << MY) if self.side == WHITE else (self.bb_square >> MY)
        
        elif self.piece_type == KNIGHT:
            can_exit = True

            # cfs = [MX*x + MY*y for x in [-1, 1] for y in [-2, 2] if (self.square + x)//8 == self.square//8]+ [MX*x + MY*y for x in [-2, 2] for y in [-1, 1] if (self.square + x)//8 == self.square//8]# Coefficients [(-1, -2), (1, -2), ..., (-2, -1), (2, -1), ...]
            cfs = []
            condition = lambda x, y: (self.square + x)//8 == self.square//8 and 0 <= MX*x + MY*y + self.square < 64
            for i in [-1, 1]:
                for j in [-2, 2]:
                    if condition(i, j):
                        cfs.append(MX*i + MY*j)
                    
                    if condition(j, i):
                        cfs.append(MX*j + MY*i)
                    
            for c in cfs:
                if c >= 0:
                    move_mask |= (self.bb_square << c)

                else:
                    move_mask |= (self.bb_square >> -c)
            
        elif self.piece_type == KING:
            can_exit = True
            
            # wrap around, on board, king can't move by not moving
            # condition = lambda x, y: ((self.square + x)//8 == self.square//8) and (0 <= MX*x + MY*y + self.square < 64) and (x*y != 0)
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    #if condition(x, y):
                    
                    # wrap around
                    if (self.square + x)//8 != self.square//8:
                        continue
                    
                    if not 0 <= (self.square + MX*x + MY*y) < 64:
                        continue
                    
                    if x == y == 0:
                        continue

                    if x*MX + y*MY >= 0:
                        move_mask |= self.bb_square << (x*MX + y*MY)

                    else:                        
                        move_mask |= self.bb_square >> -(x*MX + y*MY)
        
        if can_exit:
            move_mask &= BB_ALL
            move_mask &= ~occupied_mask[self.side]
            move_mask &= ~occupied_mask[not self.side]
            return move_mask
        
        # Continuous move pass
            
        if self.piece_type == ROOK:
            for dx in [-1, 1]:
                pass
            
            for dy in [-1, 1]:
                pass
        
        elif self.piece_type == BISHOP:
            pass
            
        elif self.piece_type == QUEEN:
            pass
        
        return 0
            
    def attack_mask(self, occupied_mask, en_passant_mask):
        pass
        
    
    
drint(__file__, 'tl done')

# b = Board('7P/8/8/8/8/8/8/8 w KQkq - 0 1')
b = Board()
b.show_moves()