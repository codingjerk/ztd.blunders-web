#pylint: disable=import-self,no-member
import chess

def blunderStartPosition(fenBefore, blunderMove):
    board = chess.Board(fenBefore)
    board.push(board.parse_san(blunderMove))

    return board.fen()
