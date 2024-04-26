from fastapi import FastAPI

###adicionanod ao path o caminho relativo do projeto
from pathlib import Path
import sys
APP_BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(APP_BASE_DIR))

from workout_api.src.config.routers import api_router

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)
