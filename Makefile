.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start-backend
start-backend: ## Starts only the backend
	@docker compose up -d --build

.PHONY: start-frontend-using-backend
start-frontend-using-backend: ## Start the frontend, using the backend
	@cd frontend/ && yarn ember server --proxy=http://localhost:8000

.PHONY: start-frontend
start-frontend: ## Start the frontend, using Mirage
	@cd frontend/ && yarn ember s
.PHONY: start
start: start-backend start-frontend-using-backend ## Start the application

.PHONY: lint-backend
lint-backend: ## Lint the backend
	@docker compose run --rm api sh -c "black --check . && flake8"

.PHONY: lint-backend-fix
lint-backend-fix: ## Lint and fix the backend
	@docker compose run --rm api sh -c "black . && isort ."

.PHONY: lint-frontend
lint-frontend: ## Lint the frontend
	@cd frontend/ && yarn lint

.PHONY: lint-frontend-fix
lint-frontend-fix: ## Lint and fix the frontend
	@cd frontend/ && yarn lint:fix

.PHONY: lint
lint: lint-backend lint-frontend ## Lint front- & backend

.PHONY: lint-fix
lint-fix: lint-backend-fix lint-frontend-fix ## Lint and fix front- & backend

.PHONY: test-backend
test-backend: ## Test the backend
	@docker compose run --rm api pytest --no-cov-on-fail --cov --create-db -vv

.PHONY: test-frontend
test-frontend: ## Test the frontend
	@cd frontend/ && yarn test

.PHONY: test
test: test-backend test-frontend ## Test front- & backend

.PHONY: api-bash
api-bash: ## Shell into the django container
	@docker-compose run --rm api bash

.PHONY: makemigrations
makemigrations: ## Make django migrations
	@docker compose run --rm api python ./manage.py makemigrations

.PHONY: migrate
migrate: ## Migrate django
	@docker compose run --rm api python ./manage.py migrate