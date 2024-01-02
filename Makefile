install: FORCE ## Intall requirements.
	@pip3 install -r requirements.txt

run: FORCE ## Run the game.
	@python main.py

test: FORCE ## Run tests.
	$(MAKE) -C tests all

# https://www.gnu.org/software/make/manual/html_node/Force-Targets.html#Force-Targets
FORCE:
