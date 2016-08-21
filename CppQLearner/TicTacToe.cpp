#include <vector>
#include <algorithm>
#include <iostream>

#include "TicTacToe.h"

const GameState TicTacToe::startNewGame() {
  isGameRunning = true;
  state_ = GameState();
  return state_;
}

const GameState TicTacToe::takeAction(const Action& action) {
  state_ = transition(state_, action);
  int winner = checkGameOver(state_, action);
  if (winner != -1) {
    isGameRunning = false;
  }
  return state_;
}

const std::vector<Action> TicTacToe::actions(const GameState& state) {
  std::vector<Action> actions = {};
  for (int i = 1; i <= 9; i++) {
    bool player_1 =
      std::find(state[0].begin(), state[0].end(), i) == state[0].end();
    bool player_2 =
      std::find(state[1].begin(), state[1].end(), i) == state[1].end();
    if (player_1 && player_2) {
      actions.push_back(i);
    }
  }
  return actions;
}

const GameState TicTacToe::transition(const GameState& state, const Action& action) {
  int turn = (state[0].size() + state[1].size()) % 2;
  auto newState = state;
  auto playersMoves = state[turn];
  playersMoves.push_back(action);
  newState[turn] = playersMoves;
  return newState;
}

const double TicTacToe::reward(const GameState& state, const Action& prevMove) {
  auto winner = checkGameOver(state, prevMove);
  if (winner > 0) {
    return 1;
  }
  return 0;
}

const bool TicTacToe::checkWin(const GameState& state, const int& player) {
  auto plays = state[player-1];
  std::array<std::array<int, 3>, 8> wins = {{
    {1,2,3}, {4,5,6}, {7,8,9}, {1,4,7}, {2,5,8}, {3,6,9}, {1,5,9}, {3,5,7}
  }};

  bool won = false;
  for (const auto& win : wins) {
    bool win_check = true;
    for (const auto& move : win) {
      bool notInPlays = std::find(plays.begin(), plays.end(), move) == plays.end();
      if (notInPlays) {
        win_check = false;
        break;
      }
    }

    if (win_check) {
      won = true;
      break;
    }
  }

  return won;
}

const bool TicTacToe::checkTie(const GameState& state) {
  return state[0].size() + state[1].size() == 9;
}

const int TicTacToe::checkGameOver(const GameState& state, const Action& prevMove) {
  for (int player = 1; player <= players; player++) {
    if (checkWin(state, player)) {
      return player;
    }
  }
  if (checkTie(state)) {
    return 0;
  }
  return -1;
}

const std::string TicTacToe::getBoard(const GameState& state) {
  std::string board(9, ' ');
  const auto& x = state[0];
  const auto& circle = state[1];

  for (auto& move : x) {
    board[move - 1] = 'X';
  }

  for (auto& move : circle) {
    board[move - 1] = 'O';
  }

  return board;
}

void TicTacToe::displayBoard(const GameState& state) {
  const auto& board = getBoard(state);
  auto printRow = [&] (int row) {
    std::cout << "   |   |\n";
    std::cout << " " << board[3 * row]
              << " | " << board[3 * row + 1]
              << " | " << board[3 * row + 2]
              << "\n";
    std::cout << "   |   |\n";
  };

  std::cout << "\n\n=======================\n\n";
  printRow(0);
  std::cout << "-----------\n";
  printRow(1);
  std::cout << "-----------\n";
  printRow(2);
}

void TicTacToe::displayGameEnd(const GameState& state) {
  displayBoard(state);
  auto winner = checkGameOver(state, 0);
  if (winner == 1) {
    std::cout << "X won!\n";
  } else if (winner == 2) {
    std::cout << "O won!\n";
  } else {
    std::cout << "It was a tie!\n";
  }
}

void TicTacToe::displayQPair(const GameState& state, const Action& action) {
  std::cout << "Displaying Q Pair:\n";
  std::cout << "Action: " << action << "\n";
  auto displayMoves = [&] (std::vector<Action> moves) {
    std::cout << "[";
    for (const auto& move : moves) {
      std::cout << move << " ,";
    }
    std::cout << "]";
  };
  std::cout << "Game state: (";
  displayMoves(state[0]);
  std::cout << ", ";
  displayMoves(state[1]);
  std::cout << ")\n";
}
