all: figure

figure: data/handicap.pickle software/ablr/.git
	make -C figures

data/handicap.pickle: software/skill/.git
	make -C data

software/skill/.git:
	git submodule update --init software/skill/
	make handicap -C software/skill/

software/glicko2/.git:
	git submodule update --init software/glicko2/
software/abrl/.git:
	git submodule update --init software/abrl/
	make -C software/abrl/ setup

setup:
	echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
	
	
	

