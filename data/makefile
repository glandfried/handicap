handicap.pickle: summary/summary.csv
	python3 handicap.py

summary.csv: summary.zip
	unzip -u summary.zip # -d data/

summary.zip:
	wget https://github.com/glandfried/output-ogs-dataset/releases/download/v1.1/summary.zip #-O data/results.zip
