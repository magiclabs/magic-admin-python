.PHONY: production
production: virtualenv_run install_prod_requirements

.PHONY: development
development: virtualenv_run install_prod_requirements install_dev_requirements install-hooks

.PHONY: virtualenv_run
virtualenv_run:
	virtualenv -p python3.6 virtualenv_run
	virtualenv_run/bin/pip install --upgrade pip

.PHONY: install_prod_requirements
install_prod_requirements: virtualenv_run
	virtualenv_run/bin/pip install -r requirements.txt

.PHONY: install_dev_requirements
install_dev_requirements: virtualenv_run
	virtualenv_run/bin/pip install -r requirements-dev.txt

.PHONY: install-hooks
install-hooks: virtualenv_run install_dev_requirements
	./virtualenv_run/bin/pre-commit install -f --install-hooks

.PHONY: test
test:
	tox

clean-cache:
	find . -name '__pycache__' | xargs rm -rf
	find . -name '*.pyc' -delete

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf sdist/
	rm -rf *.egg
	rm -rf *.eggs/
	rm -rf *.egg-info

.PHONY: clean
clean: clean-cache clean-build
	rm -rf virtualenv_run/
	rm -rf .virtualenv_run_test/
	rm -rf .pytest_cache/
	rm -rf .tox/
