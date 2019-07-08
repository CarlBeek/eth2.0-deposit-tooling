PY_DEPOSIT_DIR = ./deposit_script

clean:
	rm -rf eth2.0-specs/
	rm -rf $(PY_DEPOSIT_DIR)/venv

install_test:
	git clone git@github.com:ethereum/eth2.0-specs.git;
	cd $(PY_DEPOSIT_DIR);  python3 -m venv venv; . venv/bin/activate; pip3 install -r requirements.txt

test_python:
	cd $(PY_DEPOSIT_DIR); . venv/bin/activate; export PYTHONPATH="./"; \
	python -m pytest

test: test_python

lint:
	cd $(PY_DEPOSIT_DIR); . venv/bin/activate; \
	flake8 --max-line-length=120 --exclude venv . \
	&& mypy ./
