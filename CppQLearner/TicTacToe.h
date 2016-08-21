#include <vector>
#include <unordered_map>
#include <array>

#include "GameSetup.h"

typedef std::array<std::vector<int>, 2> GameState;
typedef int Action;
typedef std::tuple<const GameState, const Action> QPair;

namespace std {
  template <>
  struct hash<QPair>
  {
    std::size_t operator()(const QPair& k) const
    {
      using std::size_t;
      const auto moves = std::get<0>(k);
      const auto action = std::get<1>(k);
      size_t s = 0x31aebe2d;
      for (const auto& playerMoves : moves) {
        for (const auto& move : playerMoves) {
          s = (s >> 1) | (s << (sizeof(size_t) * 8 - 1));
          s ^= move * 0xaf6b3801;
        }
      }
      s *= 0xaf6b3801;
      s ^= s >> 16;
      s ^= action;

      return (s);
    }
  };
}

typedef std::unordered_map<QPair, double> QLearnerMap;

class TicTacToe : public Game<GameState, Action> {
public:
  TicTacToe()
  {

  }

  virtual void playGame(std::vector<std::shared_ptr<Player<GameState, Action>>> players) {
    Game::playGame(players);
  }

  const GameState startNewGame();
  const GameState takeAction(const Action& action);

  const std::vector<Action> actions(const GameState& state) const;
  const GameState transition(const GameState& state, const Action& action) const;
  const double reward(const GameState& state, const Action& prevMove) const;

  const bool checkWin(const GameState& state, const int& player) const;
  const bool checkTie(const GameState& state) const;
  const int checkGameOver(const GameState& state, const Action& prevMove) const;

  const std::string getBoard(const GameState& state) const;
  void displayBoard(const GameState& state) const;
  void displayGameEnd(const GameState& state) const;
  void displayQPair(const GameState& state, const Action& action) const;
  const Action getPlayerMove(const GameState& state) const;

  GameState state_;
  int players = 2;
};
