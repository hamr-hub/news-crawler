# Backend 项目开发规范

> 项目类型: python
> 语言: Python
> 架构: FastAPI / Django
> 生成时间: 2026-03-20T07:19:49.110Z

## 1. 项目结构

```
src/
├── api/         # API 路由
├── models/      # 数据模型
├── services/    # 业务逻辑
├── repositories/# 数据访问
└── tests/       # 测试文件
```

## 2. 编码规范

- **Class**: PascalCase
- **Function**: snake_case
- **Constant**: UPPER_SNAKE_CASE
- **Module**: snake_case

## 3. 架构规范

分层架构：Controller → Service → Repository → Database

- **Controller**: 处理 HTTP 请求
- **Service**: 业务逻辑
- **Repository**: 数据访问
- **Model**: 数据模型

## 4. API 设计

RESTful 设计:
- GET /api/v1/users - 列表
- POST /api/v1/users - 创建
- GET /api/v1/users/{id} - 详情
- PUT /api/v1/users/{id} - 更新
- DELETE /api/v1/users/{id} - 删除

## 5. 数据库规范

- 所有表: id、created_at、updated_at 字段
- 表名: snake_case
- 字段名: snake_case
- 索引: 为常用查询字段添加

## 6. 测试规范

- **单元测试**: pytest
- **Mock**: unittest.mock
- **覆盖率**: >= 80%

---

*由 bootstrap-ai-flow enhanced 自动生成*
