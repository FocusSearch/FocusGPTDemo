cd web
call npm install
call npm run build
cd ..
copy "web\dist\public\index.html" "server\templates\index.html"

for %%a in (css, js, img, datafocus-chart) do (
    mkdir "server\static\%%a"
    del /f /s /q "server\static\%%a\*.*"
    xcopy /s /y "web\dist\%%a" "server\static\%%a"
)
python -m pip install -r server/requirements.txt

set DF_URL=https://cloud001.datafocus.ai
set DF_APP_TOKEN=********

python server/app.py
