.PHONY: venv install activate clean

VENV_NAME=venv
PYTHON=python3
PIP=pip3
REQUIREMENTS=requirements.txt

venv:
	$(PYTHON) -m venv $(VENV_NAME)

install: venv
	. ./$(VENV_NAME)/bin/activate && \
	$(PIP) install --upgrade pip setuptools wheel && \
	$(PIP) install -r $(REQUIREMENTS)

clean:
	rm -rf $(VENV_NAME)