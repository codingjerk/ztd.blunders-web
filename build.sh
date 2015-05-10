#!/usr/bin/env sh

sed '/\.min\.css/b; /\.min\.js/b; s/\.css/\.min\.css/g; s/\.js/\.min\.js/g' index.html | htmlcompressor > compressed.html

csso css/main.css css/main.min.css
csso chessboardjs/css/chessboard.css chessboardjs/css/chessboard.min.css

closure --js js/main.js > js/main.min.js
closure --js chessboardjs/js/chessboard.js > chessboardjs/js/chessboard.min.js
# closure make this library unusable, check it. sed '253,/,$/s/,$//;443,/turn$/s/turn$/turn,/;1415,1416d;1417s/.*/}/' chessboardjs/js/chessboard.js | closure -O WHITESPACE_ONLY >
cp chessboardjs/js/chess.js chessboardjs/js/chess.min.js