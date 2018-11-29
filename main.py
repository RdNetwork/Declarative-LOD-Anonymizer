"""Main execution module."""
import random
import shutil
import os
import sys
import csv
import time
from rdflib import Graph
from policy import Policy
from query import Query
from anonymization import find_candidate_general, find_safe_ops
from prefix import Prefix
from util import block_print, enable_print, average_wl_size

GMARK_QUERIES = 500

def custom_prefixes():
    "Generating RDF prefixes used in our framework."
    p = []
    p.append(Prefix("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
    p.append(Prefix("rdfs", "http://www.w3.org/2000/01/rdf-schema#"))
    p.append(Prefix("owl", "http://www.w3.org/2002/07/owl#"))
    p.append(Prefix("xsd", "http://www.w3.org/2001/XMLSchema#"))
    p.append(Prefix("dc", "http://purl.org/dc/elements/1.1/"))
    p.append(Prefix("dcterms", "http://purl.org/dc/terms/"))
    p.append(Prefix("foaf", "http://xmlns.com/foaf/0.1/"))
    p.append(Prefix("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#"))
    p.append(Prefix("datex", "http://vocab.datex.org/terms#"))
    p.append(Prefix("lgdo", "http://linkedgeodata.org/ontology/"))
    p.append(Prefix("tcl", "http://localhost/"))
    p.append(Prefix("gld", "http://data.grandlyon.com/"))
    p.append(Prefix("skos", "http://www.w3.org/2004/02/skos/core#"))
    p.append(Prefix("gtfs", "http://vocab.gtfs.org/terms#"))
    return p


def main():
    """Main execution function."""
    STAT = False            #Stats mode: looping 7000 executions
    TEST = False            #Test mode: no anonymiation after algorithms execution
    DEMO = False            #Demo mode: fixed gmark policies, simple example
    DEMO_TXT = False        #Textual mode: import queries from text files rather than gmark output
    STAT_HISTO_P = False    #Generates stats with fixed privacy size
    STAT_HISTO_U = False    #Generates stats with fixed utility size
    SAFETY = False          #Generates operations preventing safety rather than candidates for privacy

    if "-s" in sys.argv:
        SAFETY = True

    if "-dt" in sys.argv:
        print "Running in textual demo mode: reading policies textfiles..."
        DEMO_TXT = True
        p_pol_size = int(sys.argv[1])
        u_pol_size = int(sys.argv[2])
    if "-d" in sys.argv:
        print "Running in demo mode: simple fixed policies used."
        DEMO = True
        p_pol_size = 2
        u_pol_size = 2
    else:
        p_pol_size = int(sys.argv[1])
        u_pol_size = int(sys.argv[2])
        if "-s" in sys.argv[3:]:
            print "Running in stats mode: 7000 executions looped."
            STAT = True
        if "-t" in sys.argv[3:]:
            print "Running in test mode: no graph anonymisation after computing sequences."
            TEST = True
        if "-hu" in sys.argv[3:]:
            print "Running in histogram (utility fixed) mode: 1400 executions looped."
            STAT_HISTO_U = True
        if "-hp" in sys.argv[3:]:
            print "Running in histogram (privacy fixed) mode: 1400 executions looped"
            STAT_HISTO_P = True


    if STAT:
        stats = []
        NB_EXPERIMENTS = 7000
    elif STAT_HISTO_U or STAT_HISTO_P:
        stats = []
        NB_EXPERIMENTS = 1400
    else:
        NB_EXPERIMENTS = 1

    # Fetching gmark queries
    #   DEMO uses a simple workload with 2 short queries.
    print "Fetching query workload..."
    if DEMO:
        workload = Query.parse_gmark_queries("./conf/workloads/demo.xml")
    elif DEMO_TXT:
        workload = Query.parse_txt_queries(p_pol_size, u_pol_size)
    else:
        workload = Query.parse_gmark_queries("./conf/workloads/star-starchain-workload.xml")

    avg = average_wl_size(workload) * 3

    if STAT_HISTO_U or STAT_HISTO_P:
        # Counters for histogram distribution
        min_histo = max(avg - 3, 1)
        max_histo = min_histo + 6
        print "Histogram bounds: " + str(min_histo) + "," + str(max_histo)
        if STAT_HISTO_U:
            histo_p = {}
            for i in range(min_histo, max_histo+1):
                histo_p.update({i: 0})
        if STAT_HISTO_P:
            histo_u = {}
            for i in range(min_histo, max_histo+1):
                histo_u.update({i: 0}) 

    for _ in range(0, NB_EXPERIMENTS):
        # Cleanup
        if (STAT or TEST or STAT_HISTO_P or STAT_HISTO_U):
            block_print()

        if DEMO or DEMO_TXT:
            p_pol = Policy([workload[0], workload[1]], "P")
            p_pol_nums = [0, 1]
            u_pol = Policy([workload[2], workload[3]], "U")
            u_pol_nums = [2, 3]
        else:
            # Creating random seed...
            seed = random.randrange(sys.maxsize)
            random.seed(seed)

            print "Random generator seed: " + str(seed)
            print "Defining policies:"
            # Create privacy policies
            print "\tDefining privacy policy..."
            if STAT_HISTO_U:
                FULL_P = set()
                while True:
                    total_size = 0
                    p_pol = Policy([], "P")
                    p_pol_nums = []
                    for _ in range(0, p_pol_size):
                        q_num = random.randint(0, GMARK_QUERIES-1)
                        p_pol.queries.append(workload[q_num])
                        p_pol_nums.append(q_num)
                        total_size += len(workload[q_num].where)
                    if (total_size <= max_histo) and (total_size >= min_histo):
                        if histo_p[total_size] < (NB_EXPERIMENTS / 7):
                            histo_p[total_size] += 1
                            break
                        else:
                            FULL_P.add(total_size)
                            if len(FULL_P) == 7:
                                break
            elif STAT_HISTO_P:
                while True:
                    total_size = 0
                    p_pol = Policy([], "P")
                    p_pol_nums = []
                    for _ in range(0, p_pol_size):
                        q_num = random.randint(0, GMARK_QUERIES-1)
                        p_pol.queries.append(workload[q_num])
                        p_pol_nums.append(q_num)
                        total_size += len(workload[q_num].where)
                    if total_size == avg:
                        break
            else:
                p_pol = Policy([], "P")
                p_pol_nums = []
                for _ in range(0, p_pol_size):
                    q_num = random.randint(0, GMARK_QUERIES-1)
                    p_pol.queries.append(workload[q_num])
                    p_pol_nums.append(q_num)

            # Create utility policies
            print "\tDefining utility policy..."
            if STAT_HISTO_P:
                FULL_U = set()
                while True:
                    total_size = 0
                    u_pol = Policy([], "U")
                    u_pol_nums = []
                    for _ in range(0, u_pol_size):
                        q_num = random.randint(0, GMARK_QUERIES-1)
                        u_pol.queries.append(workload[q_num])
                        u_pol_nums.append(q_num)
                        total_size += len(workload[q_num].where)
                    if (total_size <= max_histo) and (total_size >= min_histo) and (q_num not in p_pol_nums):
                        if histo_u[total_size] < (NB_EXPERIMENTS / 7):
                            break
                        else:
                            FULL_U.add(total_size)
                            if FULL_U == 7:
                                break
                histo_u[total_size] += 1
            elif STAT_HISTO_U:
                while True:
                    total_size = 0
                    u_pol = Policy([], "U")
                    u_pol_nums = []
                    for _ in range(0, u_pol_size):
                        q_num = random.randint(0, GMARK_QUERIES-1)
                        u_pol.queries.append(workload[q_num])
                        u_pol_nums.append(q_num)
                        total_size += len(workload[q_num].where)
                    if total_size == avg:
                        break
            else:
                u_pol = Policy([], "U")
                u_pol_nums = []
                for _ in range(0, u_pol_size):
                    while True:
                        q_num = random.randint(0, GMARK_QUERIES-1)
                        if q_num not in p_pol_nums:
                            break
                    u_pol.queries.append(workload[q_num])
                    u_pol_nums.append(q_num)


        print "\t\tChosen privacy queries: " + str(p_pol_nums)
        p_size = 0
        for i in range(0, p_pol_size):
            p_size += len(p_pol.queries[i].where)
            print "\t\t" + str(p_pol.queries[i])

        print "\t\tChosen utility queries: " + str(u_pol_nums)
        u_size = 0
        for i in range(0, u_pol_size):
            u_size += len(u_pol.queries[i].where)
            print "\t\t" + str(u_pol.queries[i])

        # Run algorithm
        print "Computing candidate operations..."
        if SAFETY: 
            print("SAFETY")
            o = find_safe_ops(p_pol)
            print(o)
            ops = [o]
        else:
            counters = [0, 0]
            ops = find_candidate_general(p_pol, u_pol, counters)
            print str(len(ops)) + ' operations found.'
            # old_ops = find_candidate_general(p_pol, u_pol, counters)
            # ops = set()
            # for seq in old_ops:
            #     sub_ops = set()
            #     for o_i in seq:
            #         sub_ops.add(o_i)
            #     sub_ops = frozenset(sub_ops)
            #     if sub_ops not in ops:
            #         ops.add(sub_ops)
        
        # Writing operations to result files
        op_id = 0
        for o in ops:
            with open('./out/op'+str(op_id)+'.txt', 'w+') as outfile:
                outfile.write(str(ops[op_id]))
                outfile.close()
                op_id += 1
        
        if not SAFETY:
            # Overlapping measures
            print str(counters[0]) + " triples overlapping out of " + str(counters[1]) + " privacy triples"
            measure = '{:.3%}'.format(float(counters[0]) / float(counters[1]))
            print "Overlapping value: " + str(measure)

        if ops and not TEST:    
            # Import graph
            print "Importing graph..."
            g = Graph()
            with open("./conf/graphs/graph.ttl", "r") as f:
                g.parse(file=f, format="turtle")
            print str(len(g)) + " triples found"

            print str(len(ops)) + " possible anonymization sequences found."
            print "Choose the sequence to be applied:"
            i = 0
            for i in (range(len(ops))):
                print "\t" + str(i+1) + ": " + str(ops[i])
                i = i+1
            if STAT or STAT_HISTO_P or STAT_HISTO_U:
                stats.append((measure, len(ops), False, p_size, u_size))
            else:
                choice = raw_input('Operation choice: ')

                # Perform anonymization
                print "Anonymizing graph..."
                g.serialize(destination='./out/output_anonymized_orig_'+time.strftime("%Y%m%d-%H%M%S")+'.ttl', 
                            format='trig')
                print "\tOperation " + str(choice) + " launched..."
                seq = ops[int(choice)-1]
                seq_step = 0
                for o in seq:
                    seq_step += 1
                    o.update(g, custom_prefixes())
                    g.serialize(destination='./out/output_anonymized_step'+str(seq_step)+'_'+time.strftime("%Y%m%d-%H%M%S")+'.ttl',                         format='trig')
                print "\tLength after deletion: " + str(len(g)) + " triples"
        else:
            if STAT or STAT_HISTO_P or STAT_HISTO_U:
                stats.append((measure, 0, True, p_size, u_size))

    if STAT:
        if not os.path.exists('exp'):
            os.makedirs('exp')
        with open('exp/stats_'+str(p_pol_size)+'_'+str(u_pol_size)+'.csv', 'wb') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', escapechar=' ')
            wr.writerow(["Overlap", "Length", "Incompatibility","PrivacySize","UtilitySize"])
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            for s in stats:
                wr.writerow(s)
    if STAT_HISTO_P:
        if not os.path.exists('exp'):
            os.makedirs('exp')
        with open('exp/stats_hist_p9_'+str(p_pol_size)+'_'+str(u_pol_size)+'.csv', 'wb') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', escapechar=' ')
            wr.writerow(["Overlap", "Length", "Incompatibility","PrivacySize","UtilitySize"])
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            for s in stats:
                wr.writerow(s)
    if STAT_HISTO_U:
        if not os.path.exists('exp'):
            os.makedirs('exp')
        with open('exp/stats_hist_u9_'+str(p_pol_size)+'_'+str(u_pol_size)+'.csv', 'wb') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', escapechar=' ')
            wr.writerow(["Overlap", "Length", "Incompatibility","PrivacySize","UtilitySize"])
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            for s in stats:
                wr.writerow(s)


if __name__ == "__main__":
    main()
