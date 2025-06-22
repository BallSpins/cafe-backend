#!/bin/bash
python wait_for_db.py
python migrate.py
uvicorn server:app --host 0.0.0.0 --port 8000