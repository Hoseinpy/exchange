install:
	pip install -r req.txt

makemg:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

runserver:
	python3 manage.py runserver