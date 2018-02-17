# Declarative LOD Anonymizer

This is a draft of a research project aiming at designing theoretical and
concrete tools to anonymize Linked Open Data graphs, notably RDF triple stores.
The article describing the foundations behind this work and the goal of this
implementation was [submitted to the ESWC2018 conference](https://2018.eswc-conferences.org/paper_12/),
its acceptation is pending.

This program currently works by using a previously generated query workload and
picking a fixed number random queries in this workload to affect them in either
a privacy policy or an utility policy. Privacy queries must return no results in
an "anonymized graph", while utility queries must return the same results as on
the original graph. The code then computes possible sequences of operations to
perform on the graph to anonymize it based on this set of contraints. If such
sequences are found, an output is created with the supposedly anonymized graph.

## Setup

To reproduce the various experiments and examples from the article, you can
execute the code yourself on our example graph schema.

### Prerequisites

This project uses Python and should work on any version of Python 3 and any
version of Python starting from Python 2.7. You must install the [rdflib](https://github.com/RDFLib/rdflib)
and[unification](https://pypi.python.org/pypi/unification/0.2.2) Python libraries
to run this program.

The query workload is created using [gMark](https://github.com/graphMark/gmark),
which uses an XML configuration file to generate graphs and queries. You can follow
the instructions on the gMark project to generate your own workload, or use the provided
ones in the /conf/workloads directory. By default, /conf/workloads/starchain-workload.xml is used.

## Usage

### Standard execution

To run the program and anonymize a graph, just run it as follows:
```bash
python main.py
```

The graph anonymization feature is still being worked on. Right now, it uses
a Turtle-formatted RDF graph, named ```graph.ttl``` in the /conf/graphs directory.

You can also use the demo mode, which is ran using a shortened workload, with 2
privacy queries and 2 utility queries used the article's examples:

```bash
python main.py -d
```

The standard execution will compute possible anonymization sequences, each one
indexed by a number. After choosing a sequence, its operations (here only deletions)
are performed on the graph, creating several output files:

- A copy file of the original graph, named ```[original graph file name]_orig.ttl```
- One output file per operations, named ```[original graph file name]_anonymized_stepX.ttl```, X being the number of the applied of the applied operation.

### Running the tests

To reproduce the tests presented in the ESWC submission, you can run the statistics script:

```bash
./run_stats.sh
```

This will run the following commands:

```bash
python main.py 3 3 -s
python main.py 3 3 -hu
python main.py 3 3 -hp
```

The first creates general stats about compatibility with 7000 executions (cf. 
Figures 2a, 2b and 2c in the article), the second created data when utility size
is fixed, in 1400 executions (200 executions for 7 different privacy sizes, cf. Fig. 1a),
the third when privacy size is fixed (200 executions for 7 different utility sizes, cf. Fig. 1b).
 
You can also run each of these command separately using the previously mentioned flags,
as follows:

```bash
python main.py P U [-s|-hu|-hp]
```

With P being the cardinalty of the privacy policy (the number of queries to be
picked from the workload and affected to this query), and U the cardinality of
the utility policy.

### Plot statisics

Graph figures can be recreated using the provided R script ```plot.r```. You can run it
directly in your favorite R editor, or copy/paste the contents in the R console.

This script will generate five figures in the ```exp``` directory as follows:

- ```cand_overlap_3_3.png```: Boxplot of the size of found candidate sets depending on the measure overlapping between policies
- ```cand_size_priv_3_3.png```: Boxplot of the size of found candidate sets depending on the privacy size (utility size is fixed)
- ```cand_size_util_3_3.png```: Boxplot of the size of found candidate sets depending on the utility size (privacy size is fixed)
- ```incomp_size_priv_3_3.png```: Histogram of the number of compatible cases found depending on the privacy size (utility size is fixed)
- ```incomp_size_util_3_3.png```: Histogram of the number of compatible cases found depending on the utility size (privacy size is fixed)
