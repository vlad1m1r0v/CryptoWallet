run_server:
	uvicorn src.main:create_app --factory --host 0.0.0.0 --port 8000 --workers 1
generate_certificates:
	@echo "Deleting old certificates directory (if it exists)..."
	@rm -rf certs
	@echo "Creating certificates directory..."
	@mkdir -p certs
	@echo "Generating private key..."
	@openssl genrsa -out certs/jwt-private.pem 2048
	@echo "Generating public key..."
	@openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
	@echo "Certificates created successfully in the 'certs' directory."
make_migration:
ifndef name
	$(error You must provide a migration name, e.g., make migration-create name="add_users_table")
endif
	poetry run alembic revision --autogenerate -m "$(name)"
run_migrations:
	poetry run alembic upgrade head