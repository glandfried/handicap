handicap.pickle: summary/summary.csv
	python3 handicap.py

summary/summary.csv: resultsJson
	make -C summary/

resultsJson: resultsJson.zip
	unzip -u resultsJson.zip # -d data/

resultsJson.zip:
	wget https://github.com/glandfried/output-ogs-dataset/releases/download/v1.1/resultsJson.zip #-O data/results.zip
