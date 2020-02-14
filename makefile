all: data/handicap.pickle

data/handicap.pickle: trueskill/.git
	make -C data

trueskill/.git:
	git submodule update --init trueskill/
