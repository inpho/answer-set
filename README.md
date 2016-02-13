# InPhO Answer Set Program (ASP)

## Dependencies
The Answer Set Program (ASP) requires [downloading DLV-Prolog](http://www.dlvsystem.com/dlv/), which is licensed for free academic use.

## Steps
1.  Create a file `classes.txt` that contains the taxonomic heirarchy, or use the `classes.inpho.txt` file that contains the [InPhO seed taxonomy](http://inpho.cogs.indiana.edu/taxonomy).
2.  Create a file `evals.txt` that contains the evaluations
3.  Run `dlv -pfilter=class,isa,ins,link classes.txt evals.txt program.txt 1> output.txt`
4.  Optional: to import to the InPhO database use `python toinpho.py`

## Citation

Mathias Niepert, Cameron Buckner, Colin Allen. Answer Set Programming on Expert Feedback to Populate and Extend Dynamic Ontologies. Proceedings of the 21st International FLAIRS Conference, Coconut Grove, Florida, pages 500-505, AAAI Press, 2008. [PDF](https://inpho.cogs.indiana.edu/papers/2008-InPhO-flairs.pdf)
