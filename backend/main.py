from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from firebase_config import initialize_firebase
from auth import verify_token

# Initialize Firebase when app starts
initialize_firebase()

app = FastAPI()

# Allow your frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "PredMarket API is running"}


@app.get("/protected")
def protected_route(user=Depends(verify_token)):
    """
    Test route — only works if you send a valid Firebase token.
    Your frontend hits this after login to confirm auth works.
    """
    return {
        "message": f"Welcome, {user['email']}",
        "uid": user["uid"]
    }


@app.get("/profile")
def get_profile(user=Depends(verify_token)):
    """Returns the logged-in user's basic info."""
    return {
        "uid": user["uid"],
        "email": user["email"],
        "name": user.get("name", ""),
    }