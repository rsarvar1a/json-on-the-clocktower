.PHONY: all

all: fmt lint

POETRY=poetry
POETRY_OK:=$(shell command -v $(POETRY) 2> /dev/null)
PYSRC=morph

poetry:
ifndef POETRY_OK
	python3 -m pip install poetry
endif

install-dev: poetry
	@$(POETRY) config virtualenvs.in-project true
	@$(POETRY) install --quiet

fmt: install-dev
	@$(POETRY) run black -t py311 $(PYSRC)

lint: install-dev
	@$(POETRY) run pylint $(PYSRC)

test: install-dev
	@$(POETRY) run poetry run pytest -v --junit-xml=test-results.xml $(PYSRC)/tests

morph: install-dev
	@$(POETRY) run python -m morph.cli --force-fetch
ifeq ($(shell uname),Darwin)
	@open data/generated/roles-combined.json
endif

rebuild-data: install-dev morph external-md5 external-md5-check
	@git add data/
	@git commit --no-verify -m "rebuild data"

external-md5:
	@$(POETRY) run python -m morph.external_md5

external-md5-check:
	@cd data/external && md5sum -c md5sum
