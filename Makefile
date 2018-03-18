DB_USER     ?= root
DB_PASS     ?= root
DB_HOST     ?= localhost
DB_PORT     ?= 3306
DB_ENCODING ?= utf8
DB_SCHEMA   = findinghome

CONNECTION_STRING = mysql://$(DB_USER):$(DB_PASS)@$(DB_HOST)/$(DB_SCHEMA)?charset=$(DB_ENCODING)

.PHONY: build
build:
	pip install -r requirements.txt

.PHONY: run
run:
	python daft.py --connection_string $(CONNECTION_STRING)

.PHONY: build_db
build_db:
	cat schema.sql | mysql -u$(DB_USER) -p$(DB_PASS)
