#ifndef QLearner_h
#define QLearner_h

#include <unordered_map>
#include <random>
#include <chrono>
#include <functional>
#include <tuple>
#include <iostream>

/**
 * QLearner provides the basic QLearning algorithm to its derived classes.
 */
template<class Game, typename State, typename Action, typename QPair, typename QLearnerMap>
class QLearner {
  typedef std::tuple<const Action, const double> BestQTuple;

public:
  QLearner(
    Game& game,
    double alpha,
    double epsilon,
    double gamma
  ) :
    game_(game),
    alpha_(alpha),
    epsilon_(epsilon),
    gamma_(gamma)
  {
    uint64_t timeSeed = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    std::seed_seq ss{uint32_t(timeSeed & 0xffffffff), uint32_t(timeSeed>>32)};
    rng_.seed(ss);
  }

protected:
  QLearnerMap Q_;
  double alpha_;
  double epsilon_;
  double gamma_;
  Game& game_;


  /* Used for generating randomness */
  std::mt19937_64 rng_;

  /**
   * Returns the Q value for a given pair in the Q value map.
   */
  const double getQ(const QPair qPair) {
    auto it = Q_.find(qPair);
    if (it != Q_.end()) {
      return it->second;
    }

    double defaultValue = 0.0;
    Q_.emplace(qPair, defaultValue);
    return defaultValue;
  }

  /**
   * Given a game state, returns the best action known so far as well as its
   * Q value.
   */
  BestQTuple bestQ(const State& state) {
    const auto actions = game_.actions(state);
    if (actions.empty()) {
      return std::make_tuple(0, 0.0);
    }

    std::uniform_int_distribution<> dis(0, actions.size() - 1);

    auto maxAction = actions[dis(rng_)];
    double maxQ = getQ(std::make_tuple(state, maxAction));

    for (const auto action : actions) {
      const QPair qPair = std::make_tuple(state, action);
      const double curQ = getQ(qPair);
      if (curQ > maxQ) {
        maxAction = action;
        maxQ = curQ;
      }
    }

    return std::make_tuple(maxAction, maxQ);
  }

  /**
   * Explores an action for a given state and updates the Q value map
   * accordingly.
   */
  void updateQ(const State& state, const Action& action) {
    const auto newState = game_.transition(state, action);
    const QPair qPair = std::make_tuple(state, action);
    const double qValue = getQ(qPair);
    const double maxQ = std::get<1>(bestQ(newState));
    const double qUpdate = game_.reward(newState, action) - gamma_ * maxQ - qValue;
    const double newQValue = qValue + alpha_ * qUpdate;
    Q_[qPair] = newQValue;
  }

  /**
   * Explores a state by either taking a random move with prob. epsilon or
   * a learned move with prob. 1-epsilon
   */
   const Action exploreState(const State& state) {
     std::uniform_real_distribution<double> unif(0, 1);
     const auto& rand = unif(rng_);

     const auto actions = game_.actions(state);

     Action action;
     if (rand < epsilon_) {
       const auto actions = game_.actions(state);
       std::uniform_int_distribution<> dis(0, actions.size() - 1);
       action = actions[dis(rng_)];
     } else {
       action = std::get<0>(bestQ(state));
     }
     updateQ(state, action);
     return action;
   }
};

template<class Game, typename GameState, typename Action, typename QPair, typename QLearnerMap>
class QLearnerGameAI : public QLearner<Game, GameState, Action, QPair, QLearnerMap> {
public:
  QLearnerGameAI(Game& game, double alpha, double epsilon, double gamma) :
    QLearner<Game, GameState, Action, QPair, QLearnerMap>(
      game, alpha, epsilon, gamma
    ),
    game_(game)
  {

  }

  bool isGameRunning = false;
  int numGamesLearned = 0;

  const Action& learnedMove(const GameState& state) {
    return std::get<0>(this->bestQ(state));
  }

  void learnSteps(const int& numSteps) {
    auto state = game_.startNewGame();
    for(int64_t i = 0; i < numSteps; i++) {
      const auto& action = this->exploreState(state);
      state = game_.takeAction(action);
      if (!isGameRunning) {
        numGamesLearned++;
        state = game_.startNewGame();
      }
    }
  }

  void learnGames(const int& numGames) {
    for (int64_t i = 0; i < numGames; i++) {
      auto state = game_.startNewGame();
      while (game_.isGameRunning) {
        const auto& action = this->exploreState(state);
        state = game_.takeAction(action);
      }

      numGamesLearned++;
    }
  }

private:
  Game game_;
};
#endif
