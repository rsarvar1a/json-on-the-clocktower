.PHONY: all

all: fmt lint

POETRY=poetry
POETRY_OK:=$(shell command -v $(POETRY) 2> /dev/null)
PYSRC=melder

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
	@$(POETRY) run python -m unittest $(PYSRC)

meld: install-dev
	@$(POETRY) run python -m melder.cli
ifeq ($(shell uname),Darwin)
	@open data/generated/roles-combined.json
endif

morph: install-dev
	@$(POETRY) run python -m morph.cli
