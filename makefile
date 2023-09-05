.PHONY: all install-requirements clean-db init-db start-backend install-frontend start-frontend

init: install-requirements clean-db init-db start-backend install-frontend start-frontend
start: start-backend install-frontend start-frontend
setup-server:
	@echo "Updating package lists..."
	sudo apt-get update
	@echo "Installing system dependencies..."
	sudo apt-get install -y python3-pip
	curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
	sudo apt-get install -y nodejs

install-requirements:
	@echo "Installing Python requirements..."
	pip install -r requirements.txt

delete-db:
	@echo "Cleaning up database..."
	cd src && rm -f sql_app.db


init-db:
	@echo "Initializing database..."
	cd src && python database.py


start-backend:
	@echo "Starting backend service..."
	cd src && uvicorn app:app --reload &


install-frontend:
	@echo "Installing frontend dependencies..."
	cd social_media_project && npm install

start-frontend:
	@echo "Starting frontend..."
	cd social_media_project && npm run serve
