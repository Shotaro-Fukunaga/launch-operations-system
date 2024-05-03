

# fastapi uvicornサーバーを起動する
.PHONY: run
run:
	cd server && uvicorn src.main:app --reload

# Run npm dev in client
.PHONY: rc
rc:
	cd client && npm run dev

# Run node index.js in live_server
.PHONY: run-live-server
run-live-server:
	cd live_server && node index.js


.PHONY: run-all
run-all:
	@echo "Starting all servers..."
	@cd client && npm run dev &
	@cd live_server && node index.js &
	@cd server && uvicorn src.main:app --reload
	@echo "All servers started. Use 'make stop-all' to stop all servers."


.PHONY: stop-all
stop-all:
	@echo "Stopping all servers..."
	@-pkill -f uvicorn
	@-pkill -f npm
	@-pkill -f node
	@echo "All servers have been stopped."