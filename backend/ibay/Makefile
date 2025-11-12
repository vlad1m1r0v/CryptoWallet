migration:
ifndef name
	$(error You must provide a migration name, e.g., make migration-create name="add_users_table")
endif
	poetry run alembic revision --autogenerate -m "$(name)"
upgrade:
	poetry run alembic upgrade head
worker:
	taskiq worker src.taskiq:broker src.taskiq
scheduler:
	taskiq scheduler src.taskiq:scheduler src.taskiq
faststream:
	faststream run src.faststream:app