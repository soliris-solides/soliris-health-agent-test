import json
from fastapi import APIRouter, Form, HTTPException, status, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path

router = APIRouter(prefix="/auth", tags=["auth"])

# Configurações JWT
SECRET_KEY = "XG5FzQv3ePq1rTyK9hWbB6mNlZoY7sD2RjU8x4S0gPw"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Caminho para o JSON de usuários
USERS_FILE = Path(__file__).parent / "users.json"

# Funções auxiliares
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Rota de login
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            token = create_access_token(data={"sub": username})
            return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Nome de usuário ou senha inválidos")

# Rota protegida de exemplo
@router.get("/me")
def get_me(username: str = Depends(verify_token)):
    return {"username": username}
