.PHONY: format
format:
	ruff format sum_cli
	ruff check sum_cli --fix
	ruff check sum_cli --select I --fix

.PHONY: lint
lint:
	mypy sum_cli
