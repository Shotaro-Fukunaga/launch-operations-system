

.PHONY: run
run:
	uvicorn server.src.main:app --reload