## 主要依赖
- 后端：fastapi, uvicorn, pydantic,alembic
- 前端：Vite v6, Svelte v5, TypeScript, Tailwind CSS v4 

## 开发流程
需求 → 模型 → Schema → Service → API → OpenAPI → 页面（组件）

## 基于 OpenAPI 的开发模式
后端：fastapi 生成 openapi.json
前端：@hey-api/openapi-ts 生成 API 客户端
python scripts/export_openapi.py
cp openapi.json ../frontend/
npm run generate-api
project/
 ├── backend/
 │    └── openapi.json
 └── frontend/
 
## 后端增量更新
app/models/xxx.py     →  数据库结构
app/schemas/xxx.py    →  请求/响应格式
app/services/xxx.py   →  业务逻辑
app/api/v1/xxx.py     →  路由端点
app/api/v1/router.py  →  注册路由

## 前端增量更新
src/routes/dashboard/xxx/+page.svelte  →  新页面
src/components/biz/Xxx.svelte          →  业务组件
src/components/layout/DashboardSidebar.svelte  →  导航入口

## 前端文件结构
```
frontend/
├── .env.example
├── biome.json
├── openapi.json                 # 从后端导出的 OpenAPI
├── package-lock.json
├── package.json
├── playwright.config.ts
├── svelte.config.js
├── tsconfig.json
├── vite.config.ts
├── static/
│   ├── favicon.png
│   └── favicon.svg
├── tests/
│   ├── unit/                    # Vitest 单元测试
│   └── e2e/                     # Playwright E2E
└── src/
│   ├── app.d.ts
│   ├── app.html
│   ├── styles/
│   │   └── app.css              # Tailwind v4 入口 + 主题变量
│   ├── lib/
│   │   ├── api/                    # @hey-api/openapi-ts 生成
│   │   │   ├── client.ts           # fetch 客户端 + 拦截器（双 token 自动刷新）
│   │   │   ├── index.ts            # 入口，导出生成的 SDK
│   │   │   └── generated/          # 自动生成的类型和方法
│   │   ├── stores/
│   │   │   ├── auth.ts             # 用户认证状态（双 token 管理）
│   │   │   └── ui.ts               # 主题/语言/toast
│   │   ├── schemas/                # Zod 校验 schema
│   │   └── utils/
│   │       ├── api.ts              # SDK 结果/错误处理
│   │       ├── cn.ts               # clsx + tailwind-merge
│   │       ├── format.ts
│   │       ├── storage.ts
│   │       └── token-manager.ts    # 主动刷新 token（过期前 2 分钟）
│   ├── components/
│   │   ├── layout/
│   │   │   ├── PublicHeader.svelte
│   │   │   ├── PublicFooter.svelte
│   │   │   ├── PublicLayout.svelte
│   │   │   ├── DashboardHeader.svelte
│   │   │   ├── DashboardSidebar.svelte
│   │   │   └── DashboardLayout.svelte
│   │   ├── ui/                     # 基础组件库
│   │   │   ├── avatar/
│   │   │   ├── badge/
│   │   │   ├── button/
│   │   │   ├── card/
│   │   │   ├── checkbox/
│   │   │   ├── drawer/
│   │   │   ├── form/               # Felte 集成
│   │   │   ├── input/
│   │   │   ├── modal/
│   │   │   ├── pagination/
│   │   │   ├── select/
│   │   │   ├── skeleton/
│   │   │   ├── table/
│   │   │   ├── toast/
│   │   │   └── tooltip/
│   │   └── biz/
│   │       ├── LoginForm.svelte
│   │       ├── RegisterForm.svelte
│   │       ├── TodoFormModal.svelte
│   │       ├── UserMenu.svelte
│   │       ├── ThemeToggle.svelte
│   │       └── LangSwitch.svelte
│   ├── routes/
│   │   ├── +layout.svelte          # 根布局（i18n/theme provider）
│   │   ├── +layout.ts              # 全局 load
│   │   ├── +page.svelte            # / 官网首页
│   │   ├── +error.svelte           # 错误页
│   │   ├── auth/
│   │   │   ├── +layout.svelte      # 认证页布局
│   │   │   ├── login/
│   │   │   │   └── +page.svelte
│   │   │   └── register/
│   │   │       └── +page.svelte
│   │   └── dashboard/
│   │       ├── +layout.svelte      # 后台布局（需登录）
│   │       ├── +layout.ts          # 鉴权守卫
│   │       ├── +page.svelte        # 仪表盘首页
│   │       ├── profile/
│   │       │   └── +page.svelte
│   │       ├── todos/
│   │       │   └── +page.svelte
│   │       └── settings/
│   │           └── +page.svelte
```

## 后端文件结构
```
backend/
├── .env.example
├── alembic.ini
├── openapi.json                # 最新导出的 OpenAPI
├── requirements.txt
├── uploads/                    # 用户上传文件等
├── scripts/
│   ├── export_openapi.py           # 导出 openapi.json
│   └── seed.py                     # 开发数据填充
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI 入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # pydantic-settings 配置（JWT 60min/30day）
│   │   ├── logging.py              # structlog 配置
│   │   ├── rate_limit.py           # 速率限制
│   │   └── security.py             # JWT 双 token/密码哈希/token family
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                 # 依赖注入（get_db/get_current_user）
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py           # 汇总所有路由
│   │       ├── auth.py             # 登录/注册/刷新/登出
│   │       ├── todos.py
│   │       ├── users.py
│   │       └── health.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                 # SQLAlchemy Base + TimestampMixin
│   │   ├── refresh_token.py        # Refresh Token（支持轮换/撤销）
│   │   ├── todo.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Token/RefreshTokenRequest
│   │   ├── todo.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py                 # 登录/刷新逻辑
│   │   ├── refresh_token.py        # Token CRUD/撤销/清理
│   │   ├── todo.py
│   │   └── user.py
│   └── db/
│       ├── __init__.py
│       └── session.py              # 数据库连接
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                   # 迁移记录
└── tests/
    ├── conftest.py
    ├── api/
    │   ├── test_auth.py
    │   └── test_todos.py
    └── services/                   # 预留
```
