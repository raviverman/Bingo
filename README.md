# Bingo
A bingo game playable over network.

* Features
    * Host a game over lan
    * Connect to the server
    * N dimensional bingo

## How to play?
Run the `Main.py` with python3. Currently, it runs in CLI (GUI incoming).
```
python3 Main.py
```

## Documentation

In `NetworkAPI.py`,
```python
class Network([serverIP, serverPort])
    startServer() <- starts a server on 0.0.0.0 on port 9000
    connectServer() <- connects to serverIP set in during
                     init
    send(str) <- send to server/client (supports single client currently)
    receive() <- receive from server/client
```

In `BingoUtilMixin.py`,
```python
class BingoUtilMixin
    randomizeMatrix(int[][]) <- randomizes matrix
    buildMap(int[][]) <- builds number to x,y map in matrix
    generateBingoBoard() <- generates bingo board with sequential entry
```

### GUI Architecture

TODO