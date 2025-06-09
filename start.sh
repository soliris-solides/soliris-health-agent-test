#!/bin/bash

# Inicia o FastAPI na porta configurada pelo Heroku ou Railway
uvicorn main:app --host 0.0.0.0 --port $PORT