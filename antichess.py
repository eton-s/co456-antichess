import chess
from chess import WHITE, BLACK
import argparse

# returns list of legal moves in antichess given a board
def anti_chess_legal_moves(board: chess.Board):
    moves = []
    for move in board.legal_moves:
        if board.is_capture(move):
            moves.append(move) # moves is list of legal captures
    if moves != []:
        return moves # if at least one legal capture
    else:
        return board.legal_moves # else same as normal chess
            

def get_best_move(board: chess.Board) -> chess.Move:
    best_move = None
    best_score = -float("inf")
    ac_legal_moves = anti_chess_legal_moves(board)
    for move in ac_legal_moves: 
        board.push(move)
        score = -minimax(board, depth=4, alpha=-
                         float("inf"), beta=float("inf"))
        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def minimax(board: chess.Board, depth: int, alpha: float, beta: float) -> float:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    ac_legal_moves = anti_chess_legal_moves(board)
    if board.turn == WHITE:
        best_score = -float("inf")
        for move in ac_legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta)
            board.pop()
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float("inf")
        for move in ac_legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta)
            board.pop()
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def evaluate_board(board: chess.Board) -> float:
    # TODO: Implement board evaluation function
    return 0

# argparse stuff
parser = argparse.ArgumentParser()
parser.add_argument('side') # black or white
parser.add_argument('--print', action="store_true") # print board/prompts iff true
side = BLACK # side the AI plays on
if parser.parse_args().side == "white":
    side = WHITE
print_board = parser.parse_args().print

board = chess.Board()

while not board.is_game_over():
    if print_board:
        print(board)
    if board.turn == side:
        # Let the AI make the move
        move = get_best_move(board)
        if print_board:
            print(f"AI moves: {move}")
        board.push(move)
    else:
        # Prompt the user for a move
        if print_board:
            move = chess.Move.from_uci(input("Enter your move: "))
        else:
            move = chess.Move.from_uci(input())            
        if move not in board.legal_moves: 
            print("Illegal move, try again.")
            continue
        board.push(move)

# Game is over, print the final board position
if print_board:
    print(board)
