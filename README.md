# InPhO Answer Set Program (ASP)

## Dependencies
The Answer Set Program (ASP) requires [downloading DLV-Prolog](http://www.dlvsystem.com/dlv/), which is licensed for free academic use.

## Steps
1.  Create a file `classes.txt` that contains the taxonomic heirarchy, or use the `classes.inpho.txt` file that contains the [InPhO seed taxonomy](http://inpho.cogs.indiana.edu/taxonomy).
2.  Create a file `evals.txt` that contains the evaluations
3.  Run `dlv -pfilter=class,isa,ins,link classes.txt evals.txt program.txt 1> output.txt`

## Displaying in `inphosite`
A loose sketch that assumes a working install of the [`inpho`](http://github.com/inpho/inpho) package and a database backup with the Idea table already populated.

1.  `python toinpho.py output.txt`
2.  `git clone git@github.com:inpho/inphosite.git`
3.  `cd inphosite`
4.  `virtualenv sandbox --no-site-packages`
5.  `git checkout dynamic-display`
6.  `python setup.py develop`
7.  Create a `development.ini` file:
    a.  `cp template.ini development.ini`
    b.  Modify the `sqlalchemy.url` directive to match the one in `~/.config/inpho/inpho.ini`
8.  `paster serve development.ini`

## Citation

Mathias Niepert, Cameron Buckner, Colin Allen. Answer Set Programming on Expert Feedback to Populate and Extend Dynamic Ontologies. Proceedings of the 21st International FLAIRS Conference, Coconut Grove, Florida, pages 500-505, AAAI Press, 2008. [PDF](https://inpho.cogs.indiana.edu/papers/2008-InPhO-flairs.pdf)
