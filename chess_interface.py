import engine
import random


CHECK_VALUE = 400 # better than taking a bishop (hopefully finds a check with a bishop capture later)

def move_value(board, move):
    if move.promotion is not None:
        return float("-inf") if board.turn != playing_for else float("inf")
    
    piece = board.piece_at(move.from_square)
    from_value = position_value(piece, move.from_square, board.endgame)
    to_value = position_value(piece, move.to_square, board.endgame)
    position_change = to_value - from_value
    
    attack_value = 0.0
    if move.attacking:
        attack_value = capture_value(board, move)
    
    board.push(move)
    check = board.is_check()
    board.pop()
    
    move_value = attack_value + position_change + check*CHECK_VALUE
    if board.turn != engine.WHITE:
        move_value *= -1 # invert weight if the move is good for black
    
    return move_value

def capture_value(board, move):
    # comparison of piece value
    taking = board.piece_at(move.from_square)
    captured = board.piece_at(move.captured)
    return engine.piece_value[captured.piece_type] - engine.piece_value[taking.piece_type]

def position_value(piece, square, endgame):
    # returns mapping value of position for piece
    piece_type = piece.piece_type
    mapping = []
    if piece_type == engine.PAWN:
        mapping = engine.pawnEvalWhite if piece.side == engine.WHITE else engine.pawnEvalBlack
    if piece_type == engine.KNIGHT:
        mapping = engine.knightEval
    if piece_type == engine.BISHOP:
        mapping = engine.bishopEvalWhite if piece.side == engine.WHITE else engine.bishopEvalBlack
    if piece_type == engine.ROOK:
        mapping = engine.rookEvalWhite if piece.side == engine.WHITE else engine.rookEvalBlack
    if piece_type == engine.QUEEN:
        mapping = engine.queenEval
    if piece_type == engine.KING:
        # use end game piece-square tables if neither side has a queen
        if endgame:
            mapping = (
                engine.kingEvalEndGameWhite
                if piece.side == engine.WHITE
                else engine.kingEvalEndGameBlack
            )
        else:
            mapping = engine.kingEvalWhite if piece.side == engine.WHITE else engine.kingEvalBlack

    return mapping[square]

def board_value(board):
    # returns material advantage
    endgame = board.endgame
    # for p in board.pieces:
    #     if not p.active: continue
        
    #     value = engine.piece_value[p.piece_type] + position_value(p, p.square, endgame)
    #     total += value if p.side == engine.WHITE else -value
    
    return sum(map(lambda x: (engine.piece_value[x.piece_type]*x.active + position_value(x, x.square, endgame))*(1 if x.side==engine.WHITE else -1), board.pieces))

def get_ordered_moves(board):
    return sorted(board.legal_moves(), key=lambda x: move_value(board, x))

def minimax(depth, board, alpha=float('-inf'), beta=float('inf'), maximising=engine.WHITE):
    # returns (value, nodes)
    if board.is_checkmate(): return (engine.mate_score, 1)
    
    if depth == 0: return (board_value(board), 1)
    
    if maximising == engine.WHITE:
        best_value = float('-inf')
        best_move_value = float('-inf')
        i = 0
        total_subnodes = 0
        for m in get_ordered_moves(board):
            mv_m = move_value(board, m)
            if depth <= move_value_optimisation_depth and mv_m < best_move_value*move_value_optimisation_cutoff: continue
            
            board.push(m)
            value, subnodes = minimax(depth - 1, board, alpha, beta, not maximising)
            board.pop()
            value += mv_m
            
            total_subnodes += subnodes

            if value > best_value:
                best_value = value
                if depth <= move_value_optimisation_depth:
                    best_move_value = mv_m
            
            alpha = max(alpha, best_value)
            if beta <= alpha: break
            if ((depth < len(move_lims) and i > move_lims[depth]) or i > move_lim_default) and maximising == ignorable: break
            i += 1

        return (best_value, total_subnodes)
    
    else:
        best_value = float('inf')
        best_move_value = float('-inf')
        i = 0
        total_subnodes = 0
        for m in get_ordered_moves(board):
            if depth <= move_value_optimisation_depth and move_value(board, m) < best_move_value*move_value_optimisation_cutoff: continue
            
            board.push(m)
            value, subnodes = minimax(depth - 1, board, alpha, beta, not maximising)
            board.pop()
            value += move_value(board, m)
            
            total_subnodes += subnodes

            if value < best_value:
                best_value = value
                if depth <= move_value_optimisation_depth:
                    best_move_value = move_value(board, m)
            
            beta = min(beta, best_value)
            if beta <= alpha: break
            if ((depth < len(move_lims) and i > move_lims[depth]) or i > move_lim_default) and maximising == ignorable: break
            i += 1

        return (best_value, total_subnodes)

def rank_moves(depth, board, maximising=engine.WHITE):
    valued_moves = []
    for m in board.legal_moves():
        board.push(m)
        valued_moves.append((m, minimax(depth, board, maximising=maximising)))
        board.pop()
        print(*valued_moves[-1])
    
    return sorted(valued_moves, key=lambda x: x[1][0], reverse=True)

# in_fen = input('fen: ')
# if in_fen == '':
#     in_fen = engine.STARTING_FEN

b = engine.Board()
# for i in range(50):
#     move = random.choice(b.moves())
#     b.push(move)

move_lims = [10, 10] # only consider the top {move_lim[depth]} moves of the ignorable player (computer)
move_lim_default = float('inf') # every move
move_value_optimisation_cutoff = 1/2 # any move with less than best_move_value*{move_value_optimisation_cutoff} in minimax will be discarded
move_value_optimisation_depth = 2 # only implements the algorithm when depth is <= {move_value_optimisation_depth}
ignorable = engine.WHITE # 

print('Optimisations:')
print('\tmv_l dpth:', move_lims)
print('\tmv_l dflt:', move_lim_default)
print('\tmv_o cut', move_value_optimisation_cutoff)
print('\tmv_o dpth:', move_value_optimisation_depth)
print('\tignr:', 'WHITE' if ignorable == engine.WHITE else 'BLACK')
input('start?')
for i in range(15):
    b.push(random.choice(list(b.moves())))

while 1:
    m = rank_moves(3, b)
    b.push(m[0][0])
    print(m)
    print(b.move_stack)
    # r = input('respond: ')
    # b.push(engine.Move.from_uci(r))