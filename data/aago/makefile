all: aago.csv aago_kgs_ogs.csv aago.adapted.csv aago_original_filtered.csv

aago_original_filtered.csv:
	https://github.com/glandfried/aago/releases/download/v1.1/aago_original_filtered.csv

aago.csv:
	https://github.com/glandfried/aago/releases/download/v0.0.0/aago.csv

aago_kgs_ogs.csv:
	https://github.com/glandfried/aago/releases/download/v0.0.0/aago_kgs_ogs.csv

aago_original_filtered.adapted.csv: adapt.py aago_original_filtered.csv
	python3 adapt.py
