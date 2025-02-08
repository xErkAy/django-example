manage = python src/manage.py

fmt:
	ruff format src
	toml-sort pyproject.toml


check:
	ruff check src --fix --unsafe-fixes
	mypy src
	$(manage) makemigrations --check --no-input --dry-run


lint:
	make fmt
	make check
