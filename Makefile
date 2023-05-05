.PHONY: build

build:
	python -m venv venv
	. venv/bin/activate && cd webapp && pip install -r requirements.txt
	. venv/bin/activate && cd webapp && python ./manage.py migrate
	. venv/bin/activate && cd webapp && python ./manage.py create_vector_db
run:
	. venv/bin/activate && cd webapp && ./manage.py runserver