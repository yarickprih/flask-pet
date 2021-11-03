from project import create_app
import os

app = create_app(str(os.getenv("CONFIG")))
