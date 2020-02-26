handicap.pickle: summary/summary.csv
	python3 handicap.py

summary/summary.csv: results
	make -C data/summary/

results: results.zip
	unzip -u results.zip # -d data/

results.zip:
	wget https://github.com/glandfried/output-ogs-dataset/releases/download/v1.1/results.zip #-O data/results.zip
