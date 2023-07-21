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
	@$(POETRY) run python -m morph.cli --force-fetch
ifeq ($(shell uname),Darwin)
	@open data/generated/roles-combined.json
endif

rebuild-data: install-dev morph external-md5 external-md5-check
	@git add data/
	@git commit --no-verify -m "rebuild data"



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

external-md5:
	@$(POETRY) run python -m morph.external_md5

external-md5-check:
	@cd data/external && md5sum -c md5sum
