# Project settings
PROJECT := toothbrush
PACKAGE := toothbrush
REPOSITORY := thomasvincent/toothbrush

# Project paths
PACKAGES := $(PACKAGE) tests
CONFIG := $(wildcard *.py)
MODULES := $(wildcard $(PACKAGE)/*.py)

# Virtual environment paths
export PIPENV_VENV_IN_PROJECT=true
export PIPENV_IGNORE_VIRTUALENVS=true
VENV := .venv

# MAIN TASKS ##################################################################

SNIFFER := pipenv run sniffer

.PHONY: all
all: install

.PHONY: ci
ci: check test ## Run all tasks that determine CI status

.PHONY: watch
watch: install .clean-test ## Continuously run all CI tasks when files chanage
	$(SNIFFER)

.PHONY: run ## Start the program
run: install
	pipenv run python $(PACKAGE)/__main__.py

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES ########################################################

DEPENDENCIES = $(VENV)/.pipenv-$(shell bin/checksum Pipfile* setup.py)

.PHONY: install
install: $(DEPENDENCIES)

$(DEPENDENCIES):
	pipenv run python setup.py develop
	pipenv install --dev
	@ touch $@

# CHECKS ######################################################################

ISORT := pipenv run isort
PYLINT := pipenv run pylint
PYCODESTYLE := pipenv run pycodestyle
PYDOCSTYLE := pipenv run pydocstyle

.PHONY: check
check: isort pylint pycodestyle pydocstyle ## Run linters and static analysis

.PHONY: isort
isort: install
	$(ISORT) $(PACKAGES) $(CONFIG) --recursive --apply

.PHONY: pylint
pylint: install
	$(PYLINT) $(PACKAGES) $(CONFIG) --rcfile=.pylint.ini

.PHONY: pycodestyle
pycodestyle: install
	$(PYCODESTYLE) $(PACKAGES) $(CONFIG) --config=.pycodestyle.ini

.PHONY: pydocstyle
pydocstyle: install
	$(PYDOCSTYLE) $(PACKAGES) $(CONFIG)

# TESTS #######################################################################

PYTEST := pipenv run py.test
COVERAGE := pipenv run coverage
COVERAGE_SPACE := pipenv run coverage.space

RANDOM_SEED ?= $(shell date +%s)
FAILURES := .cache/v/cache/lastfailed

PYTEST_OPTIONS := --random --random-seed=$(RANDOM_SEED)
ifdef DISABLE_COVERAGE
PYTEST_OPTIONS += --no-cov --disable-warnings
endif
PYTEST_RERUN_OPTIONS := --last-failed --exitfirst

.PHONY: test
test: test-all ## Run unit and integration tests

.PHONY: test-unit
test-unit: install
	@ ( mv $(FAILURES) $(FAILURES).bak || true ) > /dev/null 2>&1
	$(PYTEST) $(PACKAGE) $(PYTEST_OPTIONS)
	@ ( mv $(FAILURES).bak $(FAILURES) || true ) > /dev/null 2>&1
	$(COVERAGE_SPACE) $(REPOSITORY) unit

.PHONY: test-int
test-int: install
	@ if test -e $(FAILURES); then $(PYTEST) tests $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	$(PYTEST) tests $(PYTEST_OPTIONS)
	$(COVERAGE_SPACE) $(REPOSITORY) integration

.PHONY: test-all
test-all: install
	@ if test -e $(FAILURES); then $(PYTEST) $(PACKAGES) $(PYTEST_RERUN_OPTIONS); fi
	@ rm -rf $(FAILURES)
	$(PYTEST) $(PACKAGES) $(PYTEST_OPTIONS)
	$(COVERAGE_SPACE) $(REPOSITORY) overall

.PHONY: read-coverage
read-coverage:
	bin/open htmlcov/index.html

