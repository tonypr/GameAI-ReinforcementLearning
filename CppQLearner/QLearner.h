#ifndef QLearner_h
#define QLearner_h

#include <unordered_map>
#include <random>
#include <chrono>

/**
 * QLearner provides the basic QLearning algorithm to its derived classes.
 */
template<typename State, typename Action, typename QPair, typename QLearnerMap>
class QLearner {
  typedef std::tuple<const Action&, const double&> BestQTuple;
  typedef std::tuple<const Action&, const State&, const double&> LearnResults;

public:
  QLearner(double alpha, double epsilon, double gamma) :
    alpha_(alpha),
    epsilon_(epsilon),
    gamma_(gamma)
  {
    uint64_t timeSeed = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    std::seed_seq ss{uint32_t(timeSeed & 0xffffffff), uint32_t(timeSeed>>32)};
    rng_.seed(ss);
  }

protected:
  double alpha_;
  double epsilon_;
  double gamma_;
  QLearnerMap Q_;

  /* Used for generating randomness */
  std::mt19937_64 rng_;

  virtual const std::vector<Action>& getActions(const State& state) = 0;

  virtual
  const State& transition(const State& state, const Action& action) = 0;

  virtual
  const double& reward(const State& state, const Action& action) = 0;

  /**
   * Returns the Q value for a given pair in the Q value map.
   */
  const double getQ(const QPair& qPair) {
    if (Q_.find(qPair) == Q_.end()) {
      Q_[qPair] = 0;
    }
    return Q_[qPair];
  }

  /**
   * Given a game state, returns the best action known so far as well as its
   * Q value.
   */
  BestQTuple bestQ(const State& state) {
    const auto& actions = getActions(state);
    if (actions.empty()) {
      return std::make_tuple(0, 0);
    }

    auto maxAction = actions[0];
    auto maxQ = getQ(std::make_tuple(state, maxAction));

    for (const auto action : actions) {
      const auto curQ = getQ(std::make_tuple(state, action));
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
    const auto newState = transition(state, action);
    const auto qPair = std::make_tuple(state, action);
    const auto& maxQ = std::get<1>(bestQ(newState));
    const auto& qUpdate = reward(newState, action) - gamma_*maxQ - getQ(qPair);
    Q_[qPair] += alpha_ * qUpdate;
  }

  /**
   * Explores a state by either taking a random move with prob. epsilon or
   * a learned move with prob. 1-epsilon
   */
   const Action& exploreState(const State& state) {
     std::uniform_real_distribution<double> unif(0, 1);
     const auto& rand = unif(rng_);

     Action action;
     if (rand < epsilon_) {
       const auto& actions = getActions(state);
       std::uniform_int_distribution<> dis(0, actions.size() - 1);
       action = actions[dis(rng_)];
     } else {
       action = std::get<0>(bestQ(state));
     }
     updateQ(state, action);
     return action;
   }
};

template<typename GameState, typename Action, typename QPair, typename QLearnerMap>
class QLearnerGameAI : public QLearner<GameState, Action, QPair, QLearnerMap> {
public:
  QLearnerGameAI(double alpha, double epsilon, double gamma) :
    QLearner<GameState, Action, QPair, QLearnerMap>(alpha, epsilon, gamma)
  { }

  bool isGameRunning = false;
  int numGamesLearned = 0;

  virtual const GameState startNewGame() = 0;
  virtual const GameState takeAction(const Action& action) = 0;

  const Action& learnedMove(const GameState& state) {
    return std::get<0>(bestQ(state));
  }

  void learnSteps(const int& numSteps) {
    auto state = startNewGame();
    for(int64_t i = 0; i < numSteps; i++) {
      const auto& action = exploreState(state);
      const auto& state = takeAction(action);
      if (!isGameRunning) {
        numGamesLearned++;
        state = startNewGame();
      }
    }
  }

  void learnGames(const int& numGames) {
    for (int64_t i = 0; i < numGames; i++) {
      auto state = startNewGame();

      while (isGameRunning) {
        const auto& action = exploreState(state);
        const auto& state = takeAction(action);
      }

      numGamesLearned++;
    }
  }
};
#endif
