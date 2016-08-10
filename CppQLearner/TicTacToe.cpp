#include <vector>

#include "QLearner.h"

typedef int Action;
typedef std::vector<int> State;
typedef std::tuple<const State&, const Action&> QPair;

struct key_hash : public std::unary_function<QPair, std::size_t> {
  std::size_t operator()(const QPair& qPair) const {
    return 1;
    // auto gameState = std::get<0>(qPair);
    // auto action = std::get<1>(qPair);
    // size_t s = 0x3a7eb429; // Just some random seed value
    // for (int i = 0; i != 7; ++i) {
    //     for (int j = 0; j != 6; ++j) {
    //         s = (s >> 1) | (s << (sizeof(size_t) * 8 - 1));
    //         s ^= gameState[i][j] * 0xee6b2807;
    //     }
    // }
    // s *= 0xee6b2807;
    // s ^= s >> 16;
    // s ^= action;
    // return s;
  }
};

struct key_equal : public std::binary_function<QPair, QPair, bool> {
  bool operator() (const QPair& v0, const QPair& v1) const {
    return (
      std::get<0>(v0) == std::get<0>(v1) &&
      std::get<1>(v0) == std::get<1>(v1)
    );
  }
};
typedef std::unordered_map<const QPair&, const double&, key_hash, key_equal> QLearnerMap;
// class TicTacToeGame : public QLearnerGameAI<State, Action, key_hash, key_equal> {
//
//
// };
