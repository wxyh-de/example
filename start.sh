#!/bin/bash

echo "🚀 MUD 游戏 Web 版启动脚本"
echo "================================"

case "$1" in
    backend)
        echo "🔧 启动后端服务..."
        cd backend
        if [ ! -d "venv" ]; then
            echo "📦 创建虚拟环境..."
            python3 -m venv venv
        fi
        source venv/bin/activate
        echo "📦 安装依赖..."
        pip install -r requirements.txt
        echo "🚀 启动 Flask 服务..."
        python app.py
        ;;
    
    frontend)
        echo "🌐 前端界面地址: $(pwd)/frontend/index.html"
        echo "请在浏览器中打开上述文件"
        if command -v python3 &> /dev/null; then
            echo "📡 正在启动简易HTTP服务器..."
            cd frontend
            python3 -m http.server 8000
        fi
        ;;
    
    docker)
        echo "🐳 构建 Docker 镜像..."
        docker build -t mud-game .
        echo "🚀 启动 Docker 容器..."
        docker run -d -p 5000:5000 --name mud-game mud-game
        echo "✅ 容器已启动"
        ;;
    
    stop-docker)
        echo "🛑 停止容器..."
        docker stop mud-game
        echo "🗑️ 删除容器..."
        docker rm mud-game
        ;;
    
    tests)
        echo "🧪 运行测试..."
        echo "后端服务需要先启动..."
        ;;
    
    all)
        echo "🚀 启动后端服务..."
        cd backend
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✅ 后端启动中..."
        python app.py &
        BACKEND_PID=$!
        cd ..
        
        echo "🌐 前端已就绪，请打开: $(pwd)/frontend/index.html"
        echo "⚠️  按 Ctrl+C 停止服务"
        wait $BACKEND_PID
        ;;
    
    *)
        echo "📋 使用方法:"
        echo "  $0 backend   - 启动后端服务"
        echo "  $0 frontend  - 查看前端"
        echo "  $0 docker    - Docker 部署"
        echo "  $0 all       - 启动全套（后台）"
        echo "  $0 tests     - 运行测试"
        ;;
esac