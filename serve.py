import bjoern
from app import app

host='0.0.0.0'
port=5008

print("Bjoern is up and running")
bjoern.run(app,host,port)