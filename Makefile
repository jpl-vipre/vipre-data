.PHONY: hello

hello:
	echo hello

requirements.txt:
	poetry export -f requirements.txt --without-hashes | \
		cut -d ";" -f 1 > requirements.txt

vipre-api.pex: requirements.txt
	cd src && poetry run pex -r ../requirements.txt -D . -c uvicorn -o ../vipre-api.pex

pex: vipre-api.pex

