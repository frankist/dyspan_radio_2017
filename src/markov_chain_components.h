/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   markov_chain_components.h
 * Author: connect
 *
 * Created on 05 February 2017, 19:44
 */
#include <cmath>
#include <tuple>
#include <utility>
#include <algorithm>
#include <boost/circular_buffer.hpp>
#include "matrix_utils.h"
#include "../utils/json.hpp"
#include "general_utils.hpp"

#ifndef MARKOV_CHAIN_COMPONENTS_H
#define MARKOV_CHAIN_COMPONENTS_H

using std::vector;

typedef double time_format;
typedef std::tuple<time_format,int,float> DetectedPacket;

class DeepLearningMarkovChain
{
public:
    Matrix<float> transition_probability;
    vector<float> state_probability;
    
    vector<float> tmp_prob;
    
    DeepLearningMarkovChain(size_t num_states, float diag_prob = 0.95);
    
    inline size_t n_states() const { return state_probability.size(); }
    
    void push(const vector<float>& deep_learning_beliefs);
    
    inline size_t current_state() const 
    {
        return ranges::argmax(state_probability);
    }
};

class DeepLearningModeCounter
{
public:
    DeepLearningModeCounter() = default;
    DeepLearningModeCounter(int buf_size, int num_scenarios = 10) : scenario_guesses(buf_size), counter_scenarios(num_scenarios,0)
    {
    }
    
    boost::circular_buffer<int8_t> scenario_guesses;
    vector<long> counter_scenarios;
    
    inline size_t n_states() const { return counter_scenarios.size(); }
    
    void push(int8_t scenario);
    
    inline int8_t current_state() const
    {
        return ranges::argmax(counter_scenarios);
    }
};

namespace markov_utils
{
inline DeepLearningModeCounter make_deeplearning_mode_counter(float time_window, float spectrogram_duration, int num_scenarios = 10)
{
    assert(round(time_window/spectrogram_duration)>1);
    return {(int)round(time_window/spectrogram_duration),num_scenarios};
}
};

//struct PacketObservation
//{
//    time_format tdelay;
//    float snr;
//    PacketObservation(time_format t, float s) : tdelay(t), snr(s) {}
//    PacketObservation() = default;
//};
//
//class AbstractChannelMarkovChain
//{
//public:
//    AbstractChannelMarkovChain(const std::pair<PacketObservation,PacketObservation>& vrange, const PacketObservation& qstep) : 
//            val_range(vrange), quantization_step(qstep), 
//            n_pwr_steps(std::floor((vrange.second.snr-vrange.first.snr)/qstep.snr)+1),
//            n_time_steps(std::floor((vrange.second.tdelay-vrange.first.tdelay)/qstep.tdelay)+1), prev_packet(std::make_tuple(-1,-1,-1))
//    {
//    }
//    
//    inline int n_observations() const {return n_pwr_steps*n_time_steps + 1;} // last for observed packet in another channel
//    virtual void register_packet(const DetectedPacket& p) = 0;
//    virtual void register_no_packet() = 0;
//    inline int get_idx(const PacketObservation& p) const 
//    {
//        int tidx = std::min(std::max((int)std::round((p.tdelay-val_range.first.tdelay) / quantization_step.tdelay),0), n_time_steps-1);
//        int fidx = std::min(std::max((int)std::round((p.snr-val_range.first.snr) / quantization_step.snr),0), n_pwr_steps-1);
//        int idx = tidx + fidx*n_time_steps;
//        return idx;
//    }
//    
//    std::pair<PacketObservation,PacketObservation> val_range;
//    PacketObservation quantization_step;
//    int n_pwr_steps;
//    int n_time_steps;
//    DetectedPacket prev_packet;
//    // probability of staying in the same scenario is 1 (not really a MC)
//};
//
//class LearningMarkovChain;
//
//class ChallengeMarkovChain : public AbstractChannelMarkovChain
//{
//public:
//    ChallengeMarkovChain(const std::pair<PacketObservation,PacketObservation>& vrange, const PacketObservation& qstep) : 
//        AbstractChannelMarkovChain(vrange, qstep), prob_emission(n_observations())
//    {}
//    ChallengeMarkovChain(const LearningMarkovChain& m);
//    
//    void register_packet(const DetectedPacket& p) final;
//    void register_no_packet() final;
//    
//    float state_probability = 1;
//    std::vector<float> prob_emission;
//};
//
//class LearningMarkovChain : public AbstractChannelMarkovChain
//{
//public:
//    LearningMarkovChain(const std::pair<PacketObservation,PacketObservation>& vrange, const PacketObservation& qstep) : 
//        AbstractChannelMarkovChain(vrange, qstep), n_hits(n_observations())
//    {}
//    
//    void register_packet(const DetectedPacket& p) final;
//    void register_no_packet() final;
//    float probability(const PacketObservation& p) const 
//    {
//        int i = get_idx(p);
//        return (float)(n_hits[i] / (double)total_packets);
//    }
//    
//    std::vector<long> n_hits;
//    long total_packets = 0;
//};
//
//class MarkovChainLearner
//{
//public:
//    MarkovChainLearner(int n_channels, const std::pair<PacketObservation,PacketObservation>& vrange, const PacketObservation& qstep) : 
//            Nch(n_channels), 
//            mc_vec(n_channels, LearningMarkovChain(vrange, qstep)) 
//    {
//    }
//    
//    void work(std::vector<DetectedPacket>& q_packets);
//    
//    int Nch;
//    std::vector<LearningMarkovChain> mc_vec;
//};
//
//class CombinatorialMarkovChain
//{
//public:
//    CombinatorialMarkovChain(int n_channels, int n_occupied, const std::vector<LearningMarkovChain>& mc_learned);
//    
//    void work(std::vector<DetectedPacket>& q_packets);
//    std::pair<float, std::vector<int> > state_probability();
//    
//    int Nch;
//    int num_occupied;
//    bool multi_hypothesis;
//    std::vector<std::vector<bool> > combinations;
//    std::vector<ChallengeMarkovChain> mc_combinations;
//};
//
//namespace markov_utils
//{
//    nlohmann::json to_json(const LearningMarkovChain& m);
//    LearningMarkovChain from_json(nlohmann::json& j);
//    nlohmann::json to_json(const MarkovChainLearner& l);
//};

#endif /* MARKOV_CHAIN_COMPONENTS_H */

