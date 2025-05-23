include .env

$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

run:
	cd src && python github_stats.py -u twarsop -s 2024-01-01 -t 2024-06-01 -f github_stats.json