![test](https://github.com/davips/kururu/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/kururu/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/kururu)

# kururu - data science in the classroom
**WARNING: This project will undergo major changes in the next rewrite.**

<a title="CostaPPPR / CC BY-SA (https://creativecommons.org/licenses/by-sa/3.0)" href="https://commons.wikimedia.org/wiki/File:Sapo_Cururu-DISC_1328.jpg"><img width="256" alt="Sapo Cururu-DISC 1328" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Sapo_Cururu-DISC_1328.jpg/256px-Sapo_Cururu-DISC_1328.jpg"></a>

# Installation

# Examples
**Evaluated training**
<details>
<p>

```python3

from aiuna import *
from kururu import *

d = dataset("abalone").data

# Each imported step is a callable object which can be used with no parameters.
steps = binarize * split * pca * svm * metric

# After the Data object goes through the steps, its last version has the test accuracy value at 'r'.
d2 = d >> steps
print(d2.r)
"""
[0.56698565]
"""
```


</p>
</details>

# Essential concepts
The kururu framework simplifies data-related tasks (like data science) 
by providing straight-forward tools for carefully chosen general concepts:
1. **step** - kururu unifies all data-related processes under the concept of (data science) *step*
    - steps are instances of Python classes derived from Step
    - steps can be partially configured (e.g., `svm(kernel="poly")`) <br>
      or not configured at all (e.g., `svm()` or `svm` for short), <br>
      which has two different meanings, depending on the use case:
        1. a step ready to process data, using default values for the omitted parameters, e.g.:
            - ```python
              result = data >> svm(kernel="poly")  # more on `>>` latter
              ```
        1. a sampleable (ordered<sup>1</sup>) set of different steps, e.g.:
            - ```python
              svms = svm(kernel="poly")  # take the subset of all polynomial kernel SVMs
              svm0 = ~svms  # sample a single configuration randomly, more on `~` latter
              result = data >> svm0
              ```
1. **data** - all input to (and output from) each step is a Data object
    - when in a machine learning context, this includes both training and test sets, and the results as well
    - *inner/outer* - steps that process two data sets expect the (*outer*) Data object to contain an *inner* data field
    - *stream* - steps that process several data sets (e.g., partitioned or streamed) at once expect the *outer* data to
      contain a *stream* field
1. **operator** - steps are combined by operators and applied to Data objects through operators
    - **product** - steps are chained by the **&ast;** operator, which, analogously to the previous *step* definition,
      has two different meanings, depending on the use case:
        1. a sequence of steps (i.e., a *Product* object) ready to process data, using default values for the omitted
           parameters, e.g.:
            - ```python
              sequence = pca * svm(kernel="poly") 
              result = data >> sequence  # more on `>>` latter
              ```
        1. a sampleable set of different sequences of steps, e.g.:
            - ```python
              sequences = pca * svm(kernel="poly")  # take the subset of all combinations between all PCAs and polynomial kernel SVMs
              sequence = ~sequences  # sample a sequence randomly, more on `~` latter
              result = data >> sequence
              ```

**ONGOING WORK FROM HERE UNTIL THE END OF THE PAGE....**

   - **union** - sets of steps are united by the **+** operator, which returns a *Union* object.
    The implementation of the class Union doesn't follow the math concept of union of sets strictly.
    It can have repeated elements for three reasons: 
    there is no gain in enforcing such math requirement;
    it can be useful in some scenario involving the *stream* field where the repetition is actually needed;
    and, more importantly, it is ordered (this applies to all sets if steps also). 
    Like any Step object, Union has two different use cases:
     1. a set of steps ready to process data, using default values for the omitted parameters, e.g.: 
        - ```python
          ONGOING WORK ....
          union = mlp + svm(kernel="poly") 
          result = data >> ... * union *   # more on `...` and `>>` latter
          ```
     1. a sampleable set of different sequences of steps, e.g.:
        - ```python
          sequences = pca * svm(kernel="poly")  # take the subset of all combinations between all PCAs and polynomial kernel SVMs
          sequence = ~sequences  # sample a sequence randomly, more on `~` latter
          result = data >> sequence
          ```
<sup>1</sup> *Not important for the context, but it is worth to mention it is an ordered set, 
because the mathematical definition of sets has no ordering.
We use the term "set" instead of list to avoid the need to explicitly borrow all the needed
concepts related to set operations.*

# Data exploration versus machine learning
Whether in a console (e.g., *ipython*) or a temporary script (e.g., *jupyter notebooks*), sometimes one needs to easily manipulate data, 
or to easily set up a machine learning workflow.
To fit the needs of both distinct use cases (lightly leaning towards the writing of workflows), kururu provides step suffixes.
Some representative examples are given in the following table where
- **XXX_** means the step XXX will be trained and tested on outer<sup>2</sup> data (useful for data exploration);
- in all other cases, XXX will be trained on inner data:
  - **XXXi** means XXX tested on **inner** data 
  - **XXXo** means XXX tested on **outer** data 
  - **XXXb** means XXX tested on both **inner** and **outer** data 

Use case            | Name                          | Shorthand <br>(if any) | Suffixed Form | Training set  | Test set(s)   | 
 ---                | ---                           | ---           |  ---          | ---           | ---           |
data exploration    | Principal Component Analisys  |               | PCA_          | outer<sup>2</sup> | outer<sup>2</sup> |
machine learning    | Noise Reduction               | NR            | NRi           | inner         | inner         |
machine learning    | Support Vector Machines       | SVM           | SVMo          | inner         | outer         |
machine learning    | Principal Component Analisys  | PCA           | PCAb          | inner         | both          |

<sup>2</sup> *Please note that, to simplify the terminology across the documentation, 
the Data object is called "outer" even if it has no inner field.* 
   
Finally, for completeness, the other meaningful versions of the steps presented in the previous table are now also included as follows.

Use case            | Name                          | Class to use  | Training set  | Test set(s)   | 
 ---                | ---                           | ---           |  ---          | ---           |
data exploration    | Principal Component Analisys  | PCA_          | outer         | outer         |
machine learning    | Principal Component Analisys  | PCA           | inner         | both          |
data exploration    | Noise Reduction               | NR_           | outer         | outer         |
machine learning    | Noise Reduction<sup>3</sup>   | NR            | inner         | inner         |
machine learning    | Support Vector Machines       | SVM           | inner         | outer         |
machine learning    | Support Vector Machines       | SVMb          | inner         | both          |


<sup>3</sup> *Some of the steps (e.g., NR) may not implement the XXXb (e.g., NRb) version 
when it is not applicable.* 

# Implementing custom Step classes 
All fields that update a Data object should be lazy, i.e. should be a 'callable' without args.
An easy way to do that is to put `lambda:` before the value intended to be returned.
However, usually the return value is dependent upon fields from a previous Data object.
They should be accessed only from within the callable/lambda for a proper (iterator-safe) implementation.
Example:
**Creating a custom step**
<details>
<p>

```python3
from akangatu.distep import DIStep


# DIStep means "Data Independent Step", i.e. it does not depend on previously known data.
class MyAdditionStep(DIStep):
    """Multiplies the given field by a factor."""

    def __init__(self, field, factor):
        # All relevant step parameters should be passed to super() as keyword arguments.
        super().__init__(field=field, factor=factor)

        # Instance attributes are set as usual.
        self.field = field
        self.factor = factor

    def _process_(self, data):
        # All calculations (including access to data fields)
        #   is deferred to a future access to the return field - R in this case.
        return data.update(self, R=lambda: data[self.field] * self.factor)

```


</p>
</details>  

# Field name rules
A field named with a single letter has a lower case shortcut for automatic conversion from matrix to scalar/vector and vice versa.
Suffixes: ...
Reserved names: ...

# Contribution

Nothing clear yet, but one of the ways one can contribute is by creating their own repository (to be listed here as a
partner), using this repository (and/or other related ones) as a dependence. Monkey-patch can be used if one needs to
urgently integrate a module inside the same class tree used here, or ask for access to this repository, or submit a pull
request. The software architecture was planned taking that into account. It provides clear interface-classes to guide
the implementer/IDE, and each repository with a specific well-defined purpose.

# Grants
Part of the effort spent in the present code was kindly supported by Fapesp under supervision of
Prof. André C. P. L. F. de Carvalho at CEPID-CeMEAI (Grants 2013/07375-0 – 2019/01735-0).

# History

Except dependencies like sklearn and other libraries, the novel ideias presented here are a result of a years-long
process of drafts, thinking, trial/error and rewrittings from scratch in several languages from Delphi, passing through
Haskell, Java and Scala to Python. The fundamental concepts were lightly borrowed from basic category theory concepts
like algebraic data structures that permeate many recent tendencies, e.g., in programming language design.

For code (and academic) details refer to the following projects (few of them are usable by now):

2003  [TUPI imaging: there was no widespread use of git at that time / retroactive repo yet to be created]

2006  [Multicore NN: there was no widespread use of git at that time / retroactive repo yet to be created]

2013 Functional language parser/interpreter  https://github.com/davips/lamdheal-j

2014 Machine learning library including Weka algorithms, optimized immutable data structure and models, hand-made
BLAS/LAPACK neural networks, transparent distributed processing (in conjunction with active-learning-scala), plotting,
evaluation, early replicability   https://github.com/davips/mls

2015 Active learning library   https://github.com/davips/active-learning-scala

2016 Thesis and dataset generation and
visualization   https://github.com/davips/tese    https://github.com/davips/knowledge-boundary    https://github.com/davips/image2arff

2018 Gaussian processses   https://github.com/davips/surface

2019 Client to generate reports from stored results  https://github.com/davips/mysql2csv

2020 Python project where previous attempts and evolving ideias were
tested    https://github.com/davips/pjml-may_archived
