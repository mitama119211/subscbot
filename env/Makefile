all: venv

venv:
	test -d venv || python -m venv venv
	. venv/bin/activate; pip install -U pip setuptools
	. venv/bin/activate; cd ../; pip install -e .
	touch venv/bin/activate

clean:
	rm -fr venv
	find -iname "*.pyc" -delete
