# -----------------------------------------------------------------------------
# Generate help output when running just `make`
# -----------------------------------------------------------------------------
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# -----------------------------------------------------------------------------

python_version=3.9.11
venv=djangospaday_env

# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------

env:  ## Create virtual environment
	pyenv virtualenv ${python_version} ${venv} && pyenv local ${venv}

env_remove:  ## Remove virtual environment
	pyenv uninstall ${venv}

# -----------------------------------------------------------------------------
# Pip
# -----------------------------------------------------------------------------

pip_install:  ## install requirements
	python3 -m pip install -U pip && \
		python -m pip install -r requirements.txt && \
		pre-commit install

pip_list:  ## run pip list
	python3 -m pip list

pip_freeze:  ## run pipfreezer
	pipfreezer

pip_checker:  ## run pipchecker
	python3 manage.py pipchecker

# -----------------------------------------------------------------------------
# Django
# -----------------------------------------------------------------------------

manage:	## run django manage.py (eg - make manage cmd="shell")
	python3 manage.py ${cmd}

superuser:  ## Create superuser
	python3 manage.py createsuperuser

migrations:  ## Create migrations (eg - make migrations app="core")
	python3 manage.py makemigrations ${app}

migrate:  ## Apply migrations
	python3 manage.py migrate

serve:  ## Run server
	python3 manage.py runserver 127.0.0.1:8000

show_urls:  ## show urls
	python3 manage.py show_urls

shell:  ## run shell
	python3 manage.py shell_plus

flush:  ## Flush database
	python3 manage.py flush

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

pytest:  ## Run tests
	pytest -v -x

pytest_verbose:  ## Run tests
	pytest -vs

coverage:  ## Run tests with coverage
	coverage run -m pytest && coverage html

coverage_verbose:  ## Run tests with coverage
	coverage run -m pytest -vs && coverage html

coverage_skip:  ## Run tests with coverage
	coverage run -m pytest -vs && coverage html --skip-covered

open_coverage:  ## open coverage report
	open htmlcov/index.html

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

clean_build: ## remove build artifacts
	rm -fr build/ dist/ .eggs/
	find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

clean_pyc: ## remove python file artifacts
	find . \( -name '*.pyc' -o -name '*.pyo' -o -name '*~' -o -name '__pycache__' \) -exec rm -fr {} +

clean: clean_build clean_pyc ## remove all build and python artifacts

clean_pytest_cache:  ## clear pytest cache
	rm -rf .pytest_cache

clean_tox_cache:  ## clear tox cache
	rm -rf .tox

clean_coverage:  ## clear coverage cache
	rm .coverage
	rm -rf htmlcov

clean_tests: clean_pytest_cache clean_tox_cache clean_coverage  ## clear pytest, tox, and coverage caches

# -----------------------------------------------------------------------------
# Miscellaneous
# -----------------------------------------------------------------------------

tree:  ## Show directory tree
	tree -I 'build|dist|htmlcov|node_modules|migrations|contrib|__pycache__|*.egg-info|staticfiles|media'

# -----------------------------------------------------------------------------
# Deploy
# -----------------------------------------------------------------------------

dist: clean ## builds source and wheel package
	python -m build --wheel

release_test: ## upload package to pypi test
	twine upload dist/* -r pypitest

release: dist ## package and upload a release
	twine upload dist/*

# -----------------------------------------------------------------------------
# Project Specific
# -----------------------------------------------------------------------------

# Add project specific targets here
