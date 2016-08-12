#include <vector>
#include <unordered_map>

#include "QLearner.h"

typedef std::vector<std::vector<int>> GameState;
typedef int Action;
typedef std::tuple<const GameState&, const Action&> QPair;

namespace std {
  template <>
  struct hash<QPair>
  {
    std::size_t operator()(const QPair& k) const
    {
      using std::size_t;
      using std::hash;

      // Compute individual hash values for first,
      // second and third and combine them using XOR
      // and bit shifting:

      return (1);
    }
  };
}

typedef std::unordered_map<QPair, Action> QLearnerMap;

class TicTacToe : public QLearnerGameAI<GameState, Action, QPair, QLearnerMap> {
public:
  TicTacToe(double alpha, double epsilon, double gamma) :
    QLearnerGameAI<GameState, Action, QPair, QLearnerMap>(alpha, epsilon, gamma)
  { }

  const GameState startNewGame();
  const GameState takeAction(const Action& action);
};
