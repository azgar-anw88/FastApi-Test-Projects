from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

def authentication_user(credentials:HTTPBasicCredentials = Depends(security)):
    if credentials.username == 'testuser' and credentials.password == 'testpass':
        return True
    
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
@app.get("/basic-auth")
def get_basic_auth(credentials:HTTPBasicCredentials=Depends(authentication_user)):
    return {"message":"Authenticated Successfully"}

