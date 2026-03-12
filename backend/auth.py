from firebase_admin import auth as firebase_auth
from fastapi import HTTPException, Header

def verify_token(authorization: str = Header(...)):
    """
    Every protected route calls this.
    Frontend sends: Authorization: Bearer <firebase_id_token>
    We verify it here with Firebase Admin.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header format")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded  # has uid, email, etc.
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token expired, please log in again")
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Auth error: {str(e)}")


def get_user_by_uid(uid: str):
    """Look up a Firebase user by their UID."""
    try:
        return firebase_auth.get_user(uid)
    except firebase_auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")