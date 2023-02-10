.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start-backend
start-backend: ## Starts only the backend
	@docker-compose up -d --build
	@cd backend/;poetry run ./manage.py runserver

.PHONY: start-frontend-using-backend
start-frontend-using-backend: ## Start the frontend, using the API
	@cd frontend/; yarn ember server --proxy=http://localhost:8000

.PHONY: start-frontend-using-backend
start-frontend: ## Start the frontend, using Mirage
	@cd frontend/; yarn ember s

.PHONY: lint-backend
lint-backend: ## Lint the backend
	@cd backend/; poetry run black .; poetry run isort .; poetry run flake8; 

.PHONY: lint-frontend
lint-frontend: ## Lint the frontend
	@cd frontend/; yarn lint

.PHONY: lint
lint: lint-backend lint-frontend ## Lint front- & backend

.PHONY: test-backend
test-backend: ## Test the backend
	@cd backend/; poetry run pytest --no-cov-on-fail --cov

.PHONY: test-frontend
test-frontend: ## Test the frontend
	@cd frontend/; yarn test

.PHONY: test
test: test-backend test-frontend ## Test front- & backend

.PHONY: makemigrations
makemigrations: ## Make django migrations
	@cd backend/; poetry run ./manage.py makemigrations

.PHONY: migrate
migrate: ## Migrate django
	@cd backend/; poetry run ./manage.py migrate