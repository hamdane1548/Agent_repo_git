@echo off

REM Activate the virtual environment
call .\.venv\Scripts\activate.bat

REM Install libraries for ZenML deployment
uv add anyio
uv add jinja2
uv add fastapi
uv add uvicorn
uv add secure
echo.
echo Installation completed.
pause