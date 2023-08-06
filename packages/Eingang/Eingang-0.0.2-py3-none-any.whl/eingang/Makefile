.PHONY: static venv

venv:
	test -d venv || virtualenv venv -p python3
	ln -sf ./venv/bin/python

node: package.json
	npm install

static: node
	mkdir -p static
	ln -sf ../node_modules/bootstrap static/bootstrap
	ln -sf ../node_modules/jquery static/jquery

EINGANG_DIR = $(shell venv/bin/python -m eingang.Eingang)
TESTS_DIR = $(EINGANG_DIR)/tests

project: venv
	cp $(TESTS_DIR)/app.py .
	cp $(EINGANG_DIR)/config.py.in config.py
	cp $(TESTS_DIR)/create_user.py .
	cp $(TESTS_DIR)/delete_user.py .
	cp $(TESTS_DIR)/print_db.py .
	cp $(TESTS_DIR)/database.py .
	cp $(EINGANG_DIR)/package.json .
	cp -r $(TESTS_DIR)/templates .
	cp $(TESTS_DIR)/views.py .
	make node
	make static
	cp $(EINGANG_DIR)/static/* static
	venv/bin/python -m eingang.util config.py
