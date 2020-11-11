PYTEST_JUNIT_OUT_FILE=${PYTEST_JUNIT_OUT_FILE:-TODO}

tests:: unit-tests

unit-tests:
	pytest tests/

lint::
	flake8 src/ tests/

format::
	black src/ tests/

coverage::
	echo "TODO"

nuke::
	git clean -xn
