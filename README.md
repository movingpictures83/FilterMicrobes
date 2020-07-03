# FilterMicrobes
# Language: Python
# Input: CSV (file to be filtered)
# Output: CSV (filtered values)
# Tested with: PluMA 1.1, Python 3.6
# Dependency: numpy==1.16.0

PluMA plugin that accepts a CSV file representing a multi-omics network,
with nodes represented by both rows and columns and entry (i, j) the weight
of the connection from node i to node j.

The network is assumed to contain both metabolomics and metagenomics data.
Connections between two metagenomic nodes are then filtered out (set to zero)
if they cannot be joined by an underlying metabolomic network.  Note this implies
that for connection i->j to remain there must some network of metabolites
m1...mN such that i->m1->m2...->mN->j.

This can be useful for discovering metagenomic dependencies that can be
backed up by metabolomic databases.  Metabolites are assumed to start with
the letter "X".

