# Declarative LOD Anonymizer

This is a draft of a research project aiming at designing theoretical and
concrete tools to anonymize Linked Open Data graphs, notably RDF triple stores.
The article describing the foundations behind this work and the goal of this
implementation was [submitted to the ESWC2018 conference](https://2018.eswc-conferences.org/paper_12/),
 its acceptation is pending.

## Setup

To reproduce the various experiments and examples from the article, you can
execute the code yourself on our example graph schema.

### Prerequisites

This project uses Python and should work on any version of Python 3 and any 
version of Python starting from Python 2.7.

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

You can also use the demo mode, which is ran using a shortened workload and does
not run the graph anonymization code, only the anonymization sequence generation:

```bash
python main.py -d
```

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

The first creates general stats about compatibility (cf. Figures 2a, 2b and 2c in the article),
the second data when utility size is fixed (Fig. 1a), the third when privacy size is fixed (Fig. 1b).

### Plot statisics

Graph figures can be recreated using the provided R script ```plot.r```. You can run it
directly in your favorite R editor, or copy/paste the contents in the R console.

This script will generate five figures in the ```exp``` directory as follows:

- ```cand_overlap_3_3.png```: Boxplot of the size of found candidate sets depending on the measure overlapping between policies
- ```cand_size_priv_3_3.png```: Boxplot of the size of found candidate sets depending on the privacy size (utility size is fixed)
- ```cand_size_util_3_3.png```: Boxplot of the size of found candidate sets depending on the utility size (privacy size is fixed)
- ```incomp_size_priv_3_3.png```: Histogram of the number of compatible cases found depending on the privacy size (utility size is fixed)
- ```incomp_size_util_3_3.png```: Histogram of the number of compatible cases found depending on the utility size (privacy size is fixed)
