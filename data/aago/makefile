all:
	wget https://github.com/glandfried/aago/releases/download/v0.0.0/data.tar.gz
	tar -zxvf data.tar.gz

raago:
	# select 'id', 'ranking', 'event_id', 'player_id' union select * from events_eventplayer into outfile '/var/lib/mysql-files/AGA.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
	sudo cp /var/lib/mysql-files/AGA.csv AGA.csv
