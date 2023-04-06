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
] = [0xff << 8*i for i in range(8)] # [0xff, 0xff00, 0xff0000, ...]

BB_FILES = [
    BB_FILE_A, BB_FILE_B, BB_FILE_C, BB_FILE_D, BB_FILE_E, BB_FILE_F, BB_FILE_G, BB_FILE_H
] = [0x0101010101010101 << i for i in range(8)]


STARTING_FEN = 'RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr w KQkq - 0 1'
class Board:
    def __init__(self, fen_string=STARTING_FEN):
        self.pieces = []
        self.move_stack = []
        self.inactive_pieces = [] # subset of self.pieces

        fen_board, fen_turn, fen_castle, fen_en_passant, fen_half_move, fen_full_move = fen_string.split(' ')
        self.turn = WHITE if fen_turn == 'w' else BLACK
        # {WHITE: [KING, QUEEN], BLACK: [KING, QUEEN]}
        self.castling_rights = {WHITE:[CHAR_TO_PIECE[x.upper()] for x in fen_castle if x.islower()], BLACK:[CHAR_TO_PIECE[x.upper()] for x in fen_castle if x.isupper()]}
        self.prev_castling_rights = []
        self.en_passant_square = SQUARE_NAMES.index(fen_en_passant) if fen_en_passant != '-' else None
        
        self.occupied_mask = {WHITE:0, BLACK:0}
        
        # populate 
        sq = A1
        for y, row in enumerate(fen_board.split('/')):
            c = 0
            for x, p in enumerate(row):
                if p.isdigit():
                    c += int(p) - 1 # 1 is ignored
                    continue

                pi = Piece(p, x+c+y*8)
                self.pieces.append(pi)
                self.occupied_mask[pi.side] |= pi.bb_square

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
            

    def piece_at(self, s):
        '''
        returns the active piece at x, y
        '''
        for p in self.pieces:
            if p.square == s and p.active:
                return p
        
        return None

    def pieces_of(self, side):
        '''
        returns active pieces
        '''
        ret = []
        for p in self.pieces:
            if p.side == side:
                ret.append(p)
        
        return ret

    def show_moves(self):
        for p in self.pieces:
            print(p, end=' -> ')
            moves = p.moves(self.occupied_mask, self.en_passant_square, self.castling_rights)
            print(', '.join(map(Move.uci, moves)))
    
    def moves(self):
        moves = []
        for p in self.pieces:
            moves.append(p.moves(self.occupied_mask, self.en_passant_square, self.castling_rights))
        return moves
    
    def push(self, move):
        drint('Board.push(' + str(move) + ')')
        self.move_stack.append(move)
        side = self.piece_at(move.from_square).side

        if move.attacking:
            self.inactive_pieces.append(self.piece_at(move.captured))
            self.piece_at(move.captured).active = False
        
        self.piece_at(move.from_square).square = move.to_square
        self.occupied_mask[side] &= ~BB_SQUARES[move.from_square]
        self.occupied_mask[side] |= BB_SQUARES[move.to_square]
        
        if move.castling:
            self.piece_at(move.castle_from).square = move.castle_to
            self.prev_castling_rights.append(self.castling_rights)
            self.castling_rights[side] = []
        
        self.turn = not self.turn
        
    
    def pop(self):
        move = self.move_stack.pop()
        
        if move.attacking:
            self.piece_at(move.captured)
        
        if move.castling or move.castle_from in [A1, A8, H1, H8]:
            self.castling_rights = self.prev_castling_rights.pop()
        
        self.turn = not self.turn

class Move:
    def __init__(self, from_square: Square, to_square: Square, promotion=None, attacking=False, castling=False, castle_from: Square=None, castle_to: Square=None, captured=None):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion = promotion
        self.attacking = attacking
        self.castling = castling
        self.castle_from = castle_from
        self.castle_to = castle_to
        self.captured = captured
    
    def uci(self):
        promotion = PIECE_TO_CHAR[self.promotion] if self.promotion else ''
        if self.castling:
            return '-'.join((['O']*abs(self.castle_from - self.castle_to)))
        return SQUARE_NAMES[self.from_square].lower() + 'x' * self.attacking + SQUARE_NAMES[self.to_square].lower() + promotion
        # examples:
        # A1B1 (any piece that was on A1 moved to B1)
        # D7D8Q (piece at D7 goes to D8 and turns into a queeen)
    
    def from_uci(uci: str, context: Board=None):
        try:
            if uci == 'O-O-O':
                if context.turn == WHITE:
                    return Move(E1, C1, castle_from=A1, castle_to=D1, castling=True)

                if context.turn == BLACK:
                    return Move(E8, C8, castle_from=A8, castle_to=D8, castling=True)
            
            elif uci == 'O-O':
                if context.turn == WHITE:
                    return Move(E1, G1, castle_from=H1, castle_to=F1, castling=True)

                if context.turn == BLACK:
                    return Move(E8, G8, castle_from=H8, castle_to=F8, castling=True)

            from_square = SQUARE_NAMES.index(uci[0:2])
            to_square = SQUARE_NAMES.index(uci[2:4])
            promotion = CHAR_TO_PIECE[uci[4]] if len(uci) == 5 else None
            
            return Move(from_square, to_square, promotion)
            
        except ValueError:
            raise ValueError('Invalid UCI string: ' + repr(uci))
    
    def __repr__(self):
        return self.uci()

class Piece:
    def __init__(self, piece_as_char, square, active=True):
        self.piece_type = CHAR_TO_PIECE[piece_as_char.upper()]
        self.side = WHITE if piece_as_char.isupper() else BLACK
        self.square = square
        self.bb_square = 2**square
        self.active = active
    
    def __eq__(self, piece_type):
        return self.piece_type == piece_type

    def __repr__(self):
        ret = PIECE_TO_CHAR[self.piece_type]
        ret = ret.upper() if self.side == WHITE else ret.lower()
        return ret + '@' + SQUARE_NAMES[self.square]

    def moves(self, occupied_mask, en_passant_square, castling_rights):
        '''
        Generates move mask
        Ignores discovered check
        Continuous moves are constrained by the presence of pieces in the way
        '''
        moves = []
        MY = 8 # Move Y axis
        MX = 1 # Move X axis
        
        can_exit = False
        # Noncontinuous pass
        if self.piece_type == PAWN:
            can_exit = True
            
            same_rank = lambda a, b: a//8 == b//8
            on_occupied = lambda x: (occupied_mask[self.side]|occupied_mask[not self.side]) & 2**x
            # on bitboard, [x+8] is y+1
            starting_rank = RANK_2 if self.side == WHITE else RANK_7
            
            tup = (self.square + 2*MY) if self.side == WHITE else (self.square - 2*MY)
            if self.square in starting_rank and not on_occupied(tup):
                moves.append(Move(self.square, tup))
            
            up = (self.square + MY) if self.side == WHITE else (self.square - MY)
            if 0 <= up < 64 and not on_occupied(up):
                moves.append(Move(self.square, up))
            
            left = up - MX
            right = up + MX

            if same_rank(up, left) and occupied_mask[not self.side] & 2**left:
                moves.append(Move(self.square, left, attacking=True, captured=left))
            
            if same_rank(up, right) and occupied_mask[not self.side] & 2**right:
                moves.append(Move(self.square, right, attacking=True, captured=left))
        
        elif self.piece_type == KNIGHT:
            can_exit = True

            # no wrap around, on board, not attacking own piece
            condition = lambda x, y: (self.square + x)//8 == self.square//8 and 0 <= MX*x + MY*y + self.square < 64 and not 2**(self.square+x*MX+y*MY) & occupied_mask[self.side]
            attacking = lambda x, y: bool(2**(self.square + x*MX + y*MY) & occupied_mask[not self.side])
            for i in [-1, 1]:
                for j in [-2, 2]:
                    if condition(i, j):
                        moves.append(Move(self.square, self.square + MX*i + MY*j, attacking=attacking(i, j), captured=self.square + MX*i + MY*j))
                    
                    if condition(j, i):
                        moves.append(Move(self.square, self.square + MX*j + MY*i, attacking=attacking(j, i), captured=self.square + MX*j + MY*i))
                    
            
        elif self.piece_type == KING:
            can_exit = True
            
            attacking = lambda x, y: 2**(self.square + x*MX + y*MY) & occupied_mask[not self.side]
            # wrap around, on board, king can't move by not moving
            # condition = lambda x, y: ((self.square + x)//8 == self.square//8) and (0 <= MX*x + MY*y + self.square < 64) and (x*y != 0)
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    #if condition(x, y):
                    
                    # prevent wrap around
                    if (self.square + x)//8 != self.square//8:
                        continue
                    
                    # chess isn't open world yet
                    if not 0 <= (self.square + MX*x + MY*y) < 64:
                        continue
                    
                    # king can't move by not moving
                    if x == y == 0:
                        continue
                    
                    # king can't take own piece
                    if occupied_mask[self.side] & 2**(self.square + x*MX + y*MY):
                        continue


                    # attacking if square is opponent piece
                    moves.append(Move(self.square, self.square + x*MX + y*MY, attacking=attacking(x, y), captured=self.square + x*MX + y*MY))
            
            # castling
            # moving through check must be caught externally
            # assumes that the rook and king are in the correct spots and castling rights are accurate
            rank = BB_RANK_1 if self.side == WHITE else BB_RANK_8
            if KING in castling_rights[self.side]:
                # check if any piece is preventing the castle by existing in between the castle and the king
                if not (BB_FILE_F | BB_FILE_G) & rank & (occupied_mask[self.side] | occupied_mask[not self.side]):
                    moves.append(Move(self.square, self.square + 2, castling=True, castle_from=self.square + 3, castle_to=self.square + 1))
            
            if QUEEN in castling_rights[self.side]:
                if not (BB_FILE_C | BB_FILE_D) & rank & (occupied_mask[self.side] | occupied_mask[not self.side]):
                    moves.append(Move(self.square, self.square - 2, castling=True, castle_from=self.square - 4, castle_to=self.square - 1))
            
        
        # Continuous move pass
        elif self.piece_type == ROOK:
            can_exit = True
            
            move_squares = []
            on_same_rank = lambda dx: (self.square + dx*MX)//8 == self.square//8
            on_board = lambda dx, dy: 0 <= self.square + dx*MX + dy*MY < 64
            on_occupied = lambda dx, dy: (2**(self.square + dx*MX + dy*MY) & occupied_mask[self.side]) or (2**(self.square + dx*MX + dy*MY) & occupied_mask[not self.side])

            for ix in [-1, 1]:
                dx = ix
                while on_same_rank(dx) and on_board(dx, 0) and not on_occupied(dx, 0):
                    moves.append(Move(self.square, self.square + dx*MX))
                    dx += ix
                    
                # attacking
                if on_board(dx, 0) and not occupied_mask[self.side] & 2**(self.square + dx*MX):
                    moves.append(Move(self.square, self.square + dx*MX, attacking=True))
            
            for iy in [-1, 1]:
                dy = iy
                while on_board(0, dy) and not on_occupied(0, dy):
                    moves.append(Move(self.square, self.square + dy*MY))
                    dy += iy
                
                # attacking
                if on_board(0, dy) and not occupied_mask[self.side] & 2**(self.square + dy*MY):
                    moves.append(Move(self.square, self.square + dy*MY, attacking=True))
        
        elif self.piece_type == BISHOP:
            can_exit = True

            on_board = lambda dx, dy: 0 <= self.square + dx*MX + dy*MY < 64
            on_occupied = lambda dx, dy: (2**(self.square + dx*MX + dy*MY) & occupied_mask[self.side]) or (2**(self.square + dx*MX + dy*MY) & occupied_mask[not self.side])
            no_wrap_around = lambda dx: (self.square + dx*MX)//8 == self.square//8
            
            for ix in [-1, 1]:
                for iy in [-1, 1]:
                    dx = ix
                    dy = iy
                    while no_wrap_around(dx) and on_board(dx, dy) and not on_occupied(dx, dy):
                        moves.append(Move(self.square, self.square + dx*MX + dy*MY))
                        dx += ix
                        dy += iy

                    # attacking
                    if no_wrap_around(dx) and on_board(dx, dy) and not occupied_mask[self.side] & 2**(self.square + dx*MX + dy*MY):
                        moves.append(Move(self.square, self.square + dy*MY, attacking=True))
            
        elif self.piece_type == QUEEN:
            can_exit = True
            
            on_board = lambda dx, dy: 0 <= self.square + dx*MX + dy*MY < 64
            on_occupied = lambda dx, dy: BB_SQUARES[self.square + dx*MX + dy*MY] & (occupied_mask[self.side]|occupied_mask[not self.side])
            no_wrap_around = lambda dx: (self.square + dx*MX)//8 == self.square//8
            
            for ix in [-1, 0, 1]:
                for iy in [-1, 0, 1]:
                    if ix == iy == 0:
                        continue
                    
                    dx = ix
                    dy = iy
                    while no_wrap_around(dx) and on_board(dx, dy) and not on_occupied(dx, dy):
                        moves.append(Move(self.square, self.square + dx*MX + dy*MY))
                        dx += ix
                        dy += iy

                    # attacking
                    if on_board(dx, dy) and not occupied_mask[self.side] & BB_SQUARES[self.square + dx*MX + dy*MY]:
                        moves.append(Move(self.square, self.square + dy*MY, attacking=True))
            
        if can_exit:
            return moves
        
        drint('piece type fell through in Piece.passive_move_mask(occupied_mask)')
        input('read error pls')
        return 0
            
    def attack_move_mask(self, occupied_mask, en_passant_square):
        pass
        
    
    
drint(__file__, 'tl done')

if __name__ == '__main__':
    in_fen = input('fen: ')
    if in_fen == '':
        in_fen = STARTING_FEN
        # in_fen = 'RNBQKBNR/8/8/8/8/8/8/rnbqkbnr w KQkq - 0 1'

    b = Board(in_fen)
    b.show_moves()
    b.push(Move(from_square=E2, to_square=E4))
    b.push(Move(from_square=E7, to_square=E5))
    b.push(Move(from_square=F1, to_square=E2))
    b.push(Move(from_square=D7, to_square=D6))
    b.push(Move(from_square=G1, to_square=F3))
    b.push(Move(from_square=F7, to_square=F6))
    b.show_moves()
    b.push(Move.from_uci("O-O", context=b))
    b.show_moves()