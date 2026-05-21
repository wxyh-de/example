@echo off
chcp 65001 >nul
echo 🚀 MUD 游戏 Web 版启动脚本
echo ================================
echo.

if "%1"=="backend" goto backend
if "%1"=="frontend" goto frontend
if "%1"=="docker" goto docker
if "%1"=="all" goto all
if "%1"=="tests" goto tests

echo 📋 使用方法:
echo   start.bat backend  - 启动后端服务
echo   start.bat frontend - 查看前端
echo   start.bat docker   - Docker 部署
echo   start.bat all      - 启动全套
echo   start.bat tests    - 运行测试
goto end

:backend
echo 🔧 启动后端服务...
cd backend
if not exist venv (
    echo 📦 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate
echo 📦 安装依赖...
pip install -r requirements.txt
echo 🚀 启动 Flask 服务...
python app.py
cd ..
goto end

:frontend
echo 🌐 前端界面地址: %CD%\frontend\index.html
echo 请在浏览器中打开上述文件
echo.
echo 📡 启动简易HTTP服务器...
cd frontend
python -m http.server 8000
cd ..
goto end

:docker
echo 🐳 构建 Docker 镜像...
docker build -t mud-game .
echo 🚀 启动 Docker 容器...
docker run -d -p 5000:5000 --name mud-game mud-game
echo ✅ 容器已启动
goto end

:all
echo 🚀 启动全套服务...
echo.
echo 🔧 启动后端服务...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
start "MUD Backend" cmd /k "python app.py"
cd ..

echo 🌐 前端已就绪，请打开: %CD%\frontend\index.html
echo.
goto end

:tests
echo 🧪 运行测试...
echo 请先确保后端服务已启动
echo.
python -m unittest test_mud_game.py
goto end

:end