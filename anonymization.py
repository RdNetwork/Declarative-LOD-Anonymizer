"""Methods for finding anonymization sequences."""
from operation import Operation
from policy import Policy
from unification import unify,var,variable
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
            # If one policy query returned no results, then this privacy policy
            # cannot be satisfied => return empty
            return []
        else:
            
            new_op_seqs = []
            if not ops:
                for new_op in ops_i:
                    ops.append([new_op])
            else:
                for old_op_seq in ops:
                    for new_op in ops_i:
                        backup_old_op_seq = list(old_op_seq)
                        old_op_seq.append(new_op)
                        new_op_seqs.append(old_op_seq)
                        old_op_seq = list(backup_old_op_seq)
                ops = new_op_seqs

    return ops


def find_safe_ops(privacy_pol):
    """Compute the set of operations to create a safe anonymization."""
    ops = []
    for q in privacy_pol.queries:
        print "\tPrivacy policy query found..."
        ind_l = {}
        ind_v = {}
        for c in q.where:
            b_index = 0
            (s,p,o) = decompose_triple(c)
            if (type(s) == variable.Var) or (':' in s):
                if (type(s) == variable.Var):
                    s = str(s)[1:]
                if not s in ind_v:
                    ind_v[s] = set()
                ind_v[s].add(c)
            if (type(p) == variable.Var) or (':' in p):
                if (type(p) == variable.Var):
                    p = str(p)[1:]
                if not p in ind_v:
                    ind_v[p] = set()
                ind_v[p].add(c)
            if (type(o) == variable.Var) or (':' in o):
                if (type(o) == variable.Var):
                    o = str(o)[1:]
                if not o in ind_v:
                    ind_v[o] = set()
                ind_v[o].add(c)
            else:
                if not o in ind_l:
                    ind_l[o] = set()
                ind_l[o].add(c)
        # print("Subgraphs for each variable and IRI:")
        # print(ind_v)
        # print("Subgraphs for each literal:")
        # print(ind_l)
        v_crit = set([v[1:] for v in q.select])
        for v,g in ind_v.iteritems():
            if len(g) > 1:
                v_crit.add(v)
        print("Critical terms: " + str(v_crit))
        g_prime = q.where
        for v in v_crit:
            print(v)
            v = '?' + v
            g_prime_post = []
            for t in g_prime:
                t_int = t.replace(v+" ","_:b"+str(b_index)+" ")
                g_prime_post.append(t_int.replace(" "+v," _:b"+str(b_index)))
            b_index += 1
            g_prime = g_prime_post
        if not g_prime == q.where:
            if len(q.select) == 0:
                # case of a boolean query: pick the first triple and delete it
                ops.append(Operation([c], None, q.where))
            else:
                ops.append(Operation(q.where, g_prime, q.where))
        g_prime = []
        l_crit = set()
        for l,g in ind_l.iteritems():
            if len(g) > 1:
                l_crit.add(l)    
        for l in l_crit:
            for t in ind_l[l]:
                (s_l,p_l,_) = decompose_triple(t)
                if s_l not in v_crit and p_l not in v_crit:
                    g_prime.append(t)
        if g_prime:
            ops.append(Operation(g_prime, None, g_prime))
    return ops
