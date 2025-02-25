cd web
@REM call npm install
@REM call npm run build
cd ..
copy "web\dist\index.html" "server\templates\index.html"

for %%a in (css, js, img, datafocus-chart) do (
    mkdir "server\static\%%a"
    del /f /s /q "server\static\%%a\*.*"
    xcopy /Y "web\dist\%%a" "server\static\%%a"
)
@REM python -m pip install -r server/requirements.txt

set DF_URL="https://cloud001.datafocus.ai"
set DF_APP_TOKEN="abcdef"

python server/app.py
