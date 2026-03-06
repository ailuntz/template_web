
### 本地
docker build -t ailuntz-xxx .

http://localhost:8080
健康检查：http://localhost:8080/api/health

### 后端定制 构建公网服务器镜像
```
docker buildx build \
  --platform linux/arm64,linux/amd64 \
  -t ailuntz/xxx:latest \
  -t ailuntz/xxx:v1.0.0 \
  -f Dockerfile.xxx \
  --push \
  .

docker buildx build \
  --platform linux/arm64 \
  -t ailuntz/xxx:latest \
  -t ailuntz/xxx:v1.0.0 \
  -f Dockerfile.xxx \
  --push \
  .
```

# 后端定制 公网服务器命令
```
docker run -d --name ailuntz-xxx \
  --restart=always \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e APP_NAME='Aurelius Research Exchange API' \
  -e DEBUG=false \
  -e DATABASE_URL='postgresql+psycopg://admin:admin782954@host.docker.internal:8401/database_xxx' \
  -e SECRET_KEY='42dc570dc68b917aeb985329cb68507045ce85d1e30c1ad8907bdc0ec40eb394' \
  -e JWT_SECRET_KEY='42dc570dc68b917aeb985329cb68507045ce85d1e30c1ad8907bdc0ec40eb394' \
  -e REGISTRATION_INSTITUTION_CODE='782954' \
  -e CORS_ORIGINS='["https://ailuntz.com","https://api.ailuntz.com"]' \
  -v ailuntz_xxx:/app/backend/uploads \
  ailuntz/ailuntz_xxx:latest \
  /bin/sh -lc "python -m alembic upgrade head && DEBUG=false python scripts/seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8080"
```

