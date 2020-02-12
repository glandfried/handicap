all: results.zip results/
results.zip:
	wget https://github.com/glandfried/output-ogs-dataset/releases/download/v1.0/results.zip

results/:
	unzip results.zip
