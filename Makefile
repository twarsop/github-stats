include .env

$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

run:
	python src/github-stats.py -u twarsop -s 2023-10-01 -t 2023-11-01

env: env.sh.enc
	gpg --decrypt < env.sh.enc > .env

encrypt-env:
	export GPG_TTY=$(tty) && gpg --symmetric < env.sh > env.sh.enc