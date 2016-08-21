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
    return game_.getPlayerMove(state);
  }
private:
  Game game_;
};

template<class Game, typename GameState, typename Action, typename QPair, typename QLearnerMap>
class AI : public Player<GameState, Action> {
public:
  AI(Game& game, double epsilon, double alpha, double gamma) :
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

private:
  QLearnerGameAI<Game, GameState, Action, QPair, QLearnerMap> gameAI_;
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
      const Action& move = player->play(state);
      state = takeAction(move);
      turn += 1;
    }
    displayGameEnd(state);
  }

  virtual const GameState startNewGame();
  virtual const GameState takeAction(const Action& action);
  virtual void displayBoard(const GameState& state) const;
  virtual void displayGameEnd(const GameState& state) const;
  bool isGameRunning = false;
};
