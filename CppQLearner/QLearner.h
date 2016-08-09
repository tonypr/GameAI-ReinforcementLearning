#ifndef QLearner_h
#define QLearner_h

#include <unordered_map>
#include <random>
#include <chrono>

/**
 * QLearner provides the basic QLearning algorithm to its derived classes.
 */
template<typename GameState, typename Action, class key_hash, class key_equal>
class QLearner {
  typedef std::tuple<const GameState&, const Action&> QPair;
  typedef std::tuple<const Action&, const double&> BestQTuple;
  typedef std::tuple<const Action&, const GameState&, const double&> LearnResults;
  typedef std::unordered_map<const QPair&, const double&, key_hash, key_equal> QLearnerMap;

public:
  QLearner(
    GameState start, double alpha, double epsilon, double gamma
  ) :
    alpha_(alpha),
    epsilon_(epsilon),
    gamma_(gamma),
    startState_(start) {
      uint64_t timeSeed = std::chrono::high_resolution_clock::now().time_since_epoch().count();
      std::seed_seq ss{uint32_t(timeSeed & 0xffffffff), uint32_t(timeSeed>>32)};
      rng_.seed(ss);
    }

protected:
  double alpha_;
  double epsilon_;
  double gamma_;
  QLearnerMap Q_;
  GameState startState_;

  /* Used for generating randomness */
  std::mt19937_64 rng_;

  virtual const std::vector<Action> getActions(const GameState& state);
  virtual const GameState transition(const GameState& state, const Action& action);
  virtual const double reward(const GameState& state, const Action& action);

  /**
   * Returns the Q value for a given pair in the Q value map.
   */
  const double getQ(const QPair& qPair) {
    auto qPairIt = Q_.find(qPair);
    if (qPairIt == Q_.end()) {
      Q_[qPair] = 0;
    }
    return Q_[qPair];
  }

  /**
   * Given a game state, returns the best action known so far as well as its
   * Q value.
   */
  BestQTuple bestQ(const GameState& state) {
    auto actions = getActions(state);
    if (actions.empty()) {
      return std::make_tuple<Action, double>(0, 0);
    }

    auto maxAction = actions[0];
    const auto qPair = std::make_tuple<const GameState&, const Action&>(state, maxAction);
    auto maxQ = getQ(qPair);
    for (const auto& action : actions) {
      const auto tempQPair =
        std::make_tuple<const GameState&, const Action&>(state, action);
      const auto curQ = getQ(tempQPair);

      if (curQ > maxQ) {
        maxAction = action;
        maxQ = curQ;
      }
    }

    return std::make_tuple<const Action&, const double&>(maxAction, maxQ);
  }

  /**
   * Explores an action for a given state and updates the Q value map
   * accordingly.
   * Returns the reward of the new state.
   */
  const double updateQ(const GameState& state, const Action& action) {
    auto newState = transition(state, action);
    auto qReward = reward(newState, action);
    auto qPair = std::make_tuple<const GameState&, const Action&>(state, action);
    auto qValue = getQ(qPair);
    auto qUpdate = qReward - gamma_* std::get<1>(bestQ(newState)) - qValue;
    Q_[qPair] += alpha_ * qUpdate;
    return qReward;
  }

  /**
   * Takes one learning step on a given state.
   * Returns a tuple of:
   *    - the action explored
   *    - the new state transitioned to
   *    - the reward from the new state
   */
   LearnResults learn(const GameState& state) {
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
     const auto& newState = transition(state, action);
     const auto& reward = updateQ(state, action);
     return std::make_tuple<const Action&, const GameState&, const double&>(
       action,
       newState,
       reward
     );
   }
};

template<typename GameState, typename Action, class key_hash, class key_equal>
class QLearnerGameAI : public QLearner<GameState, Action, key_hash, key_equal> {
public:
  QLearnerGameAI(
    GameState start, double alpha, double epsilon, double gamma
  ) :
    QLearner<GameState, Action, key_hash, key_equal>(start, alpha, epsilon, gamma),
    numGamesLearned_(0)
  { }

  const Action& learnedMove(const GameState& state) {
    return std::get<0>(bestQ(state));
  }

  void learnSteps(const int& stepCount) {
    GameState state = this->startState_;
    for(int i = 0; i < stepCount; i++) {
      Action action;
      double reward;
      std::tie(action, state, reward) = learn(state);

      bool win = std::abs(reward) == 1;
      bool tie = getActions(state).size() == 0;
      if (tie || win) {
        state = this->startState_;
      }
    }
  }

  void learnGames(const int& gameCount) {
    GameState state;
    Action action;
    double reward;

    for (int i = 0; i < gameCount; i++) {
      bool gameNotFinished = false;
      state = this->startState_;
      while (gameNotFinished) {
        std::tie(action, state, reward) = learn(state);

        // Check if game finished
        bool win = std::abs(reward) == 1;
        bool tie = getActions(state).size() == 0;
        gameNotFinished = !(tie || win);
      }
      numGamesLearned_++;
    }
  }

private:
  int numGamesLearned_;
};
#endif
