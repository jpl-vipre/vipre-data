.PHONY: hello

VERSION = $(shell poetry version | cut -d ' ' -f 2)

mac:
	poetry install && \
	poetry run pyinstaller -y vipre-data.spec && \
	cd ./dist && \
	zip -r vipre-data-${VERSION}-mac.zip vipre-data/

version:
	echo ${VERSION}

hello:
	echo hello

requirements.txt:
	poetry export -f requirements.txt --without-hashes | \
		cut -d ";" -f 1 > requirements.txt

vipre-api.pex: requirements.txt
	cd vipre_data && poetry run pex -r ../requirements.txt -D . -c uvicorn -o ../vipre-api.pex

pex: vipre-api.pex

