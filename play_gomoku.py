def is_empty(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    y_start= y_end - (length-1)*d_y
    x_start= x_end - (length-1)*d_x
    start_bounded = end_bounded = False

    if not (0 <= y_start - d_y <= len(board) - 1) or not (0 <= x_start - d_x <= len(board) - 1):
        start_bounded = True
    elif board[y_start-d_y][x_start-d_x] in ["b","w"]: # If true, y_start, x_start bounded by stone/edge
        start_bounded = True

    if not (0 <= y_end + d_y <= len(board) - 1) or not (0 <= x_end + d_x <= len(board) - 1):
        end_bounded = True
    elif board[y_end + d_y][x_end + d_x] in ["b","w"]: # If true, y_end, x_end bounded by stone/edge
        end_bounded = True

    if start_bounded and end_bounded:
        return "CLOSED"
    elif start_bounded or end_bounded:
        return "SEMIOPEN"
    else:
        return "OPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    y, x = y_start, x_start
    open_seq_count, semi_open_seq_count = 0, 0

    # Keep checking as long as x and y are within the board range
    while 0 <= y <= len(board) - length * d_y and 0 <= x <= len(board[0]) - length * d_x:
        i = 1
        cur_seq = True
        # Keep checking for all sequences that start at y,x
        while i <= length:
            if board[y+ (i-1)* d_y][x+ (i-1) * d_x] != col:
                cur_seq = False
            i += 1

            #elif board[y+ (i-1) * d_y][x+ (i-1) * d_x] == col:
        # while i <= length:
        #     if board[y+ (i-1)* d_y][x+ (i-1) * d_x] != col:
        #         i += 1
        #         cur_seq = False
        #     elif board[y+ (i-1) * d_y][x+ (i-1) * d_x] == col:
        #         i += 1

        if cur_seq == False:
            y += d_y
            x += d_x
        if cur_seq == True:
            # This condition is only true if the entire length was checked and
            # all the same colour, col
            y += d_y * (i-1)
            x += d_x * (i-1)

            if x < -1:
                return open_seq_count, semi_open_seq_count

            # y-d_y and x-d_x are the coords of the stone AT the LAST position of length
            if is_bounded(board, y-d_y, x-d_x, length, d_y, d_x) == "OPEN":
                open_seq_count += 1

            elif is_bounded(board, y-d_y, x-d_x, length, d_y, d_x) == "SEMIOPEN":
                # Check if  we are at the edge of the board
                # We can safely say semiopen if we are
                if y >= len(board) or x >= len(board[0]) or x < 0:
                    semi_open_seq_count += 1
                    # no more need for checking since we're at the edge
                    return open_seq_count, semi_open_seq_count

                # If next stone is also the same colour, don't add anything
                elif board[y][x] != col:
                    if y-d_y-length*d_y >= 0 and 0<= x-d_x-length*d_x < len(board):
                        if board[y-length*d_y-d_y][x-length*d_x-d_x] != col:
                            semi_open_seq_count += 1
                    else:
                        semi_open_seq_count += 1
    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):

    open_seq_count, semi_open_seq_count = 0, 0
    #Do the horizontals, verticals, and two diagonal directions

    # sweep through board to check ROW BY ROW
    for hor in range(len(board)):
        open_seq_count += detect_row(board, col, hor, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, hor, 0, length, 0, 1)[1]
    #sweep through board to check COLUMN BY COLUMN
    for vert in range(len(board[0])):
        open_seq_count += detect_row(board, col, 0, vert, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, 0, vert, length, 1, 0)[1]
    # diagonal right down
    for diag1 in range(len(board)):
        open_seq_count += detect_row(board, col, diag1, 0, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, diag1, 0, length, 1, 1)[1]
    for diag1 in range(len(board)-1):
        open_seq_count += detect_row(board, col, 0, diag1+1, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, 0, diag1+1, length, 1, 1)[1]

    #diagonal left down
    for diag2 in range(len(board)-1):
        open_seq_count += detect_row(board, col, diag2+1, 7, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, diag2+1, 7, length, 1, -1)[1]
    for diag2 in range(len(board)):
        open_seq_count += detect_row(board, col, 0, diag2, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, 0, diag2, length, 1, -1)[1]

    return open_seq_count, semi_open_seq_count

def five(board, col):

    for i in range(len(board)):
        for j in range(len(board[0])-4):
            # Horizontal tests
            k = 0
            while j+k < len(board) and board[i][j+k] == col:
                k += 1
            if k == 5:
                return True

    for i in range(len(board) - 4):
        for j in range(len(board[0])):
            #Vertical tests
            k = 0
            while i+k < len(board) and board[i+k][j] == col:
                k += 1
            if k == 5:
                return True

    for i in range(4):
        for j in range(4):
            # Diagonal right
            k = 0
            while i+k < len(board) and j+k < len(board) and board[i+k][j+k] == col:
                k += 1
            if k == 5:
                return True

    for i in range(4):
        for j in range(4,8):
            # Diagonal left down (1,-1)
            k = 0
            while i+k < len(board) and 0 <= j-k < len(board) and board[i+k][j-k] == col:
                k += 1
            if k == 5:
                return True

    return False

def search_max(board):
    board[0][0] = "b"
    cur = score(board)
    max = [(0,0), cur]
    board[0][0] = " "

    for move_y in range(len(board)):
        for move_x in range(len(board[0])):
            if board[move_y][move_x] == " ":
                board[move_y][move_x] = "b"
                if score(board) > max[1]:
                    max = [(move_y, move_x), score(board)]
                board[move_y][move_x] = " "
    return max[0]

def score(board):
    #DO NOT CHANGE
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):
    full_board = True
    for i in range(8):
        for j in range(8):
            if board[i][j] == " ":
                full_board = False
    if full_board:
        return "Draw"
    if detect_rows(board, "w", 5) != (0,0) or five(board,"w"):
        return "White won"
    if detect_rows(board,"b",5) != (0,0) or five(board,"b"):
        return "Black won"

    return "Continue playing"

def print_board(board):
    #DO NOT CHANGE
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    #DO NOT CHANGE
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    import time

    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    while True:
        # print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        time.sleep(1)
        # clear terminal
        print(chr(27) + "[2J")

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"


        print(chr(27) + "[2J")
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    #DO NOT CHANGE
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 6; y = 4; d_x = 1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 5
    x_end = 7

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    put_seq_on_board(board, 4, 5, -1, 1, 2 , "w")
    put_seq_on_board(board,7,2,-1,1,2,'w')
    print_board(board)
    if detect_row(board, "w", 2, 7, 2 , 1 , -1) == (1,1):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, 0, 3, 1, 0, 4, "w")
    print_board(board)
    #print(detect_rows(board, col,length))
    if detect_rows(board, col,length) == (0,1):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_five():
    board = make_empty_board(8)
    put_seq_on_board(board, 2, 2, 1, 0, 5, "w")
    print_board(board)
    print(five(board,'w'))
    if five(board,'w') == True:
        print("TEST CASE for five PASSED")
    else:
        print("TEST CASE for five FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

if __name__ == '__main__':
    #test_gomoku(2)
    # board = make_empty_board(8)
    # put_seq_on_board(board, 0, 4, 1, -1, 5, "w")
    # print_board(board)
    # print(five(board,"w"))

    play_gomoku(8)


