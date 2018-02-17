"""Methods for finding anonymization sequences."""
from operation import Operation
from policy import Policy
from unification import unify,var
from util import decompose_triple

def find_candidate_unitaryP(privacy_pol, utility_pol, counters):
    """
        Find a candidate sequence of anonymization operations to process a
        graph while satisfying the given policies, with an unitary privacy policy.

        :requires: privacy_pol.queries.len = 1
    """
    ops = []
    for c in privacy_pol.queries[0].where:
        # Triple decomposition
        (s,p,o) = decompose_triple(c)
        #print "Privacy triple to be unified:" + str((s,p,o))
        counters[1] += 1
        # Main algorithm
        flag = True
        for Q_u in utility_pol.queries:
            for c_u in Q_u.where:
                (s_u, p_u, o_u) = decompose_triple(c_u)
                if unify((s, p, o), (s_u, p_u, o_u)) != False:
                    print "\t" + str((s,p,o)) + " unified with " + str((s_u,p_u,o_u))
                    if flag:
                        counters[0] += 1
                    flag = False
        if flag:
            ops.append(Operation([c], privacy_pol.queries[0].where))
    return ops

def find_candidate_general(privacy_pol, utility_pol, counters):
    """
        Find a candidate sequence of anonymization operations to process a
        graph while satisfying the given policies.

        :requires: privacy_pol.queries.len > 1
    """
    ops = []
    ind = 0
    for q in privacy_pol.queries:
        print "\tPrivacy policy query found..."
        ind += 1
        ops_i = find_candidate_unitaryP(Policy([q], "P"), utility_pol, counters)
        if not ops_i:
            return []
        else:
            new_op_seqs = []
            if not ops:
                for new_op in ops_i:
                    ops.append([new_op])
            else:
                for old_op_seq in ops:
                    for new_op in ops_i:
                        old_op_seq.append(new_op)
                        new_op_seqs.append(old_op_seq)
                ops = new_op_seqs

    return ops


def find_optimal(privacy_pol, utility_pol, metric):
    """Find the best sequence of anonymization operations, using a given comparison
    metric, to process the given graph while satisfying the given policies."""
    # TODO
    pass
