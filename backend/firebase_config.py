import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    # Only initialize once
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)