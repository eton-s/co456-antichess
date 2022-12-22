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

PawnVal = 10
KnightVal = 30
BishopVal = 30
RookVal = 50
QweenVal = 90

king_pos_vals_white = [
    22, 40, 10,  0,  0, 10, 40, 22,
    25, 10,  0, -10, -10,  0, 10, 25,
    -20, -25, -30, -35, -35, -30, -25, -20,
    -25, -30, -30, -45, -45, -30, -30, -25,
    -30, -42, -45, -55, -55, -45, -42, -30,
    -35, -42, -45, -55, -55, -45, -42, -35,
    -35, -42, -45, -55, -55, -45, -42, -35,
    -35, -40, -42, -50, -50, -42, -40, -35,
]
king_pos_vals_black = [
    -35, -40, -42, -50, -50, -42, -40, -35,
    -35, -42, -45, -55, -55, -45, -42, -35,
    -35, -42, -45, -55, -55, -45, -42, -35,
    -30, -42, -45, -55, -55, -45, -42, -30,
    -25, -30, -30, -45, -45, -30, -30, -25,
    -20, -25, -30, -35, -35, -30, -25, -20,
    25, 10,  0, -10, -10,  0, 10, 25,
    22, 40, 10,  0,  0, 10, 40, 22
]


def get_material_val(board: chess.Board) -> int:
    white_pieces = (
        len(board.pieces(chess.PAWN, WHITE)),
        len(board.pieces(chess.KNIGHT, WHITE)),
        len(board.pieces(chess.BISHOP, WHITE)),
        len(board.pieces(chess.ROOK, WHITE)),
        len(board.pieces(chess.QUEEN, WHITE)),
        len(board.pieces(chess.KING, WHITE)),
    )
    black_pieces = (
        len(board.pieces(chess.PAWN, BLACK)),
        len(board.pieces(chess.KNIGHT, BLACK)),
        len(board.pieces(chess.BISHOP, BLACK)),
        len(board.pieces(chess.ROOK, BLACK)),
        len(board.pieces(chess.QUEEN, BLACK)),
        len(board.pieces(chess.KING, BLACK)),
    )
    eval = \
        PawnVal * (white_pieces[0] - black_pieces[0]) + \
        KnightVal * (white_pieces[1] - black_pieces[1]) + \
        BishopVal * (white_pieces[2] - black_pieces[2]) + \
        RookVal * (white_pieces[3] - black_pieces[3]) + \
        QweenVal * (white_pieces[4] - black_pieces[4])
    return eval


def king_safety_val(board: chess.Board) -> int:
    return king_safety_val_each(board, WHITE) - king_safety_val_each(board, BLACK)


def king_safety_val_each(board: chess.Board, color: chess.Color) -> int:
    king_pos = 0
    val = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if (not(piece)):
            continue
        elif (piece.piece_type is chess.KING and piece.color is color):
            king_pos = square

    left = True
    right = True
    up = True
    down = True

    if (0 <= king_pos <= 7):
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
    return can_castle_val_each(board, WHITE) - can_castle_val_each(board, BLACK)


def can_castle_val_each(board: chess.Board, color: chess.Color) -> int:
    one_castle = board.has_castling_rights(color)
    two_castles = board.has_kingside_castling_rights(
        color) and board.has_queenside_castling_rights(color)
    return (one_castle * 10) + (two_castles * 5)


def under_check_val(board: chess.Board) -> int:
    return - 500 * board.is_check()


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

TIME_LIMIT = 10 # max time in seconds

# Determining best move with 3 levels of depth
def get_best_move(board: chess.Board, player_white: bool) -> chess.Move:
    best_move = None
    best_score = -math.inf if player_white else math.inf
    ac_legal_moves = anti_chess_legal_moves(board)

    # Determine depth
    depth = 2
    if ac_legal_moves.count() <= 5:
        depth = 4
    elif ac_legal_moves.count() <= 8:
        depth = 3

    # Timer limit fallback
    start_time = time.time()
    
    for move in ac_legal_moves:
        if board.gives_check(move):
            return move
        board.push(move)
        score = minimax(board, depth, -math.inf, math.inf, player_white, start_time)
        board.pop()

        if player_white:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move
        
        # Timer limit fallback
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
    eval = \
        get_material_val(board) + \
        king_safety_val(board) + \
        can_castle_val(board) + \
        under_check_val(board)

    if board.is_game_over():
        winner = board.outcome().winner
        if winner == None:  # draw case, should have eval of 0? i think
            return 0
        elif winner == WHITE:
            return math.inf
        else:
            return -math.inf
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
        move = get_best_move(board, player_white)
        if print_board:
            print(f"AI moves: {move}")
        else:
            print(f"{move}")
        board.push(move)

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
