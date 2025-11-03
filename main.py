import threading
import webview
from app import create_app

flask_app = create_app()


def start_flask():
    flask_app.run(host='127.0.0.1', port=5000, debug=False)


flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

webview.create_window("Construction Inventory System",
                      "http://127.0.0.1:5000", width=1200, height=800)
webview.start()
