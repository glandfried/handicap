all: data/handicap.pickle 

data/handicap.pickle: software/trueskill/.git
	make -C data

software/trueskill/.git:
	git submodule update --init software/trueskill/
	make handicap -C software/trueskill/



software/glicko2/.git:
	git submodule update --init software/glicko2/
software/analytic-bayesian-linear-regression/.git:
	git submodule update --init software/analytic-bayesian-linear-regression/
