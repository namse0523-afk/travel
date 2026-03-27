@echo off
cd /d "%~dp0"
python -m streamlit run "%~dp0chatbot_app.py" --server.port 8502 --server.headless true
