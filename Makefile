include .env

$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

run:
	python src/github-stats.py

env: env.sh.enc
	gpg --decrypt < env.sh.enc > .env

encrypt-env:
	export GPG_TTY=$(tty) && gpg --symmetric < env.sh > env.sh.enc