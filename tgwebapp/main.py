from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>Mini App — Привет, мир</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
          body { font-family: system-ui, Arial; padding: 20px; }
          button { font-size: 16px; padding: 8px 12px; border-radius: 6px; }
        </style>
      </head>
      <body>
        <h1>Привет, мир 👋</h1>
        <p>Это тестовая страница Mini App, запущенная на локальном сервере.</p>
        <button id="closeBtn">Закрыть WebApp</button>

        <script>
          const tg = window.Telegram?.WebApp;
          if (tg) {
            tg.expand();
            document.getElementById('closeBtn').onclick = () => tg.close();
          } else {
            // Если страница открыта в браузере (а не в Telegram)
            document.getElementById('closeBtn').onclick = () => alert('Откройте эту страницу через кнопку бота в Telegram');
          }
        </script>
      </body>
    </html>
    """