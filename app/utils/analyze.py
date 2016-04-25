import chess
import chess.uci

class Engine:
    def __init__(self, path):
        self.engine = chess.uci.popen_engine(path)
        self.engine.uci()
        self.engine.isready()

        self.handler = chess.uci.InfoHandler()
        self.engine.info_handlers.append(self.handler)

        self.board = chess.Board()

        if not self.engine.is_alive():
            raise Exception("Engine failed to start")

    def __enter__(self):
        return self

    def new(self):
        self.engine.ucinewgame()
        self.engine.isready()

    def set(self, fen):
        self.board = chess.Board(fen)
        self.engine.position(self.board)
        self.engine.isready()

    def is_game_over(self):
        return self.board.is_game_over()

    def __cloneScore(self, score):
        return { "cp": score.cp, "mate": score.mate }

    def __pvToStr(self, fen, line):
        board = chess.Board(fen)

        result = []
        for move in line:
            movestr = board.san(move)
            result.append(movestr)
            board.push(move)

        return result

    def __filterMove(self, index):
        pv = self.handler.info['pv']
        score = self.handler.info['score']
        if pv == {} or score == {}:
            return None

        if index not in pv or index not in score:
            return None

        lineStr = self.__pvToStr(self.board.fen(), pv[index])
        scoreStr = self.__cloneScore(score[index])

        return {
            'line': lineStr,
            'score': scoreStr
        }

    def think(self, timeToThink, move = None):
        searchmoves = None
        self.engine.isready()
        if move is not None:
            searchmoves = [self.board.parse_san(move)]

        promise = self.engine.go(movetime=timeToThink, searchmoves=searchmoves, async_callback=True)

        promise.result()
        result = self.__filterMove(1)
        if result is None:
           raise Exception('Engine failed to analyze blunder')

        return result

    def moveLine(self, line):
        for move in line:
            move_int = self.board.parse_san(move)
            if move_int not in self.board.legal_moves:
                raise Exception("Illegal move in this position")
            self.board.push(move_int)
        self.engine.position(self.board)
        self.engine.isready()

    def moveOne(self, move):
        self.moveLine([move])

    def unmove(self):
        self.board.pop()
        self.engine.position(self.board)
        self.engine.isready()

    def __enter__(self):
        return self

    def __exit__(self, exception, _1, _2):
        self.engine.quit()
