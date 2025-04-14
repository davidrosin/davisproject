from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = ["RS256"]

app = FastAPI()
security = HTTPBearer()

def get_public_key():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    return jwks["keys"]

def verify_jwt(token: str):
    jwks = get_public_key()
    unverified_header = jwt.get_unverified_header(token)
    
    for key in jwks:
        if key["kid"] == unverified_header["kid"]:
            try:
                payload = jwt.decode(
                    token,
                    jwt.algorithms.RSAAlgorithm.from_jwk(key),
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f"https://{AUTH0_DOMAIN}/"
                )
                return payload
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(status_code=401, detail="Key not found")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return verify_jwt(token)

@app.get("/value")
def get_value(user: dict = Depends(get_current_user)):
    return {"value": 42}
