"""Utility methods."""
import sys
import os
from unification import var

def block_print():
    """Disable printing for faster display"""
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    """Enable print for debugging"""
    sys.stdout = sys.__stdout__

def decompose_triple(t):
    """Extract the three parts of an RDF triple string"""
    s_str = t.split(" ")[0]
    p_str = t.split(" ")[1]
    o_str = t.split(" ")[2]
    if s_str[0] == '?':
        s = var(s_str[1:])
    else:
        s = s_str
    if p_str[0] == '?':
        p = var(p_str[1:])
    else:
        p = p_str
    if o_str[0] == '?':
        o = var(o_str[1:])
    else:
        o = o_str

    return (s,p,o)

def replace_blank(t, ind):
    """Replace one element of an RDF triple string by a blank node"""
    t_tab = t.split(" ")
    t_tab[ind] = ("[]")
    return " ".join(t_tab)
    
def average_wl_size(workload):
    """Compute (integer) average size (in triples) of a query workload"""
    return int(sum(len(query.where) for query in workload) / float(len(workload)))