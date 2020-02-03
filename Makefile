init:
	pip install -r requirements.txt
	python bidijkstra/setup.py build_ext --build-lib=./bidijkstra/
