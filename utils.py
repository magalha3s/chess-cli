def parse_board_line(line : str, start : int= 0) -> list[int]:
    column = line.find("|   |",start)
    if column == -1:
        return []
    else:
        return [column+2] + parse_board_line(line, column + 4)

def assign_owner(char,owner,tp = None):
    return {"owner": owner, "char": char, "type": tp}

def op(piece_type):
    if piece_type == "black":
        return 1
    elif piece_type == "white":
        return -1

def make_grid(n : int = 8) -> list[tuple[int,int]]:
    grid = []

    for i in range(n):
        for j in range(n):
            grid.append((i,j))

    return grid

def promote(tp):
    pass