echo "Running flake8:"
poetry run flake8
echo "Running black:"
poetry run black .
