format:
	@poetry run ruff check --fix context_handler tests
	@poetry run ruff format context_handler tests

test:
	@poetry run pytest --verbose -p no:warning --cov=context_handler --cov-report=html --cov-report=xml:.artifacts/coverage.xml --junit-xml=.artifacts/tests.xml --cov-config=.coveragerc tests

check-vul:
	@echo "--> Check vulnerabilities"
	@poetry run bandit -r context_handler -c bandit.yaml