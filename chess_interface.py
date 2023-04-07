import engine
import random


playing_for = engine.WHITE
def move_value(board, move):
    if move.promotion is not None:
        return float("-inf") if board.turn != playing_for else float("inf")
    
    piece = board.piece_at(move.from_square)
    from_value = evaluate_piece(piece, move.from_square, board.endgame)
    to_value = evaluate_piece(piece, move.to_square, board.endgame)
    position_change = to_value - from_value
    
    capture_value = 0.0
    if move.attacking:
        capture_value = evaluate_capture(board, move)
    
    move_value = capture_value + position_change
    if board.turn != playing_for:
        move_value *= -1 # invert weight if the move is good for opposing side
    
    return move_value

def evaluate_capture(board, move):
    # comparison of piece value
    taking = board.piece_at(move.from_square)
    captured = board.piece_at(move.captured)
    return engine.piece_value[captured.piece_type] - engine.piece_value[taking.piece_type]

def evaluate_piece(piece, square, endgame):
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

def evaluate_board(board):
    total = 0
    endgame = board.endgame
    
    for p in board.pieces:
        if not p.active: continue
        
        value = engine.piece_value[p.piece_type] + evaluate_piece(p, p.square, endgame)
        total += value if p.side == playing_for else -value
    
    return total


def next_move(depth, board):
    move = minimax_root(depth, board)
    return move

def get_ordered_moves(board):
    # sort moves by move_value
    return list(sorted(board.moves(), key=lambda x: move_value(board, x)))

def minimax_root(depth, board):
    best_move = -float("inf")
    
    moves = get_ordered_moves(board)
    best_move_found = moves[0]
    
    for move in moves:
        board.push(move)
        value = minimax(depth - 1, board, -float("inf"), float("inf"))
        board.pop()
        if value >= best_move:
            best_move = value
            best_move_found = move
    
    return best_move_found

def minimax(depth, board, alpha, beta):
    # returns value of the best move on this board
    if board.is_checkmate():
        return MATE_SCORE if board.turn != playing_for else -MATE_SCORE
    
    if depth == 0:
        return evaluate_board(board)
    
    best_move = -float("inf")
    moves = get_ordered_moves()
    for move in moves:
        board.push(move)
        curr_move = minimax(depth - 1, board, alpha, beta)
        
        # fastest checkmate (?)
        if curr_move >= engine.mate_threshold:
            curr_move -= 1
        
        elif curr_move <= engine.mate_threshold:
            curr_move += 1
        
        best_move = max(best_move, curr_move)
        board.pop()
        alpha = max(alpha, curr_move)
        if beta <= alpha:
            return best_move
    return best_move


# in_fen = input('fen: ')
# if in_fen == '':
#     in_fen = engine.STARTING_FEN

b = engine.Board()
# for i in range(50):
#     move = random.choice(b.moves())
#     b.push(move)

print(minimax_root(1, b))