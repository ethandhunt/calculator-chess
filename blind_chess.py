import engine

print('type \'help\' for help text')

def filter(func, iter):
    for i in iter:
        if func(i):
            yield i

# moves can be tested for equality using the returned tuple
move_iden = lambda move: (move.from_square, move.to_square, move.captured)

board = engine.Board()
while 1:
    m_text = input('w: ' if board.turn == engine.WHITE else 'b: ')
    
    if 'help' in m_text:
        print('commands:')
        print('help - print this help')
        print('moves - print previous moves')
        print('AC,up to read more')
        print()
        
        if input('more? Y/aNy: ').upper() != 'Y': continue
        
        print()
        print('move format:')
        print('A1A2 - move')
        print('A1xA2 - capture')
        print('A5xB5B6 - en passant')
        print('A7A8Q - promote')
        print('O-O - castle kingside')
        print('O-O-O castle queenside')
        print()
        
        if input('more? Y/aNy: ').upper() != 'Y': continue

        print()
        print('technicalities:')
        print('x anywhere for attacking flag')
        print('x replaced with \'\' so no len change')
        print('promotion only works when len is 5')
        print('move_text is converted to uppercase')
            
        continue

    if m_text == 'moves':
        print(board.move_stack)
        continue
    
    try:
        m = engine.Move.from_uci(m_text, context=board)

        if move_iden(m) not in map(move_iden, board.legal_moves()):
            print('invalid move')
            continue

    except ValueError as e:
        print('bad move format')
        print(e)
        continue

    
    board.push(list(filter(lambda x: move_iden(x)==move_iden(m), board.legal_moves()))[0])
    
    if board.is_checkmate():
        print('checkmate')
        break

    if board.is_check():
        print('check')