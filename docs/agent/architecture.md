### 分层
- View（页面）
- Components（组件）
- Query（数据获取）
- Services（API & models）
- Common（桥接/日志/请求封装）
- Platform（跨端适配）

### 数据流
- 页面 -> useQuery hook -> services -> request wrapper

### 关键约束
- 接口模型统一出口
- 错误处理与兜底统一

---
