migration:
ifndef name
	$(error You must provide a migration name, e.g., make migration-create name="add_users_table")
endif
	poetry run alembic revision --autogenerate -m "$(name)"
upgrade:
	poetry run alembic upgrade head
faststream:
	faststream run src.faststream:app