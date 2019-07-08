PY_DEPOSIT_DIR = ./deposit_script
ETH2_SPEC_DIR = ./eth2.0-specs
ETH2_PYSPEC_DIR = ./test_libs/pyspec/eth2spec/phase0/

clean:
	rm -rf eth2.0-specs/
	rm -rf $(PY_DEPOSIT_DIR)/venv
	rm -rf $(PY_DEPOSIT_DIR)/spec.py

install_test:
	git clone git@github.com:ethereum/eth2.0-specs.git;
	cd $(PY_DEPOSIT_DIR);  python3 -m venv venv; . venv/bin/activate; pip3 install -r requirements.txt
	cd $(ETH2_SPEC_DIR); make install_test

test_python:
	cd $(ETH2_SPEC_DIR); make pyspec; cp $(ETH2_PYSPEC_DIR)/spec.py .$(PY_DEPOSIT_DIR)
	cd $(PY_DEPOSIT_DIR); . venv/bin/activate; export PYTHONPATH="./"; \
	python -m pytest

test: test_python

lint:
	cd $(PY_DEPOSIT_DIR); . venv/bin/activate; \
	flake8 --ignore=E252,W504,W503 --max-line-length=120 --exclude venv . \
	&& mypy --follow-imports=skip ./
