import pymongo
import os
import certifi

try:
    from utils import colors
except ImportError:
    class colors:
        OKGREEN = FAIL = ENDC = ''
from dotenv import load_dotenv  # type: ignore[import-untyped]
from pymongo.mongo_client import MongoClient


load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print(f"{colors.OKGREEN}Connected to MongoDB{colors.ENDC}")
    
except Exception as e:
    print(f"{colors.FAIL}Error connecting to MongoDB{colors.ENDC}")
    print(f"{colors.FAIL}{e}{colors.ENDC}")

db = client["HelpHiveDB"]
