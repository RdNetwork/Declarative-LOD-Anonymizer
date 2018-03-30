"""Methods for finding anonymization sequences."""
from operation import Operation
from policy import Policy
from unification import unify,var
from util import decompose_triple, replace_blank

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
            # Deletion operation
            ops.append(Operation([c], None, privacy_pol.queries[0].where))

            # Update operation #1
            for c_1 in privacy_pol.queries[0].where:
                (s_1, p_1, o_1) = decompose_triple(c_1)
                if ((s_1, p_1, o_1) == (s_1, p_1, s) or
                   ((s_1, p_1, o_1) == (s, p_1, o_1) and (not unify((s, p, o), (s, p_1, o_1)))) or
                   ('?'+str(s)) in privacy_pol.queries[0].select):
                    c_blank = replace_blank(c, 0)
                    ops.append(Operation([c], [c_blank], privacy_pol.queries[0].where))
                    break

            # Update operation #2
            for c_2 in privacy_pol.queries[0].where:
                (s_2, p_2, o_2) = decompose_triple(c_2)
                if ((s_2, p_2, o_2) == (o, p_2, s_2) or
                 ((s_2, p_2, o_2) == (s_2, p_2, o) and (not unify((s, p, o), (s_2, p_2, o)))) or
                   ('?'+str(s)) in privacy_pol.queries[0].select):
                    c_blank = replace_blank(c, 2)
                    ops.append(Operation([c], [c_blank], privacy_pol.queries[0].where))       
                    break         
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
