def viterbi(evidence_vector, prior, states, evidence_variables, transition_probs, emission_probs):

    # initialize
    viterbi_most_likely_state_sequence = [None] * evidence_vector.__len__()
    evidence_probability_list = []
    trellis_probability = []
    prior_distribution = prior.copy()

    for evidence in evidence_vector:
        if evidence_variables[0] in evidence:
            note = evidence[evidence_variables[0]]

        # initialize state dict with lists of tuple
        state_probability_dict = {}
        for state in states:
            state_probability_dict[state] = [], []

        for state in states:
            highest_prob_backtrack = {}

            if state in prior_distribution:
                state_prior = prior_distribution[state]
            else:
                state_prior = 0.0

            if state in transition_probs:
                state_transition_probs_dict = transition_probs[state]
                if state in state_transition_probs_dict:
                    state_transition_prob = state_transition_probs_dict[state]
                else:
                    state_transition_prob = 0.0

            if state in emission_probs:
                emission_probs_dict = emission_probs[state]
                if evidence_variables[0] in emission_probs_dict:
                    emission_probs_list = emission_probs_dict[evidence_variables[0]]
                    state_emission_prob = emission_probs_list[note]

            state_probability = state_prior * state_transition_prob * state_emission_prob

            state_probability_list, state_probability_source = state_probability_dict[state]
            state_probability_list.append(state_probability)
            state_probability_source.append(state)
            state_probability_dict[state] = state_probability_list, state_probability_source

            # find transitive states from this state
            for key, value in state_transition_probs_dict.iteritems():
                if state != key and value != 0:
                    transitive_state = key
                    transitive_state_transition_prob = value
                    transitive__emission_probs_dict = emission_probs[transitive_state]
                    if evidence_variables[0] in emission_probs_dict:
                        transitive__emission_probs_list = transitive__emission_probs_dict[evidence_variables[0]]
                        transitive__state_emission_prob = transitive__emission_probs_list[note]
                    if state in prior_distribution:
                        transitive_state_prior = prior_distribution[state]
                    else:
                        transitive_state_prior = 0.0

                    transitive_state_probability = transitive_state_prior * transitive_state_transition_prob * transitive__state_emission_prob

                    transitive_state_probability_list, state_probability_source = state_probability_dict[transitive_state]
                    transitive_state_probability_list.append(transitive_state_probability)
                    state_probability_source.append(state)
                    state_probability_dict[transitive_state] =  transitive_state_probability_list, state_probability_source

        last = prior_distribution.copy()
        # determine most likely state and re-set prior_distribution
        for key, value in state_probability_dict.iteritems():
            if key in prior_distribution:
                state_probability_list, state_probability_source = value
                highest_prob = max(state_probability_list)
                index_highest_prob = state_probability_list.index(highest_prob)
                # needed for backtracking
                highest_prob_source = state_probability_source[index_highest_prob]
                highest_prob_backtrack[key] = last[highest_prob_source]
                prior_distribution[key] = highest_prob

        calculated_prob_source =  prior_distribution.copy(), highest_prob_backtrack.copy()
        evidence_probability_list.append(calculated_prob_source)

        # for sanity check
        state_trellis = []
        for k, v in prior_distribution.iteritems():
            state_trellis.append(v)
        trellis_probability.append(state_trellis)

    # backtracking
    path_prob = None
    for index, evidence_probability in reversed(list(enumerate(evidence_probability_list))):
        highest_dict, backtrack_dict = evidence_probability
        # exit out of viterbi path is a special case with total probability of path
        if index == (evidence_probability_list.__len__() - 1):
            last_path_state = max(highest_dict.keys(), key=(lambda k: highest_dict[k]))
            path_prob = backtrack_dict[last_path_state]
            viterbi_most_likely_state_sequence[index] = last_path_state
        # entry into viterbi path is a special case with provided prior_distribution prob
        elif index == 0:
            first_path_state = max(highest_dict.keys(), key=(lambda k: highest_dict[k]))
            viterbi_most_likely_state_sequence[index] = first_path_state
        else:
            path_state = highest_dict.keys()[highest_dict.values().index(path_prob)]
            path_prob = backtrack_dict[path_state]
            viterbi_most_likely_state_sequence[index] = path_state

    # for checking correctness against hand drawn trellis
    print evidence_vector
    print trellis_probability
    print viterbi_most_likely_state_sequence
    print ""

    return viterbi_most_likely_state_sequence


avalanche_states = ('High', 'Low', 'End')
avalanche_evidence_variables = ('Note',)

avalanche_transition_probs = {
    'High': {'High': 0.6, 'Low': 0.4, 'End':0},
    'Low':  {'High': 0.4, 'Low': 0.5, 'End':0.1},
    'End':  {'High': 0,   'Low': 0,   'End':1}
}

avalanche_emission_probs = {
    'High' : {'Note':[0.1, 0.1, 0.4, 0.4]},
    'Low'  : {'Note':[0.4, 0.4, 0.1, 0.1]},
    'End'  : {'Note':[1e-4, 1e-4, 1e-4, 1e-4]}
}

prior = {'High':0.5, 'Low':0.5}


invasion_states = ('High', 'Mid', 'Low', 'End')
invasion_evidence_variables = ('Note',)


invasion_transition_probs = {
    'High': {'High': 0.6, 'Mid':0.4 , 'Low': 0, 'End':0},
    'Mid' : {'High': 0,  'Mid':0.7, 'Low': 0.3, 'End': 0  },
    'Low':  {'High': 0,   'Mid': 0,    'Low': 0.6, 'End':0.4},
    'End':  {'High': 0,   'Mid': 0,    'Low': 0,   'End':1}
}

invasion_emission_probs = {
    'High' : {'Note':[0.1, 0.1, 0.2, 0.6]},
    'Mid'  : {'Note':[0.1, 0.1, 0.7, 0.1]},
    'Low'  : {'Note':[0.6, 0.2, 0.1, 0.1]},
    'End'  : {'Note':[1e-4, 1e-4, 1e-4, 1e-4]}
}

invasion_prior = {'High':0.33, 'Mid':0.33, 'Low':0.33}

# D# D C# C C# D D# D C# C
evidence_sequence_1 = [{'Note':3}, {'Note':2}, {'Note':1},{'Note':0},{'Note':1},{'Note':2},{'Note':3},{'Note':2},{'Note':1},{'Note':0}]

invasion_state_sequence_1 = viterbi(evidence_sequence_1, invasion_prior, invasion_states, invasion_evidence_variables, invasion_transition_probs, invasion_emission_probs)
avalanche_state_sequence_1 = viterbi(evidence_sequence_1, prior, avalanche_states, avalanche_evidence_variables, avalanche_transition_probs, avalanche_emission_probs )

# D# D# D# D D D C# C C
evidence_sequence_2 = [{'Note':3}, {'Note':3}, {'Note':3},{'Note':2},{'Note':2},{'Note':2},{'Note':1},{'Note':0},{'Note':0}]

invasion_state_sequence_2 = viterbi(evidence_sequence_2, invasion_prior, invasion_states, invasion_evidence_variables, invasion_transition_probs, invasion_emission_probs)
avalanche_state_sequence_2 = viterbi(evidence_sequence_2, prior, avalanche_states, avalanche_evidence_variables, avalanche_transition_probs, avalanche_emission_probs )

# The following is an evidence sequence given as a test:

example_sequence = [{'Note':3}, {'Note':2}, {'Note':2},{'Note':1},{'Note':0}]

