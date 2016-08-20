#include <iostream>
#include <vector>
#include <algorithm>
#include <memory>

#include "QLearner.h"

template<typename GameState, typename Action>
class Player {
public:
  virtual const Action play(const GameState& state);
};

template<class Game, typename GameState, typename Action>
class HumanPlayer : public Player<GameState, Action> {
public:
  HumanPlayer(Game& game) :
    game_(game)
  { }

  virtual const Action play(const GameState& state) {
    auto actions = game_.actions(state);
    int move;
    while(true) {
      std::cout << "Available moves:";
      for (const auto& action : actions) {
        std::cout << " " << action;
      }
      std::cout << "\n";
      std::cout << "Please pick one of the available moves: ";
      std::cin >> move;
      if (std::find(actions.begin(), actions.end(), move) != actions.end()) {
        return move;
      } else {
        std::cout << "That move is not available. Try again!";
      }
    }
  }
private:
  Game game_ = Game();
};

template<class Game, typename GameState, typename Action, typename QPair, typename QLearnerMap>
class AI : public Player<GameState, Action> {
public:
  AI(Game& game, double epsilon, double alpha, double gamma) :
    game_(game),
    gameAI_(game, alpha, epsilon, gamma)
  { }

  virtual const Action play(const GameState& state) {
    return gameAI_.learnedMove(state);
  }

  void learnSteps(int64_t numSteps) {
    gameAI_.learnSteps(numSteps);
  }

  void learnGames(int64_t numGames) {
    gameAI_.learnGames(numGames);
  }

  QLearnerGameAI<Game, GameState, Action, QPair, QLearnerMap> gameAI_;
private:
  Game game_ = Game();

};

template<typename GameState, typename Action>
class Game {
public:
  virtual void playGame(std::vector<std::shared_ptr<Player<GameState, Action>>> players) {
    GameState state = startNewGame();
    int turn = 0;

    while (isGameRunning) {
      displayBoard(state);
      auto player = players[turn % players.size()];
      const Action move = player->play(state);
      state = takeAction(move);
      turn += 1;
    }
    displayGameEnd(state);
  }

  virtual const GameState startNewGame();
  virtual const GameState transition(const GameState& state, const Action& action);
  virtual const GameState takeAction(const Action& action);
  virtual void displayBoard(const GameState& state);
  virtual void displayGameEnd(const GameState& state);
  bool isGameRunning = false;
};
