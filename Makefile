format:
	poetry run python -m ruff format
	poetry run python -m ruff check --fix 


test:
	poetry run python manage.py test


local:
	poetry run python manage.py runserver