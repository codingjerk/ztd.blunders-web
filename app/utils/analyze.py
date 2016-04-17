import chess
import chess.uci

engine_path = "/opt/stockfish/src/stockfish"
engine_time = 5000

def analyzePosition(fen):
    # TODO: what if engine not exist
    engine = chess.uci.popen_engine(engine_path)
    engine.uci()
    engine.isready()

    handler = chess.uci.InfoHandler()
    engine.info_handlers.append(handler)

    board = chess.Board(fen)
    engine.position(board)
    engine.isready()

    promise = engine.go(movetime=engine_time, async_callback=True)

    promise.result()
    print(handler.info)
