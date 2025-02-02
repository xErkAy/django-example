manage = poetry run python src/manage.py

fmt:
	poetry run ruff format src
	poetry run toml-sort pyproject.toml


check:
	poetry run ruff check src --fix --unsafe-fixes
	poetry run mypy src
	$(manage) makemigrations --check --no-input --dry-run


lint:
	make fmt
	make check
