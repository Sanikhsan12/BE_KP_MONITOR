import yaml
from app.main import app

def generate_swagger():
    openapi_schema = app.openapi()
    
    with open("swagger.yaml", "w") as f:
        yaml.dump(openapi_schema, f, sort_keys=False)
        
if __name__ == "__main__":
    generate_swagger()
    print("swagger.yaml berhasil dibuat!")
