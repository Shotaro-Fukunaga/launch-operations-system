# .envファイルの作成コマンド
make-env:
	@if [ -e .env ] ; then \
        echo ".env already exists"; \
    else \
		cp .env.example .env; \
	fi


run:
	poetry run uvicorn src.main:app --reload



poetry-setup:
	@echo "Setting up the project..."
	poetry --version || curl -sSL https://install.python-poetry.org | python3 -
	@echo "Poetry version: `poetry --version`"
	@echo "Configuring Poetry to create virtualenvs in the project directory..."
	@POETRY_VIRTUALENVS_IN_PROJECT=true poetry config virtualenvs.in-project
	@echo "Installing dependencies..."
	POETRY_VIRTUALENVS_IN_PROJECT=true poetry install