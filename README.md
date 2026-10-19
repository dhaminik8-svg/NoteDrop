# NoteDrop

A temporary text and code snippet sharing web application built using Flask and SQLite.

## Features
- Unique shareable links
- Configurable expiry duration
- Maximum view limits
- Lightweight SQLite storage
- Health-check endpoint

## Technology Stack
- Python and Flask
- HTML and CSS
- SQLite
- Git and GitHub
- Jenkins, Docker and Kubernetes

## Run Locally

    py -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe app.py

Open http://127.0.0.1:5000 in your browser.

## Health Check

Open http://127.0.0.1:5000/health
