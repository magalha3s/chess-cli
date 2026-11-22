# Lib imports
import os
import copy
from pathlib import Path
import subprocess

# Local imports
import utils


def play_turn(board, board_ui_map, ui):

    print_board(board, board_ui_map, ui)

    pawn = input("Piece to move: ")

    while len(pawn) != 2:
        print_board(board, board_ui_map, ui)
        pawn = input("Invalid piece, type a valid piece: ")
    if len(pawn) == 2:
        while pawn[0] not in "12345678":
            print_board(board, board_ui_map, ui)
            pawn = input("Invalid piece, type a valid piece: ")

        while pawn[1] not in "ABCDEFGH":
            print_board(board, board_ui_map, ui)
            pawn = input("Invalid piece, type a valid piece: ")

    pawn = (int(pawn[0])-1, ord(pawn[1]) - ord("A"))
    piece_type = board[pawn[0]][pawn[1]]["type"]

    if piece_type == "pawn":
        valid_moves = valid_moves_pawn(pawn[0],pawn[1],board)
    elif piece_type == "bishop":
        valid_moves = valid_moves_bishop(pawn[0],pawn[1],board)
    elif piece_type == "knight":
        valid_moves = valid_moves_knight(pawn[0],pawn[1],board)
    elif piece_type == "tower":
        valid_moves = valid_moves_tower(pawn[0],pawn[1],board)
    elif piece_type == "queen":
        valid_moves = valid_moves_queen(pawn[0],pawn[1],board)
    elif piece_type == "king":
        valid_moves = valid_moves_king(pawn[0],pawn[1],board)

    # Print board with move hints
    print_preview_board(board, board_ui_map, ui, valid_moves)
    
    move = input("Where to move: ")

    while len(move) != 2:
        print_board(board, board_ui_map, ui)
        move = input("Invalid piece, type a valid piece: ")
    if len(move) == 2:
        while move[0] not in "12345678":
            print_board(board, board_ui_map, ui)
            move = input("Invalid piece, type a valid piece: ")

        while move[1] not in "ABCDEFGH":
            print_board(board, board_ui_map, ui)
            move = input("Invalid piece, type a valid piece: ")

    move = (int(move[0])-1, ord(move[1]) - ord("A"))

    while move not in valid_moves:
        print_preview_board(board, board_ui_map, ui, valid_moves)
        move = input("Invalid move, type a valid move: ")
        move = (int(move[0])-1, ord(move[1]) - ord("A"))

    # Move piece in board
    move_piece(move, pawn, valid_moves, board)

    # Print updated board
    print_board(board, board_ui_map, ui)

def print_board(board : list[list[dict]], board_ui_map : list[list[tuple[int,int]]], ui : list[list[str]]):
        os.system("clear")
        ui = copy.deepcopy(ui)

        for row, pieces in enumerate(board):
            for column, piece in enumerate(pieces):
                # Translate row,column to row, column in ui
                ui_row, ui_column = board_ui_map[row][column][0], board_ui_map[row][column][1]

                # Swap ui's blank space for piece char
                ui[ui_row][ui_column] = piece["char"]

        for line in ui:
            print("".join(line),end="")

        print("\n--------------------------------------")

def print_preview_board(board, board_ui_map, ui, valid_moves):
        os.system("clear")
        
        ui = copy.deepcopy(ui)

        for row, pieces in enumerate(board):
            for column, piece in enumerate(pieces):
                # Translate row,column to row, column in ui
                ui_row, ui_column = board_ui_map[row][column][0], board_ui_map[row][column][1]

                # Swap ui's blank space for piece char
                if (row, column) in valid_moves:
                    if board[row][column]["owner"] == None:
                        ui[ui_row][ui_column] = "x"
                    else:
                        ui[ui_row][ui_column] = f"{piece["char"]}\u0338"
                else:
                    ui[ui_row][ui_column] = piece["char"]
        for line in ui:
            print("".join(line),end="")

        print("\n--------------------------------------")

def valid_moves_pawn(row,column, board) -> list[tuple[int,int]]:
    valid_moves = []
    # pawn informations

    owner = board[row][column]["owner"]
    
    if column < 7 and board[row+utils.op(owner)][column+1]["owner"] != owner and board[row+utils.op(owner)][column+1]["owner"] != None:
        valid_moves.append((row+utils.op(owner),column+1))


    if column > 0 and (board[row+utils.op(owner)][column-1]["owner"] != owner) and (board[row+utils.op(owner)][column-1]["owner"] != None):
        valid_moves.append((row+utils.op(owner),column-1))

    if row > 0 and row < 7 and board[row+utils.op(owner)][column]["owner"] == None:
        valid_moves.append((row+utils.op(owner),column))

    return valid_moves

def valid_moves_knight(row, column, board) -> list[tuple[int,int]]:
    grid = utils.make_grid()
    owner = board[row][column]["owner"]

    valid_moves = []
    possible_valid_moves = ((row+2,column-1), (row+2,column+1), (row-2,column-1), (row-2,column+1), (row-1, column-2), (row+1, column-2), (row-1, column+2), (row+1, column+2))

    for move in possible_valid_moves:
        if move not in grid:
            pass
        elif board[move[0]][move[1]]["owner"] == owner:
            pass
        else:
            valid_moves.append(move)

    return valid_moves

def valid_moves_bishop(row, column, board) -> list[tuple[int,int]]:
    grid = utils.make_grid()
    owner = board[row][column]["owner"]

    valid_moves = []
    # First Quadrant
    i = 1
    while (possible_move := (row-i,column+i)) in grid and board[row-i][column+i]["owner"] != owner:
        if board[row-i][column+i]["owner"] != None:
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    # Second Quadrant
    i = 1
    while (possible_move := (row-i,column-i)) in grid and board[row-i][column-i]["owner"] != owner:
        if board[row-i][column-i]["owner"] != None:
            print(board[row-i][column-i])
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    # Third Quadrant
    i = 1
    while (possible_move := (row+i,column-i)) in grid and board[row+i][column-i]["owner"] != owner:
        if board[row+i][column-i]["owner"] != None:
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    # Fourth Quadrant
    i = 1
    while (possible_move := (row+i,column+i)) in grid and board[row+i][column+i]["owner"] != owner:
        if board[row+i][column+i]["owner"] != None:
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    return valid_moves

def valid_moves_tower(row, column, board) -> list[tuple[int,int]]:
    grid = utils.make_grid()
    owner = board[row][column]["owner"]

    valid_moves = []
    # First Quadrant
    i = 1
    while (possible_move := (row,column+i)) in grid and board[row][column+i]["owner"] != owner:
        if board[row][column+i]["owner"] != None:
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    # Second Quadrant
    i = 1
    while (possible_move := (row,column-i)) in grid and board[row][column-i]["owner"] != owner:
        if board[row][column-i]["owner"] != None:
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    # Third Quadrant
    i = 1
    while (possible_move := (row+i,column)) in grid and board[row+i][column]["owner"] != owner:
        if board[row+i][column]["owner"] != None:
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    # Fourth Quadrant
    i = 1
    while (possible_move := (row-i,column)) in grid and board[row-i][column]["owner"] != owner:
        if board[row-i][column]["owner"] != None:
            valid_moves.append(possible_move)
            break
        else:
            valid_moves.append(possible_move)
        i+=1

    return valid_moves

def valid_moves_queen(row, column, board) -> list[tuple[int,int]]:
    return valid_moves_tower(row,column, board) + valid_moves_bishop(row, column, board)

def valid_moves_king(row, column, board) -> list[tuple[int,int]]:
    grid = utils.make_grid()
    owner = board[row][column]["owner"]

    valid_moves = []
    possible_valid_moves = [(row,column+1), (row,column-1), (row-1,column), (row+1,column), (row+1,column-1), (row+1,column+1), (row-1,column-1), (row-1,column+1)]

    for move in possible_valid_moves:
        if move not in grid:
            pass
        elif board[move[0]][move[1]]["owner"] == owner:
            pass
        else:
            valid_moves.append(move)

    return valid_moves

def move_piece(move : tuple[int, int], piece_pos,valid_moves : list, board) -> None:
    row, column = move
    prow, pcolumn = piece_pos


    if board[prow][pcolumn]["type"] == "pawn" and (row == 7 or row == 0):
        board[row][column] = utils.promote(tp=board[prow][pcolumn]["owner"]) 
        board[prow][pcolumn] = utils.assign_owner(" ", None, None)

    elif board[row][column]["owner"] != None:
        piece = board[row][column]

        board[row][column] = board[prow][pcolumn]
        board[prow][pcolumn] = utils.assign_owner(" ", None, None)
        
        return piece
    else:
        board[row][column] = board[prow][pcolumn]
        board[prow][pcolumn] = utils.assign_owner(" ", None)

def assign_owner(char,owner,tp = None):
    return {"owner": owner, "char": char, "type": tp}

def make_board() -> list[list[dict]]:

    board = []

    # Black Row
    black_king_row = [assign_owner("♜","black","tower"), assign_owner("♞","black","knight"), assign_owner("♝","black","bishop"), assign_owner("♛","black","queen"), assign_owner("♚","black","king"), assign_owner("♝","black","bishop"), assign_owner("♞","black","knight"), assign_owner("♜","black","tower")]
    black_paw_row = [assign_owner("♟","black","pawn"), assign_owner("♟","black","pawn"), assign_owner("♟","black","pawn"), assign_owner("♟","black","pawn"), assign_owner("♟","black","pawn"), assign_owner("♟","black","pawn"), assign_owner("♟","black","pawn"), assign_owner("♟","black","pawn")]

    # Empty Row
    empty_row = [assign_owner(" ", None), assign_owner(" ", None), assign_owner(" ", None), assign_owner(" ", None), assign_owner(" ", None), assign_owner(" ", None), assign_owner(" ", None), assign_owner(" ", None)]

    # White Row
    white_paw_row = [assign_owner("♙","white","pawn"), assign_owner("♙","white","pawn"), assign_owner("♙","white","pawn"), assign_owner("♙","white","pawn"), assign_owner("♙","white","pawn"), assign_owner("♙","white","pawn"), assign_owner("♙","white","pawn"), assign_owner("♙","white","pawn")]
    white_king_row = [assign_owner("♖","white","tower"), assign_owner("♘","white","knight"), assign_owner("♗","white","bishop"), assign_owner("♕","white","queen"), assign_owner("♔","white","king"), assign_owner("♗","white","bishop"), assign_owner("♘","white","knight"), assign_owner("♖","white","tower")]


    # Make Board
    board.append(black_king_row)
    board.append(black_paw_row)

    for _ in range(4):
        board.append(copy.deepcopy(empty_row))

    board.append(white_paw_row)
    board.append(white_king_row)

    return board

def make_ui(pth : Path = Path("board.txt")) -> list[list[str]]:
    if not pth.exists():
        raise FileNotFoundError("UI file not found, please install 'board.txt'")
    
    with open(pth, "r") as file:
        # load ui file and converters everything to type list
        file = list(file.readlines())
        file = [list(line) for line in file]

    return file

def board_ui_map(ui) -> dict:
    board_ui_map = []


    for i, chars in enumerate(ui):
        row = []
        if i == 0 or i%2 != 0:
            pass
        else:
            for j in utils.parse_board_line("".join(chars)):
                row.append((i,j))
            board_ui_map.append(row)

    return board_ui_map


                
    return board_ui_map