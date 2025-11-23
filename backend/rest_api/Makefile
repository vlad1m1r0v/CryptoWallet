server:
	uvicorn src.server:create_app --factory --host 0.0.0.0 --port 8000 --workers 1
cli:
	python -m src.presentation.cli
certificates:
	@rm -rf certs
	@mkdir -p certs
	@openssl genrsa -out certs/jwt-private.pem 2048
	@openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
migration:
ifndef name
	$(error You must provide a migration name, e.g., make migration name="add_users_table")
endif
	poetry run alembic revision --autogenerate -m "$(name)"
migrate:
	poetry run alembic upgrade head