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
	@$(POETRY) run python -m unittest $(PYSRC)

morph: install-dev
	@$(POETRY) run python -m morph.cli
ifeq ($(shell uname),Darwin)
	@open data/generated/roles-combined.json
endif


release: fmt lint changelog
	@git tag v$$(poetry version --no-ansi --short)
	@git push --tags

changelog: next-version
	@changie batch $$(poetry version --short)
	@changie merge
	@git add CHANGELOG.md README.md .changes/
	@git commit --no-verify -m "changie updates for $$(poetry version --short)" CHANGELOG.md README.md .changes/
	@git push

next-version:
	@poetry version patch
	@git commit --no-verify -m "bump pyproject version to $$(poetry version --short)" pyproject.toml
