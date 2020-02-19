all: data/handicap.pickle 

data/handicap.pickle: trueskill/.git
	make -C data

setup:
	git submodule update --init software/
	make setup -C analytic-bayesian-linear-regression/

software/trueskill/.git:
	git submodule update --init software/trueskill/.git
software/glicko2/.git:
	git submodule update --init software/glicko2/.git
software/analytic-bayesian-linear-regression/.git:
	git submodule update --init software/analytic-bayesian-linear-regression/.git
