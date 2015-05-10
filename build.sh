#!/usr/bin/env sh

sed '/\.min\.css/b; /\.min\.js/b; s/\.css/\.min\.css/g; s/\.js/\.min\.js/g' index.html | htmlcompressor > compressed.html

csso css/main.css css/main.min.css
csso chessboardjs/css/chessboard.css chessboardjs/css/chessboard.min.css

# Compile main.js with closure to get errors and warnings
closure --js js/main.js > /dev/null

uglifyjs -cm -- js/main.js > js/main.min.js
uglifyjs -cm -- chessboardjs/js/chessboard.js > chessboardjs/js/chessboard.min.js
uglifyjs -cm -- chessboardjs/js/chess.js > chessboardjs/js/chess.min.js