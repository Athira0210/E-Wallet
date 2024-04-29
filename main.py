import json

from fastapi_sqlalchemy import DBSessionMiddleware
import uvicorn
from config.configuration import Configuration
from fastapi import FastAPI

from api.endpoints import router as endpoint_app



app = FastAPI()

# from dotenv import load_dotenv

# load_dotenv('.env')


configuration = Configuration()
database_uri=configuration.set_configuration()

#to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=database_uri)



# engine = create_engine(database_uri)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
 

with open('config.json', 'r') as config_file:
        config = json.load(config_file)
app_config = config.get('app', {})
host=app_config.get('host',None)
port=app_config.get('port',None)
app.include_router(endpoint_app)
 
if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)

