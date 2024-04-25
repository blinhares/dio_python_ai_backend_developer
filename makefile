runapi: #rodar nosso api
	@uvicorn 5_Explorando_FastAPI.workout_api.main:app --reload
	