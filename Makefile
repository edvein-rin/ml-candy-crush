install: FORCE ## Intall requirements.
	@pip3 -r requirements.txt

run: FORCE ## Run the game.
	@python main.py

# https://www.gnu.org/software/make/manual/html_node/Force-Targets.html#Force-Targets
FORCE:
