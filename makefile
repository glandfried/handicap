#all: talk

#talk: figure
#	make -C doc

#figure: data/handicap.pickle software/ablr/.git
#	make -C figures

estimations/tsh.csv: dataset software/skill/.git
	make -C estimations

dateset: 
	make -c data

# Submodules
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

# Posible fix
setup:
	# El backend que agrego a matplotlib es para evitar un posible error
	echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
	
	
	

