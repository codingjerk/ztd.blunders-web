#pylint: disable=import-self,no-member
import chess

def join(blunder_move, forced_line):
    return [blunder_move] + forced_line

def boardAfterVariation(fen, line):
    board = chess.Board(fen)

    for move in line:
        move_int = board.parse_san(move)
        if move_int not in board.legal_moves:
            raise Exception("Illegal move in this position")
        board.push(move_int)

    return board

def fenAfterVariation(fen, line):
    return boardAfterVariation(fen, line).fen()

def blunderStartPosition(fenBefore, blunderMove):
    fen = fenAfterVariation(fenBefore, [blunderMove])
    return fen

def compareLines(blunder_move, forced_line, user_line):
    # TODO: Compare using pychess
    return join(blunder_move, forced_line) == user_line

def mismatchCheck(blunder_move, forced_line, user_line):
    # It is ok, that best line can be recalculated one day and to be changed
    # We are checking if this happens and return error, so client will reload the pack
    originalLine = join(blunder_move, forced_line)

    # Userline can't be longer, then original line
    if(len(user_line) > len(originalLine)):
        return True

    if originalLine[:len(user_line) - 1 ] != user_line[:-1]:
        return True

    return False

# We assume user_line is shorter(or at least same size), than solution
# mismatchCheck should be called before and check this
def boardsToAnalyze(fen_before, blunder_move, forced_line, user_line):
    line = user_line[:-1]
    userMove = user_line[len(line)]
    bestMove = join(blunder_move, forced_line)[len(line)]

    if(userMove == bestMove):
        return [{
            'user_line': line,
            'user_move': userMove
        }]

    return [{
            'user_line': line,
            'user_move': userMove
        },
        {
            'user_line': line,
            'user_move': bestMove
        }]
