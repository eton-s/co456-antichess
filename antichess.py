import chess
from chess import WHITE, BLACK


def get_best_move(board: chess.Board) -> chess.Move:
    best_move = None
    best_score = -float("inf")

    for move in board.legal_moves:
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

    if board.turn == WHITE:
        best_score = -float("inf")
        for move in board.legal_moves:
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
        for move in board.legal_moves:
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


board = chess.Board()

while not board.is_game_over():
    print(board)
    if board.turn == WHITE:
        # Let the AI make the move
        move = get_best_move(board)
        print(f"AI moves: {move}")
        board.push(move)
    else:
        # Prompt the user for a move
        move = chess.Move.from_uci(input("Enter your move: "))
        if move not in board.legal_moves:
            print("Illegal move, try again.")
            continue
        board.push(move)

# Game is over, print the final board position
print(board)
