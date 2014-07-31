build:
	@echo "Building... Done."

id:
	@python q5-identify.py reidentify

query:
	@python q5-identify.py probability
