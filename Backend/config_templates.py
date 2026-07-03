import os
from fastapi.templating import Jinja2Templates

# Obtén la ruta absoluta al directorio raíz (Lynko/)
# Si tu estructura es Lynko/Backend y Lynko/Frontend:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "Frontend", "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)