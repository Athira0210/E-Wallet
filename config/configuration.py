import json
import os
                

class Configuration:
    def __init__(self,*args, **kwargs):
        self.set_configuration()
    def set_configuration(self):
        config_file = os.path.join(os.getcwd(),"config.json")
        with open(config_file,"r") as read_file:
            data=json.load(read_file)
        dev_data=data.get("db")
        configuration=type("ConfigClass",(),dev_data)
        db_username=configuration.username
        db_password=configuration.password
        port=configuration.port
        db_database=configuration.database
        return f"postgresql+psycopg2://{db_username}:{db_password}@localhost:{port}/{db_database}"
    
        


