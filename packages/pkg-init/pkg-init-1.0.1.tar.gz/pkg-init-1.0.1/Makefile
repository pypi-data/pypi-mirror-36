# Copyright (c) 2018 bluelief.
# This source code is licensed under the MIT license.

.PHONY: install clean version pypi

install:
	python3 setup.py install

clean:
	rm -rf ./__pycache__/
	rm -rf ./*/__pycache__/
	rm -rf ./*/*/__pycache__/
	rm -rf ./*/*/*/__pycache__/
	rm -rf ./*.pyc
	rm -rf ./*/*.pyc
	rm -rf ./*/*/*.pyc
	rm -rf ./*/*/*/*.pyc
	rm -rf ./pkg_init.egg-info/
	rm -rf ./dist/
	rm -rf ./build/

version:
	python3 tests/versiontest.py

pypi:
	python3 setup.py sdist && python3 setup.py bdist_wheel --universal && twine upload dist/*
