.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: api-bash
api-bash: ## Shell into the API
	@docker-compose run --rm api bash

.PHONY: api-lint
api-lint: ## Lint the backend
	@docker compose run --rm api sh -c "black --check . && flake8"

.PHONY: api-lint-fix
api-lint-fix: ## Lint and fix the API
	@docker compose run --rm api sh -c "black . && isort ."

.PHONY: api-start
api-start: ## Start the API
	@docker compose up db api -d --build

.PHONY: api-test
api-test: ## Test the API
	@docker compose run --rm api pytest --no-cov-on-fail --cov -vvv -s

.PHONY: cleanup
cleanup: ## Cleanup all docker containers, images, volumes and networks from the project
	@docker compose down -v --timeout 0

.PHONY: ember-lint
ember-lint: ## Lint ember
	@cd frontend/ && yarn lint

.PHONY: ember-lint-fix
ember-lint-fix: ## Lint and fix ember
	@cd frontend/ && yarn lint:fix

.PHONY: ember-start
ember-start: ## Start ember using Mirage
	@cd frontend/ && yarn ember s

.PHONY: ember-start-using-api
ember-start-using-api: ## Start ember using the API
	@cd frontend/ && yarn && yarn ember server --proxy=http://localhost:8000

.PHONY: ember-test
ember-test: ## Test ember
	@cd frontend/ && yarn test

.PHONY: lint
lint: api-lint ember-lint ## Lint the API and ember

.PHONY: lint-fix
lint-fix: api-lint-fix ember-lint-fix ## Lint and fix the API and ember

.PHONY: makemigrations
makemigrations: ## Make django migrations
	@docker compose run --rm api python ./manage.py makemigrations

.PHONY: migrate
migrate: ## Migrate django
	@docker compose run --rm api python ./manage.py migrate

.PHONY: migrate-zero
migrate-zero: ## Unapply all django migrations
	@docker compose run --rm api python ./manage.py migrate outdated zero

.PHONY: start
start: api-start ember-start-using-api ## Start the application

.PHONY: test
test: api-test ember-test ## Test the API and ember
