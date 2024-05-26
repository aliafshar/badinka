
test:
	./ve/bin/py.test

test_long:
	./ve/bin/py.test --capture=no --verbose --integration

test_verbose:
	./ve/bin/py.test --capture=no --verbose

docs_gen:
	./ve/bin/python -W ignore docs/gen.py

docs_upload: docs_gen
	cd docs && firebase deploy
