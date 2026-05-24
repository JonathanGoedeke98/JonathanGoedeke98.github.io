.PHONY: all data train figures test clean

all: data train figures test

data:
	python3 scripts/download_data.py

train:
	python3 scripts/train.py

figures:
	python3 scripts/visualise.py

test:
	python3 -m pytest tests/ -v

clean:
	rm -rf data/raw/ models/*.pkl outputs/figures/*.png outputs/tables/*.csv
