PROJECT = django_smorest
PYTHON_VERSION=3.7
venv_name = py${PYTHON_VERSION}-${PROJECT}
venv = .venv/${venv_name}

# Commands that activate and run virtual environment versions.
_python = . ${venv}/bin/activate; python
_pip = . ${venv}/bin/activate; pip

create_venv: ${venv}
.PHONY: create_venv

${venv}: PYTHON_PREFIX=
${venv}: requirements.txt
	${PYTHON_PREFIX}python${PYTHON_VERSION} -m venv ${venv}
	${_pip} install --upgrade pip --cache .tmp/
	${_pip} install -r requirements.txt --cache .tmp/

update_venv: requirements.txt ${venv}
	${_pip} install -r requirements.txt --cache .tmp/
	@rm -f .venv/current
	@ln -s ${venv_name} .venv/current
	@echo Success, to activate the development environment, run:
	@echo "\tsource .venv/current/bin/activate"
.PHONY: update_venv
