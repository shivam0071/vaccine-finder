from threading import Thread
from vaccine import create_app
from vaccine import util

app = create_app()

if __name__ == "__main__":
    # Threads Here
    thread = Thread(target=util.vaccination_thread, daemon=True)
    thread.start()
    app.run("localhost", port=5000)
