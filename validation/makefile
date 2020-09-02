all: ../data/ogs/summary_filtered.csv ../software/trueskill.jl/.git
	julia validation.jl

../data/ogs/summary_filtered.csv:
	make -C ../data/ogs/

../software/trueskill.jl/.git:
	git submodule  update --init ../software/trueskill.jl/
