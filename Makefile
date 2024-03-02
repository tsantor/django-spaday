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

# -----------------------------------------------------------------------------

env:  ## Create virtual environment
	pyenv virtualenv ${python_version} ${venv} && pyenv local ${venv}

reqs:  ## Install requirements
	python3 -m pip install -U pip && \
		python -m pip install -r requirements_dev.txt && \
		python -m pip install -r requirements_test.txt

migrations:  ## Create migrations
	python3 manage.py makemigrations

migrate:  ## Apply migrations
	python3 manage.py migrate

createsuperuser:  ## Create superuser
	python3 manage.py createsuperuser

serve:  ## Run server
	python3 manage.py runserver 0.0.0.0:8000

scratch: env reqs migrate createsuperuser serve  ## Create environment, install requirements, apply migrations, create superuser and run server

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

pytest:  ## Run tests
	pytest -v -x

coverage:  ## Run tests with coverage
	coverage run -m pytest && coverage html
	# --skip-covered

open_coverage:  ## open coverage report
	open htmlcov/index.html

# -----------------------------------------------------------------------------

clean:  ## Remove build artifacts
	# Remove build artifacts
	rm -rf {build,dist,*.egg-info}

# build:  ## Build package
# 	python3 setup.py sdist bdist_wheel

# upload_test:
# 	python3 setup.py sdist bdist_wheel && twine upload dist/* -r pypitest

# upload:
# 	python3 setup.py sdist bdist_wheel && twine upload dist/* -r pypi
