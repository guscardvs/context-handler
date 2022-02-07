format:
	@pdm run black .
	@pdm run isort .
	@pdm run autoflake --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys --expand-star-imports -ir .

test:
	@pdm run pytest --verbose -p no:warning --cov=context_handler --cov-report=html --cov-report=xml:.artifacts/coverage.xml --junit-xml=.artifacts/tests.xml --cov-config=.coveragerc tests

check-vul:
	@echo "--> Check vulnerabilities"
	pdm run bandit -r context_handler -c bandit.yaml