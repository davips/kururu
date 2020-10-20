# kururu - data science in the classroom

<a title="CostaPPPR / CC BY-SA (https://creativecommons.org/licenses/by-sa/3.0)" href="https://commons.wikimedia.org/wiki/File:Sapo_Cururu-DISC_1328.jpg"><img width="256" alt="Sapo Cururu-DISC 1328" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Sapo_Cururu-DISC_1328.jpg/256px-Sapo_Cururu-DISC_1328.jpg"></a>

# Installation

# Examples


# Implementing custom Step classes 
All fields that update a Data object should be lazy, i.e. should be a 'callable' without args.
An easy way to do that is to put `lambda:` before the value intended to be returned.
However, usually the return value is dependent upon fields from a previous Data object.
They should be accessed only from within the callable/lambda for a proper (iterator-safe) implementation.
Example:
<<laziness>>  

# Field name rules
A field named with a single letter has a lower case shortcut for automatic conversion from matrix to scalar/vector and vice versa.
Suffixes: ...
Reserved names: ...

# Contribution
Nothing clear yet, but one of the ways one can contribute is by creating their own repository (to be listed here as a partner), using this (and/or other related ones) as a dependence.
Monkey-patch can be used if one needs to urgently integrate a module inside the same class tree used here.
The software architecture was planned taking that into account, providing clear interface-classes to guide the implementer/IDE,
and several levels of increasing niceties across the repositories.


# Grants

# History
With the exception of dependencies like sklearn and others, the novel ideias presented here are a result of a years-long process of drafts, thinking, trial/error and rewrittings from scratch in several languages from Delphi, passing through Haskell, Java and Scala to Python. The fundamental concepts were lightly borrowed from basic category theory concepts like algebraic data structures that permeate many recent tendencies in programming language design, data flow specification, among others. 

For code (and academic) details refer to the following projects (few of them are usable by now):

2003  [TUPI imaging: there was no widespread use of git at this time / retroactive repo yet to be created]

2006  [Multicore NN: there was no widespread use of git at this time / retroactive repo yet to be created]

2013  Functional language parser/interpreter  https://github.com/davips/lamdheal-j

2014  Machine learning library including Weka algorithms, optimized immutable data structure and models, hand-made BLAS/LAPACK neural networks, transparent distributed processing (in conjunction with active-learning-scala), plotting, evaluation, early replicability   https://github.com/davips/mls

2015  Active learning library   https://github.com/davips/active-learning-scala

2016  Thesis and dataset generation and visualization   https://github.com/davips/tese    https://github.com/davips/knowledge-boundary    https://github.com/davips/image2arff

2018  Gaussian processses   https://github.com/davips/surface

2019  Client to generate reports from stored results  https://github.com/davips/mysql2csv

2020  Python project where previous attempts and evolving ideias were tested    https://github.com/davips/pjml-may_archived
