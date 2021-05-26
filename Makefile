
.PHONY: wheel upload clean

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    PYEXE := py -3
else
    PYEXE := python3
endif


wheel:
	$(PYEXE) setup.py bdist_wheel

upload:
	twine upload dist/*.whl

clean:
	rm -rf build dist