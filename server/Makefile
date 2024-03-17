# pip listの内容をrequirements.txtに移す
.PHONY: pip-freeze
pip-freeze:
	pip freeze > requirements.txt

.PHONY: pip-uninstall
pip-uninstall:
	cat requirements.txt | xargs -n 1 pip uninstall -y

.PHONY: run
run:
	uvicorn src.main:app --reload



# ************* DataBase関連のショートカット **************

# マイグレーションファイルの自動生成
.PHONY: autogenerate
autogenerate:
	$(eval NAME := $(filter-out $@,$(MAKECMDGOALS)))
	cd src/database && alembic -c alembic.ini revision --autogenerate -m "$(NAME)"
%:
	@:

# マイグレート
migrate:
	cd src/database && alembic upgrade head

# 全てのマイグレートをdropする
rollback:
	cd src/database && alembic downgrade base

# 一個前のマイグレートをdropする
downgrade:
	cd src/database && alembic downgrade -1
# ************* ************************** **************


