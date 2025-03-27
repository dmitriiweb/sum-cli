.PHONY: format
format:
	ruff format sum_cli
	ruff check sum_cli --select I --fix

.PHONY: lint
lint:
	ruff check sum_cli 
	mypy sum_cli
