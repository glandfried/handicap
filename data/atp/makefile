all: history.csv history.adapted.csv

history.csv:
	wget https://github.com/glandfried/tennis_atp/releases/download/atp/history.csv.zip
	unzip history.csv.zip
	rm history.csv.zip

history.adapted.csv:
	python3 adapt.py
