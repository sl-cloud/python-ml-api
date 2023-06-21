#!/usr/bin/python

import pandas as pd
import pickle
import os

#from dotenv import load_dotenv
from dotenv import dotenv_values
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Any, List

# Load environment variables from .env file
#load_dotenv()

class PredictionService:
    @staticmethod
    def predict(data: str) -> List[float]:
        # Prediction Model
        filename = 'model.pkl'

        # Load the saved model from the file
        with open(filename, 'rb') as file:
            loaded_model = pickle.load(file)

        cli_pattern = list(data)
        new_data = pd.DataFrame([cli_pattern])

        # Make predictions using the loaded model
        predictions = loaded_model.predict(new_data)
        probabilities = loaded_model.predict_proba(new_data)

        # Convert predictions and probabilities to Python lists
        predictions = predictions.tolist()
        probabilities = probabilities.tolist()

        return predictions[0], probabilities[0][predictions[0]]


class AuthenticationService:
    #SECRET_KEY = os.getenv("SECRET_KEY")
    env_vars = dotenv_values(".env")
    USERNAME = env_vars.get("USERNAME")
    SECRET_KEY = env_vars.get("SECRET_KEY")
    ALGORITHM = "HS256"

    @staticmethod
    def authenticate(token: str) -> str:
        try:
            payload = jwt.decode(token, AuthenticationService.SECRET_KEY, algorithms=[AuthenticationService.ALGORITHM])
            username: str = payload.get("sub")
            if username != AuthenticationService.USERNAME:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials for user: " + username,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return username
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Create the FastAPI application
app = FastAPI()

# OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/predict/")
async def predict_endpoint(data: str, token: str = Depends(oauth2_scheme)) -> Any:
    # Authenticate the user
    AuthenticationService.authenticate(token)

    # Once token is verified, perform prediction
    try:
        return {"prediction": PredictionService.predict(data)[0], "probabilities": PredictionService.predict(data)[1]}
    except Exception as e:
        # Handle the exception
        error_message = str(e)
        return {"error": error_message}

# Run this script with: nohup uvicorn api:app --port 8008 --reload > server.log 2>&1 & //Live
