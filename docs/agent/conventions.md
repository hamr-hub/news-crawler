### 目录约定
- src/pages：页面组件
- src/components：通用组件
- src/hooks：自定义 React Hooks
- src/services 或 src/api：API 接口
- src/stores 或 src/store：状态管理（Redux/Zustand/Jotai）
- src/utils：工具函数
- src/types：TypeScript 类型定义
- src/styles：全局样式

### 代码片段复用（Snippets）
- **位置**：`.kwaipilot/snippets/` 目录（统一生成位置）
- **分类**：
  - `1-components/`：组件片段
  - `2-hooks/`：自定义 Hooks 片段
  - `3-context/`：Context API 片段
  - `4-routing/`：路由配置片段
  - `5-state/`：状态管理片段
  - `6-api/`：API 接口片段
  - `7-utils/`：工具函数片段
  - `8-tests/`：测试用例片段
- **命名规则**：`{分类}-{功能描述}.tsx`（如 `components-form-input.tsx`）
- **生成方式**：运行 `snippet-generator` skill 自动扫描代码库生成
- **使用场景**：
  - AI 生成代码时优先参考 snippets 中的模式
  - 新人学习项目代码规范
  - 代码 Review 时的参考标准
- **自动读取**：
  - `ai-flow` Stage 7 会自动读取 `.kwaipilot/snippets/README.md`
  - `iterate-from-plan-and-tests` 开始前会自动读取 snippets 目录
- **更新频率**：建议每次重大重构后重新生成一次

### 文案与国际化
- 所有字符串必须通过 i18n 库（如 react-i18next）包裹
- key 命名规则：`{模块}.{页面}.{字段}`（如 `auth.login.submit`）

### 样式
- **SCSS + convertStyles**（必须）
- **CSS 单位**：rpx/lrpx/nrpx（基于 750/414/828 设计稿）
- **禁止单位**：rem/em/vw/vh
- **换算规则**：rpx = 设计稿px × 2（750基准）
- **PostCSS**：自动转换 rpx → vw
- RN 不支持样式黑名单（维护列表）

### 跨端
- Platform.OS 作为分支入口
- Web/RN 行为差异的兜底策略

### 状态管理
- React Query：请求/缓存/失效策略
- Zustand：页面级与全局 store 分层

### 日志与埋点
- logger 统一入口
- 严禁记录敏感字段

---
