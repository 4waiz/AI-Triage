#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs -d '\n')
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
