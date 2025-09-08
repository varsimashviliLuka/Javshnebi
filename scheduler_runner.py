from src import create_app
from src.scheduler import init_scheduler

app = create_app()

# Initialize scheduler only, no Flask server
init_scheduler(app)

# Keep container alive
import time
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    pass
