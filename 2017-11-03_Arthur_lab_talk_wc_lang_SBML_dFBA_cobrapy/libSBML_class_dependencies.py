#!/usr/bin/env python
# visualize dependencies among libSBML model classes

# dependencies among libSBML model classes constrain the order in which they're written:
#     Model depends on nothing
#     Compartment depends on nothing
#     Parameter depends on nothing
#     Compartment must precede Species
#     Compartment must precede Reaction
#     Species must precede Reaction
#     Reaction must precede ObjectiveFunction
# This partial order is satisfied by this sequence:
# model_order = [Model, Compartment, Parameter, Species, Reaction, ObjectiveFunction]

import pygraphviz as pgv

nodes = "Model Compartment Parameter Species Reaction ObjectiveFunction"
dependencies = """
Compartment Species
Species Reaction
Reaction ObjectiveFunction"""

A = pgv.AGraph(directed=True, name='blue')
for node in nodes.split():
    A.add_node(node, color = 'blue')

for line in dependencies.split('\n'):
    line = line.strip()
    if line:
        (antecedent, successor) = line.split()
        A.add_edge(antecedent, successor, color='red')

print(A.string()) # print to screen
A.layout() # layout with default (neato)
A.draw('libSBML_class_dependencies.png') # draw png