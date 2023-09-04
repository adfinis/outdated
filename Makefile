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

.PHONY: api-shell
api-shell: ## Open django shell
	@docker-compose exec api ./manage.py shell

.PHONY: api-start
api-start: ## Start the API
	@docker compose up db api -d --build

.PHONY: api-test
api-test: ## Test the API
	@docker compose run --rm api pytest --no-cov-on-fail --cov -vvv -s

.PHONY: build
build: ## Build the containers
	@docker compose build

.PHONY: cleanup
cleanup: ## Cleanup all docker containers, images, volumes and networks from the project
	@docker compose down -v --timeout 0

.PHONY: ember-lint
ember-lint: ## lint ember
	@cd ember && yarn lint

.PHONY: ember-lint-fix
ember-lint-fix: ## lint and fix ember
	@cd ember && yarn lint:fix

.PHONY: ember-start
ember-start: ## Start ember
	@docker compose up ember --build -d

.PHONY: ember-start-livereload
ember-start-livereload: ## Start ember with livereload
	@docker compose up -d --build db keycloak api caddy && cd ember && yarn && yarn start-proxy

.PHONY: ember-test
ember-test: ## test the frontend
	@cd ember && yarn test:ember

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
	@docker compose run --rm api python ./manage.py migrate user zero

.PHONY: keycloak-import
keycloak-import: ## Import keycloak configuration
	@docker compose exec keycloak /opt/keycloak/bin/kc.sh import --override true --file /opt/keycloak/data/import/config.json

.PHONY: keycloak-export
keycloak-export: ## Export keycloak configuration
	@docker compose exec keycloak /opt/keycloak/bin/kc.sh export --file /opt/keycloak/data/import/config.json

.PHONY: start
start: ## Start the application
	@docker compose up -d --build

.PHONY: test
test: api-test ember-test ## Test the API and ember