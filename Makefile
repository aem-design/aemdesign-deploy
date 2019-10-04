pydeps-install:
	mkdir -p library/python-packages
	pip install --requirement library/python-requirements.txt

pydeps: pydeps-install
