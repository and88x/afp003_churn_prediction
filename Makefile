PY=python 
.PHONY:
    run
    all
    install
    typehint
    lint
    black

run:
	#$(PY) -i src/main.py 
	jupyter-lab

all:
	@+make run

black:
	black -l 79 src/*.py

lint:
	pylint src/	

typehint:
	mypy --ignore-missing-imports src/		

install:
	pip install -U pandas==1.3.4 plotly==5.1.0 jupyterlab==3.2.2 ipywidgets==7.6.5 matplotlib==3.4.3
	pip install -U xgboost==1.4.2 scikit-learn==1.0.1
	conda install ipykernel
	$(PY) -m ipykernel install --user --name hackathon
