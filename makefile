#all: talk

#talk: figure
#	make -C doc

#figure: data/handicap.pickle software/ablr/.git
#	make -C figures
test: generate-expected
	cd tests; julia tests.jl

generate-expected: software/ttt.jl/.git estimations/aago2.jl
	cd estimations; julia aago2.jl
	touch $@

software/ttt.jl/.git:
    make -C software

estimations/tsh.csv: dataset software/skill/.git
	make -C estimations

dateset:
	make -c data

# Posible fix
setup:
	# El backend que agrego a matplotlib es para evitar un posible error
	echo "backend: Agg" > ~/.config/matplotlib/matplotlibrc
