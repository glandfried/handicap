all: figure

figure: data/handicap.pickle software/analytic-bayesian-linear-regression/.git
	make -C figures

data/handicap.pickle: software/skill/.git
	make -C data

software/skill/.git:
	git submodule update --init software/skill/
	make handicap -C software/skill/

software/glicko2/.git:
	git submodule update --init software/glicko2/
software/analytic-bayesian-linear-regression/.git:
	git submodule update --init software/analytic-bayesian-linear-regression/
	make setup -C analytic-bayesian-linear-regression/

setup:
	echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
	
	
	

