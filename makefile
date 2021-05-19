#all: talk

#talk: figure
#	make -C doc

#figure: data/handicap.pickle software/ablr/.git
#	make -C figures

estimations/tsh.csv: dataset software/skill/.git
	make -C estimations

dateset: 
	make -c data

# Posible fix
setup:
	# El backend que agrego a matplotlib es para evitar un posible error
	echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
	
	
	

