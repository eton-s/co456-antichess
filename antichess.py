import chess
from chess import WHITE, BLACK, PIECE_TYPES
import argparse
import math
import time

# PawnMG      = 10,   PawnLG      = 10
# KnightMG    = 40,   KnightLG    = 40
# BishopMG    = 30,   BishopLG    = 30
# RookMG      = 50,   RookLG      = 60
# QweenMG     = 80,   QweenLG     = 90

PawnVal     = 10
KnightVal   = 30
BishopVal   = 30
RookVal     = 50
QweenVal    = 90

king_pos_vals_white = [
         22, 40, 10,  0,  0, 10, 40, 22,
         25, 10,  0,-10,-10,  0, 10, 25,
        -20,-25,-30,-35,-35,-30,-25,-20,
        -25,-30,-30,-45,-45,-30,-30,-25,
        -30,-42,-45,-55,-55,-45,-42,-30,
        -35,-42,-45,-55,-55,-45,-42,-35,
        -35,-42,-45,-55,-55,-45,-42,-35,
        -35,-40,-42,-50,-50,-42,-40,-35,
    ]
king_pos_vals_black = [
        -35,-40,-42,-50,-50,-42,-40,-35,
        -35,-42,-45,-55,-55,-45,-42,-35,
        -35,-42,-45,-55,-55,-45,-42,-35,
        -30,-42,-45,-55,-55,-45,-42,-30,
        -25,-30,-30,-45,-45,-30,-30,-25,
        -20,-25,-30,-35,-35,-30,-25,-20,
         25, 10,  0,-10,-10,  0, 10, 25,
         22, 40, 10,  0,  0, 10, 40, 22
    ]


def get_material_val(board: chess.Board) -> int:
    to_play = board.turn
    our_pieces = (
        len(board.pieces(chess.PAWN, to_play)),
        len(board.pieces(chess.KNIGHT, to_play)),
        len(board.pieces(chess.BISHOP, to_play)),
        len(board.pieces(chess.ROOK, to_play)),
        len(board.pieces(chess.QUEEN, to_play)),
        len(board.pieces(chess.KING, to_play)),
    )
    their_pieces = (
        len(board.pieces(chess.PAWN, not to_play)),
        len(board.pieces(chess.KNIGHT, not to_play)),
        len(board.pieces(chess.BISHOP, not to_play)),
        len(board.pieces(chess.ROOK, not to_play)),
        len(board.pieces(chess.QUEEN, not to_play)),
        len(board.pieces(chess.KING, not to_play)),
    )
    eval = \
    PawnVal     *(our_pieces[0] - their_pieces[0]) + \
    KnightVal   *(our_pieces[1] - their_pieces[1]) + \
    BishopVal   *(our_pieces[2] - their_pieces[2]) + \
    RookVal     *(our_pieces[3] - their_pieces[3]) + \
    QweenVal    *(our_pieces[4] - their_pieces[4])
    return eval



def king_safety_val(board: chess.Board) -> int:
    to_play = board.turn
    return king_safety_val_each(board, to_play) - king_safety_val_each(board, not to_play)


def king_safety_val_each(board: chess.Board, color: chess.Color) -> int:
    king_pos = 0
    val = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if (not(piece)):
            continue
        elif (piece.piece_type is chess.KING and piece.color is color):
            king_pos = square
    
    left  = True
    right = True
    up    = True
    down  = True
    
    if (0  <= king_pos <=  7):
        down = False
    if (56 <= king_pos <= 63):
        up = False
    if (king_pos % 8 == 0):
        left = False
    if ((king_pos + 1) % 8 == 0):
        right = False

    if (color):
        if (left and up):
            piece = board.piece_at(king_pos+7)
            if (piece):
                val += (((piece.color is color)*2)-1) * 20
        if (up):
            piece = board.piece_at(king_pos+8)
            if (piece):
                val += (((piece.color is color)*2)-1) * 20
        if (right and up):
            piece = board.piece_at(king_pos+9)
            if (piece):
                val += (((piece.color is color)*2)-1) * 20
        if (left):
            piece = board.piece_at(king_pos-1)
            if (piece):
                val += (((piece.color is color)*2)-1) * 15
        if (right):
            piece = board.piece_at(king_pos+1)
            if (piece):
                val += (((piece.color is color)*2)-1) * 15
        if (left and down):
            piece = board.piece_at(king_pos-9)
            if (piece):
                val += (((piece.color is color)*2)-1) * 10
        if (down):
            piece = board.piece_at(king_pos-8)
            if (piece):
                val += (((piece.color is color)*2)-1) * 10
        if (right and down):
            piece = board.piece_at(king_pos-7)
            if (piece):
                val += (((piece.color is color)*2)-1) * 10

    if (not color):
        if (left and up):
            piece = board.piece_at(king_pos+7)
            if (piece):
                val += (((piece.color is color)*2)-1) * 00
        if (up):
            piece = board.piece_at(king_pos+8)
            if (piece):
                val += (((piece.color is color)*2)-1) * 00
        if (right and up):
            piece = board.piece_at(king_pos+9)
            if (piece):
                val += (((piece.color is color)*2)-1) * 10
        if (left):
            piece = board.piece_at(king_pos-1)
            if (piece):
                val += (((piece.color is color)*2)-1) * 15
        if (right):
            piece = board.piece_at(king_pos+1)
            if (piece):
                val += (((piece.color is color)*2)-1) * 15
        if (left and down):
            piece = board.piece_at(king_pos-9)
            if (piece):
                val += (((piece.color is color)*2)-1) * 20
        if (down):
            piece = board.piece_at(king_pos-8)
            if (piece):
                val += (((piece.color is color)*2)-1) * 20
        if (right and down):
            piece = board.piece_at(king_pos-7)
            if (piece):
                val += (((piece.color is color)*2)-1) * 20

        if(color):
            val += king_pos_vals_white[king_pos]
        else:
            val += king_pos_vals_black[king_pos]
    return val


def can_castle_val(board: chess.Board) -> int:
    to_play = board.turn
    return can_castle_val_each(board, to_play) - can_castle_val_each(board, not to_play)


def can_castle_val_each(board: chess.Board, color: chess.Color) -> int:
    one_castle = board.has_castling_rights(color)
    two_castles = board.has_kingside_castling_rights(
        color) and board.has_queenside_castling_rights(color)
    return (one_castle * 75) + (two_castles * 25)
    '''
    if (color):
        can_castle_one = bool(board.castling_rights & chess.BB_A1) or  bool(board.castling_rights & chess.BB_H1)
        can_castle_two = bool(board.castling_rights & chess.BB_A1) and bool(board.castling_rights & chess.BB_H1)
    else:
        can_castle_one = bool(board.castling_rights & chess.BB_A8) or  bool(board.castling_rights & chess.BB_H8)
        can_castle_two = bool(board.castling_rights & chess.BB_H8) and bool(board.castling_rights & chess.BB_H8)
    return can_castle_one * 75 + can_castle_two * 25
    '''


def under_check_val(board: chess.Board) -> int:
    to_play = board.turn
    return - 500 * board.is_check()
    #return under_check_val_each(board, to_play) - under_check_val_each(board, not to_play)

# def under_check_val_each(board: chess.Board, color: chess.Color) -> int:
#    return 


# Determine list of legal moves in antichess given a board
def anti_chess_legal_moves(board: chess.Board):
    moves = []
    for move in board.legal_moves:
        if board.is_capture(move):
            moves.append(move)  # moves is list of legal captures
    if moves != []:
        return moves  # if at least one legal capture
    else:
        return board.legal_moves  # else same as normal chess

TIME_LIMIT = 5 # max time in seconds

# Determining best move with 3 levels of depth
def get_best_move(board: chess.Board, depth: int, player_white: bool) -> chess.Move:
    best_move = None
    best_score = -math.inf
    ac_legal_moves = anti_chess_legal_moves(board)
    start_time = time.time()
    for move in ac_legal_moves:
        if board.gives_check(move):
            return move
        board.push(move)
        score = minimax(board, depth, -math.inf, math.inf, player_white, start_time)
        board.pop()

        if score > best_score:
            best_score = score
            best_move = move
        
        end_time = time.time()
        if (end_time - start_time > TIME_LIMIT):
            break

    return best_move

# Minimax
# Black: minimize; White: maximize
def minimax(board: chess.Board, depth: int, alpha: float, beta: float, player_white: bool, start_time: int) -> float:
    # Game over or max depth reached
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    # Initialize best_score as -infinity for maximizing player (white) or infinity for minimizing player (black)
    best_score = -math.inf if player_white else math.inf

    ac_legal_moves = anti_chess_legal_moves(board)

    for move in ac_legal_moves:
        board.push(move)

        # Recursively call minimax to get the score of this move
        score = minimax(board, depth - 1, alpha, beta, player_white, start_time)

        board.pop()

        # Update best_score
        if player_white:
            # Maximizing player
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            # Minimizing player
            best_score = min(best_score, score)
            beta = min(beta, best_score)

        end_time = time.time()
        if (end_time - start_time > TIME_LIMIT):
            return best_score
        
        # Prune
        if beta <= alpha:
            break

    return best_score

# Heuristic
def evaluate_board(board: chess.Board) -> float:
    # TODO: Implement board evaluation function
    to_play = board.turn
    eval = \
        get_material_val(board) + \
        king_safety_val(board) + \
        can_castle_val(board) + \
        under_check_val(board)

    if board.is_game_over():
        winner = board.outcome().winner
        if winner == None:  # draw case, should have eval of 0? i think
            return 0
        elif winner == to_play:
            return 20000
        else:
            return -20000
    else:
        return eval


# Arguments for running the program
parser = argparse.ArgumentParser()
parser.add_argument('side')  # black or white
# print board/prompts iff true
parser.add_argument('--print', action="store_true")
side = BLACK  # side the AI plays on
if parser.parse_args().side == "white":
    side = WHITE
print_board = parser.parse_args().print
player_white = side == BLACK


# Initialize board
board = chess.Board()
num_moves = 0
curr_depth = 2

# Running the game
while not board.is_game_over():
    # Check for 50-move rule and repetition
    fifty_moves = board.is_fifty_moves()
    repetition = board.can_claim_threefold_repetition()
    if (fifty_moves or repetition):
        print("Forced draw due to",
              "fifty moves rule" if fifty_moves else "threefold repetition rule")
        break

    if print_board:
        print(board)
    if board.turn == side:
        # Let the AI make the move
        move = get_best_move(board, curr_depth, player_white)
        if print_board:
            print(f"AI moves: {move}")
        else:
            print(f"{move}")
        board.push(move)

        num_moves += 1
        if num_moves == 10:
            curr_depth += 1
            num_moves = 0
    else:
        # Prompt the user for a move
        if print_board:
            move = chess.Move.from_uci(input("Enter your move: "))
        else:
            move = chess.Move.from_uci(input())
        ac_legal_moves = anti_chess_legal_moves(board)
        if move not in ac_legal_moves:
            print("Illegal move, try again.")
            continue
        board.push(move)

# Game is over, print the final board position if needed
if print_board:
    print(board)
