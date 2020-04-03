all: figure

figure: data/handicap.pickle software/ablr/.git
	make -C figures

data/handicap.pickle: software/skill/.git
	make -C data

software/skill/.git:
	git submodule update --init software/skill/
	make handicap -C software/skill/
software/ttt/.git:
	git submodule update --init software/ttt/
	make mirror 
software/glicko2/.git:
	git submodule update --init software/glicko2/
software/abrl/.git:
	git submodule update --init software/abrl/
	make -C software/abrl/ setup

setup:
	# El backend que agrego a matplotlib es para evitar un posible error
	echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
	
	
	

