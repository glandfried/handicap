all: handicap handicap_history handicap_population handicap_population_prod

handicap: pdf/handicap19.pdf pdf/handicap9.pdf pdf/handicap13.pdf
handicap_history:  pdf/handicap19_history.pdf pdf/handicap9_history.pdf pdf/handicap13_history.pdf
handicap_population: pdf/handicap19_population.pdf pdf/handicap9_population.pdf pdf/handicap13_population.pdf
handicap_population_prod: pdf/handicap9_population_prod.pdf pdf/handicap13_population_prod.pdf pdf/handicap19_population_prod.pdf

pdf/handicap19.pdf:
	python3 handicap19.py
pdf/handicap9.pdf:
	python3 handicap9.py
pdf/handicap13.pdf:
	python3 handicap13.py

pdf/handicap19_history.pdf:
	python3 handicap19_history.py
pdf/handicap13_history.pdf:
	python3 handicap13_history.py
pdf/handicap9_history.pdf:
	python3 handicap9_history.py

pdf/handicap19_population.pdf:
	python3 handicap19_population.py
pdf/handicap13_population.pdf:
	python3 handicap13_population.py
pdf/handicap9_population.pdf:
	python3 handicap9_population.py

pdf/handicap9_population_prod.pdf:
	python3 handicap9_population_prod.py
pdf/handicap13_population_prod.pdf:
	python3 handicap13_population_prod.py
pdf/handicap19_population_prod.pdf:
	python3 handicap19_population_prod.py

pdf/handicap19_population_distribution.pdf:
	python3 handicap19_population_distribution.py
