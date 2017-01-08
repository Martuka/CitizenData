## Citizen Data

This project works with the Swiss federal popular initiatives that have been
created during the last century. The project will read and analyse these
initiatives and try to speculate on the future initiatives contents.



## Run it

This project uses mainly `python` in version 3.
The easiest way to have every required libraries is to use a virtual
environment:

* Install `virtualenv` if necessary.
* Set up a virtual environment: `virtualenv -p python3 env`.
* Activate it: `source env/bin/activate`.
* Install the required libraries using `pip`:
	`pip install -r requirements.txt`
* Install the TreeTagger following instructions at [its website](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)
* Update the config.conf file, particularly the 'tagdir' value to set the path to the tree-tagger installation folder.
* Once everything is done, simply run the application:
  `python run.py`
