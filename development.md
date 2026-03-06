## 创建环境 （已存在则可省略）
conda create -n backend python=3.10 -y
conda activate backend
cd backend
pip install -r requirements.txt

## 后端初始化
cp .env.example .env #修改数据库信息
alembic upgrade head #新数据库则先升级数据库
python scripts/seed.py

## 前端初始化
cd frontend
cp .env.example .env  #修改VITE_API_URL
npm install
npx playwright install chromium

## 后端启动
cd backend
conda activate backend
uvicorn app.main:app --reload
## 前端启动
cd frontend
npm run dev

## 增量更新后
alembic revision --autogenerate -m "New migration"  #如果修改了模型，再生成新的迁移
alembic upgrade head #再升级数据库
python scripts/export_openapi.py
cp openapi.json ../frontend/
npm run generate-api

# 检查和测试
npm run check #前端类型检查
python -m ruff check . #后端 Ruff lint 
python -m mypy app --ignore-missing-imports #后端 Mypy 类型检查
python -m pytest tests/ -v #后端 Pytest
npm run test:e2e #前端 E2E 测试 (需要后端服务运行)
