runapi: #rodar nosso api
	@uvicorn 5_Explorando_FastAPI.workout_api.main:app --reload

create-migrations: #revisar as migracoes
	@ cd 5_Explorando_FastAPI/ ; alembic revision --autogenerate 

run-migrations: #realizar migracoes
	@cd 5_Explorando_FastAPI/ ;  alembic upgrade head

ls:
	@cd .. ; ls
	