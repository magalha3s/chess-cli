import moves as mv

board = mv.make_board()
ui = mv.make_ui()
board_ui_map = mv.board_ui_map(ui)


while True:
    mv.play_turn(board, board_ui_map, ui)