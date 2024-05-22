


# APIを起動する
api-run:
	cd server && poetry run uvicorn src.main:app --reload

# クライアントを起動する
client-run:
	cd client && npm run dev

# ライブサーバーを起動する
live-run:
	cd live_server && node index.js

