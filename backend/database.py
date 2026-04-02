from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["illinibets"]

events_col = db["events"]
orders_col = db["orders"]
trades_col = db["trades"]