format:
	poetry run python -m ruff format


test:
	poetry run python manage.py test


local:
	python manage.py runserver