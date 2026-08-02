import pymongo
import os
import certifi

from utils import colors
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient


load_dotenv()

MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
uri = f"mongodb+srv://helphive_devanshee:{MONGO_PASSWORD}@helphivedb.togtz.mongodb.net/?retryWrites=true&w=majority&appName=HelpHiveDB"

client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print(f"{colors.OKGREEN}Connected to MongoDB{colors.ENDC}")
    
except Exception as e:
    print(f"{colors.FAIL}Error connecting to MongoDB{colors.ENDC}")
    print(f"{colors.FAIL}{e}{colors.ENDC}")

db = client["HelpHiveDB"]
