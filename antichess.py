import chess
from chess import WHITE, BLACK
import argparse

#PawnMG      = 10,   PawnLG      = 10
#KnightMG    = 40,   KnightLG    = 40
#BishopMG    = 30,   BishopLG    = 30
#RookMG      = 50,   RookLG      = 60
#QweenMG     = 80,   QweenLG     = 90

PawnVal     = 10
KnightVal    = 30
BishopVal   = 30
RookVal     = 50
QweenVal    = 90


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
    return 0



def can_castle_val(board: chess.Board) -> int:
    to_play = board.turn
    return can_castle_val_each(board, to_play) - can_castle_val_each(board, not to_play)

def can_castle_val_each(board: chess.Board, color: chess.Color) -> int:
    one_castle = board.has_castling_rights(color)
    two_castles= board.has_kingside_castling_rights(color) and board.has_queenside_castling_rights(color)
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

#def under_check_val_each(board: chess.Board, color: chess.Color) -> int:
#    return 



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
    eval = \
    get_material_val(board) + \
    king_safety_val(board) + \
    can_castle_val(board) + \
    under_check_val(board)
    
    if board.is_game_over():
        winner = board.outcome().winner
        if winner == None: # draw case, should have eval of 0? i think
            return 0
        elif winner == to_play:
            return 200 
        else:
            return -200
    else:
        return eval

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

# Game is over, print the final board position
if print_board:
    print(board)
