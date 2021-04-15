
run:
	python3 manage.py runserver 0.0.0.0:8000

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate --run-syncdb

flush:
	python3 manage.py migrate ring zero
	python3 manage.py migrate ring 

