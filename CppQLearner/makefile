CC = g++
CPPFLAGS = -Wall --std=c++17 -O3
PROG = playTicTacToe
OBJS = playTicTacToe.o TicTacToe.o
SRCS = playTicTacToe.cpp TicTacToe.cpp

build: $(OBJS)
	$(CC) $(CPPFLAGS) -o $(PROG) $(OBJS)

.PHONY: clean
clean:
	rm -f $(OBJS)

depend:
	makedepend -- $(CPPFLAGS) -- -Y $(SRCS)

# DO NOT DELETE

playTicTacToe.o: QLearner.h TicTacToe.h GameSetup.h
	$(CC) $(CPPFLAGS) -c playTicTacToe.cpp
TicTacToe.o: TicTacToe.h GameSetup.h QLearner.h
	$(CC) $(CPPFLAGS) -c TicTacToe.cpp
