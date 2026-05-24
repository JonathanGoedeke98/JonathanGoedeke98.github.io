.PHONY: all data figures clean

all: data figures

data:
	python3 scripts/build_dataset.py

figures:
	python3 scripts/make_figures.py

clean:
	rm -f data/processed/*.csv data/processed/*.md
	rm -f outputs/figures/*.png
