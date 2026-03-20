# AGENTS.md

> **⚠️ AI 助手请注意**：
> 这是本项目**唯一的、权威的入口文件**。
> 在执行任何任务前，请优先阅读本文档以理解项目上下文。
> 
> **作用**：
> 1. 提供自定义指令，指导 AI 行为
> 2. 确保项目中代码生成的一致性
> 3. 定义项目的架构、规范和最佳实践

---

## 📍 文档导航

### 📚 核心规范（必读）
- **[本文档（AGENTS.md）](AGENTS.md)** - 项目概览、技术栈、架构设计 ⭐ **优先阅读**
- **[开发规范（rules.md）](.codeflicker/rules.md)** - 编码规范、命名约定、最佳实践
- **[开发命令（development_commands.md）](docs/agent/development_commands.md)** - 所有开发、构建、测试命令
- **[架构设计（architecture.md）](docs/agent/architecture.md)** - 系统架构、目录结构、设计模式

### 🛠️ 开发工作流
- **[需求到代码指南（requirement-to-code-guide.md）](docs/agent/requirement-to-code-guide.md)** - 完整开发工作流 SOP
- **[代码约定（conventions.md）](docs/agent/conventions.md)** - 文件命名、导入顺序、错误处理等约定

### 🗂️ 资产与档案
- **[任务卷宗（docs/tasks/）](docs/tasks/)** - 所有需求的 requirement/tech/plan 文档
- **[研发资产（docs/research/）](docs/research/)** - rd-assets.yaml 等资产清单
- **[代码片段（.codeflicker/snippets/）](.codeflicker/snippets/)** - 可复用的标准代码模板 ✅ **已从项目提取**

---

## 📦 项目概览（WHAT）

### 基本信息

| 项目 | 信息 |
|------|------|
| **项目类型** | python |
| **编程语言** | python |
| **CSS 框架** | Unknown |
| **包管理器** | npm |
| **构建工具** | 无 |
| **测试框架** | unittest |

| **生成时间** | 2026-03-20T07:19:49.112Z |

### 技术栈

#### 核心框架


#### 开发工具


#### 关键依赖


### 核心功能

本项目的核心功能包括：

- 用户认证和授权
- 数据展示和交互
- 表单处理和验证
- 状态管理
- 路由导航

*（建议手动补充项目特定功能）*


### 📚 项目代码资产（从实际代码提取）

本项目包含 **0 个**真实代码片段，覆盖以下类别：

- **说明**
- **如何触发提取**
- **提取后的目录结构**

**使用方式**：
- 查看 [`.codeflicker/snippets/README.md`](.codeflicker/snippets/README.md) 获取完整索引
- 在生成代码时，**优先参考这些片段**以保持风格一致



---

## 🎯 核心原则（Core Principles）

### 🔴 绝对红线（MUST - 必须遵守）

这些规则是**不可协商的底线**，违反将导致 PR 被拒绝：

#### 1. 类型安全
   - ✅ 使用 JSDoc 注释标注函数参数和返回值类型
   - ✅ 明确标注可选参数


#### 2. 代码质量
   - ✅ 新增代码必须通过 `flake8` 检查（**无 error，warning 需修复**）
   - ❌ **禁止在生产代码中使用 `console.log`**（使用统一的日志工具或调试工具）
   - ✅ 提交前必须运行：
     ```bash
     flake8
     pytest --tb=short -q
     ```

#### 3. 测试覆盖
   - ✅ **新增功能必须包含测试用例**（单元测试或集成测试）
   - ✅ 公共工具函数必须有单元测试
   - ✅ 关键业务逻辑测试覆盖率 **≥ 80%**
   - ✅ 修复 Bug 时，先编写**重现问题的测试**，再修复代码
   
   **测试框架**：unittest

#### 4. 安全合规
   - ❌ **严禁在代码中硬编码敏感信息**（API Key、密码、Token 等）
   - ❌ **严禁在日志中记录敏感数据**（密码、令牌、个人信息等）
   - ✅ 用户输入必须进行验证和清理（防止 XSS、SQL 注入）
   - ✅ 使用环境变量管理配置：
     ```javascript
     // ✅ 推荐
     const API_KEY = process.env.VITE_API_KEY;
     
     // ❌ 禁止
     const API_KEY = 'sk-1234567890abcdef';
     ```

#### 5. CSS/样式规范
   - **框架**：Unknown
   - **文件扩展名**：`.css`
   - **导入方式**：
     ```javascript
     import './index.css';
     ```

   - ❌ **禁止内联样式**（除非动态计算）
   - ❌ **禁止随意修改全局样式**（使用 scoped 样式或 CSS Modules）

#### 6. 版本控制
   - ✅ 提交信息必须遵循 **Conventional Commits** 规范：
     ```
     <type>(<scope>): <subject>
     
     <body>
     
     <footer>
     ```
     类型（type）：
     - `feat:` 新功能
     - `fix:` 修复 bug
     - `docs:` 文档更新
     - `style:` 代码格式（不影响功能）
     - `refactor:` 重构
     - `test:` 测试相关
     - `chore:` 构建/工具链
   
   - ✅ **禁止直接提交到主分支**（通过 PR 合并）
   - ✅ **禁止提交未完成的代码**（使用 feature flag 或 WIP PR）

### 🟢 推荐实践（SHOULD - 强烈建议）

#### 1. TDD（测试驱动开发）
   - 优先编写测试用例，再实现功能代码
   - 使用测试框架的 watch 模式进行开发
   - 保持测试简洁、可读、可维护

#### 2. 组件设计原则
   - 遵循**单一职责原则**（SRP）
   - 优先使用**函数式组件**
   - 避免过度封装，保持组件简洁
   - 组件拆分原则：单个组件 < 200 行
   
   **示例**：
   ```javascript
   interface ButtonProps {
     label: string;
     onClick: () => void;
     variant?: 'primary' | 'secondary';
   }
   
   export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
     return (
       <button className={`btn btn-${variant}`} onClick={onClick}>
         {label}
       </button>
     );
   }
   ```


#### 3. 状态管理
   - **本地状态**：使用 `useState`
   - **派生状态**：使用 `useMemo`
   - **副作用**：使用 `useEffect`
   - **全局状态**：使用 **Zustand** 或 **Context API**
   - **服务端状态**：使用 **TanStack Query / React Query**（不要在全局状态中存储）


#### 4. 代码复用
   - 提取可复用逻辑为 Custom Hooks（组合式函数）
   - 提取可复用 UI 为组件
   - **优先参考** `.codeflicker/snippets/` 中的代码片段

#### 5. 性能优化
   - 使用 `React.memo` 避免不必要的重渲染
   - 使用 `useMemo` 和 `useCallback` 缓存计算结果和函数
   - 大列表使用虚拟滚染（`react-window` 或 `react-virtualized`）
   - 图片使用懒加载
   - 路由懒加载：`React.lazy(() => import('./Home'))`


#### 6. 错误处理
   - **永远不要忽略错误**
   - 使用 try-catch 包裹异步操作
   - 提供友好的错误提示
   - 记录错误到监控系统
   
   **示例**：
   ```javascript
   // ✅ 推荐
   async function fetchUser(id) {
     try {
       const response = await fetch(`/api/users/${id}`);
       if (!response.ok) {
         throw new Error(`HTTP ${response.status}: ${response.statusText}`);
       }
       return await response.json();
     } catch (error) {
       console.error('Failed to fetch user:', error);
       // 上报到监控系统
       reportError(error);
       throw error;
     }
   }
   
   // ❌ 禁止
   async function fetchUser(id) {
     const response = await fetch(`/api/users/${id}`);
     return await response.json();
   }
   ```

---

## 🏗️ 项目架构（HOW）

### 目录结构

```
Project Root
├── src/                         # 源代码
│   ├── components/              # UI 组件
│   │   ├── ui/                 # 基础组件（Button, Input 等）
│   │   └── features/           # 业务组件
│   ├── pages/                  # 页面组件
│   ├── hooks/              # Custom Hooks（逻辑复用）
│   ├── utils/                   # 工具函数
│   ├── services/                # API 服务
│   ├── store/                   # 状态管理
│   ├── types/                   # TypeScript 类型定义 (如使用 TS)
│   ├── styles/                  # 样式文件
│   ├── config/                  # 配置文件
│   └── App.tsx            # 根组件
│
├── .codeflicker/                  # AI Flow 配置
│   ├── codeflicker.json             # 项目配置
│   ├── rules.md                 # 开发规范
│   ├── snippets/                # 代码片段
│   └── skills/                  # AI Skills
│
├── docs/                        # 项目文档
│   ├── agent/                   # AI 开发约定
│   │   ├── architecture.md              # 架构说明
│   │   ├── conventions.md               # 代码约定
│   │   └── development_commands.md      # 开发命令
│   ├── tasks/                   # 任务文档
│   │   └── <taskId>/
│   │       ├── requirement.md           # 需求文档
│   │       ├── tech-solution.md         # 技术方案
│   │       └── plan.md                  # 实施计划
│   └── research/                # 研发资产沉淀
│       ├── rd-assets.md                 # 资产报告
│       └── rd-assets.yaml               # 机读资产数据
│
├── tests/                       # 测试文件
│   ├── unit/                    # 单元测试
│   ├── integration/             # 集成测试
│   └── e2e/                     # 端到端测试
│
├── AGENTS.md                    # ⭐ 本文档（项目入口）
├── .env                         # 环境变量
├── .gitignore                   # Git 忽略规则
├── package.json                 # 项目依赖
└── js           # 构建配置
```

### 核心约定

#### 1. 文件命名
- **组件文件**：PascalCase（如 `UserProfile.tsx`）
- **Hooks 文件**：camelCase，以 `use` 开头（如 `useAuth.ts`）
- **工具函数文件**：camelCase（如 `formatDate.ts`）
- **常量文件**：camelCase 或 UPPER_SNAKE_CASE（如 `constants.ts` 或 `API_KEYS.ts`）
- **测试文件**：与源文件同名 + `.test.js` 或 `.spec.js`

#### 2. 导入顺序
```javascript
// 1. 外部依赖（第三方库）
import React, { useState } from 'react';

// 2. 内部模块（别名导入）
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';

// 3. 相对路径导入
import { formatDate } from '../utils/formatDate';

// 4. 样式文件
import './index.css';

// 5. 类型定义（仅 TypeScript，放在最后）

```

#### 3. 路径别名

本项目配置了以下路径别名：

```json
{
  "@/": "src/",
  "@components/": "src/components/",
  "@utils/": "src/utils/",
  "@hooks/": "src/hooks/"
}
```

**使用示例**：
```javascript
// ✅ 推荐（使用别名）
import { Button } from '@/components/Button';
import { formatDate } from '@utils/formatDate';

// ❌ 避免（相对路径过深）
import { Button } from '../../../components/Button';
```

### 设计模式

#### 1. 组件组合模式（Composition Pattern）

使用 Custom Hooks 组织逻辑：

```typescript
import { useState, useEffect } from 'react';
import { useUser } from '@/hooks/useUser';

function UserList() {
  // 组合多个 hooks
  const { user, loading, fetchUser } = useUser();
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredItems = useMemo(() => {
    return items.filter(item => 
      item.name.includes(searchTerm)
    );
  }, [items, searchTerm]);
  
  return (
    // JSX
  );
}
```

#### 2. 容器/展示组件模式（Container/Presentational Pattern）

- **容器组件**：负责数据获取和业务逻辑
- **展示组件**：只负责 UI 渲染，通过 props 接收数据

#### 3. 高阶组件模式（HOC Pattern）

```typescript
function withAuth<P extends object>(
  Component: React.ComponentType<P>
) {
  return function AuthenticatedComponent(props: P) {
    const { isAuthenticated } = useAuth();
    
    if (!isAuthenticated) {
      return <Redirect to="/login" />;
    }
    
    return <Component {...props} />;
  };
}
```

#### 4. 单例模式（Singleton Pattern）

用于 API 客户端、配置管理等：

```typescript
// services/apiClient.ts
class ApiClient {
  private static instance: ApiClient;
  
  private constructor() {
    // 初始化
  }
  
  static getInstance(): ApiClient {
    if (!ApiClient.instance) {
      ApiClient.instance = new ApiClient();
    }
    return ApiClient.instance;
  }
  
  async get(url: string) {
    // ...
  }
}

export const apiClient = ApiClient.getInstance();
```

---

## ⚙️ 开发命令（Development Commands）

### 常用命令

| 命令 | 说明 | 使用场景 |
|------|------|----------|
| `npm run dev` | 启动开发服务器 | 日常开发 |
| `npm run build` | 构建生产版本 | 部署前 |
| `pytest --tb=short -q` | 运行所有测试 | 提交前、CI/CD |
| `pytest --tb=short -q -- --coverage` | 生成测试覆盖率报告 | 检查测试覆盖率 |
| `flake8` | 运行 ESLint 检查 | 提交前 |
| `flake8 -- --fix` | 自动修复 lint 问题 | 批量修复格式问题 |


### 提交前检查清单

在提交代码前，**必须**确保以下命令都通过：

```bash
# 1. Lint 检查
flake8

# 2. 测试
pytest --tb=short -q

# 3. 构建
npm run build
```

**推荐**：使用 Husky 配置 pre-commit hook 自动执行检查。



---

## 🔧 环境配置（Environment Configuration）

### 环境变量

本项目使用 `.env` 文件管理环境变量：

```
.env                # 默认配置（提交到 Git）
.env.local          # 本地覆盖（不提交）
.env.development    # 开发环境
.env.production     # 生产环境
```

**变量命名规范**：
- 使用 `` 前缀（客户端可访问）
- UPPER_SNAKE_CASE 命名

**示例**：
```bash
REACT_APP_API_URL=https://api.example.com
REACT_APP_ENV=development
```

### 依赖管理

**包管理器**：npm

**依赖安装**：
```bash
# 安装所有依赖
npm install

# 添加新依赖
npm install <package-name>

# 添加开发依赖
npm install --save-dev <package-name>
```

**依赖更新原则**：
- ❌ **禁止随意升级主版本**（可能引入 breaking changes）
- ✅ 小版本和补丁版本更新需通过测试
- ✅ 重大更新需在团队内讨论

---

## 🤖 AI 工作流集成

### 使用 AI Flow 完成开发任务

本项目已集成 AI Flow 工作流，支持从需求到代码的自动化生成。

#### 触发方式

```bash
# 在 kwaicli/Codeflicker 中输入：
"帮我实现 https://team.kuaishou.com/task/T123456"
```

#### AI 自动执行步骤

1. **需求分析**（requirement-quality-gate）
   - 解析 Team 任务
   - 提取关键需求和验收标准

2. **技术方案**（tech-solution）
   - 基于项目架构生成技术方案
   - 包含状态机、埋点、灰度、回滚等

3. **任务拆解**（plan-from-tech-solution）
   - 生成符合 TDD 的任务清单

4. **方案验证**（verify-from-tech-solution）
   - 路径一致性校验
   - P0 缺口门禁

5. **TDD 实现**（iterate-from-plan-and-tests）
   - 测试驱动开发
   - 自动生成符合项目规范的代码

6. **提交报告**（commit-report）
   - 生成代码改动明细

### AI 指令示例

```
# 快速开发
"实现用户登录功能"
"修复 Button 组件点击无响应的问题"
"优化首页加载性能"

# 需求驱动
"完成需求 https://team.kuaishou.com/task/T123456"

# 资产管理
"研发资产盘点"
"提取代码片段"
```

---

## 📚 参考文档

### 内部文档
- [开发规范详细说明](.codeflicker/rules.md)
- [架构设计文档](docs/agent/architecture.md)
- [开发命令参考](docs/agent/development_commands.md)
- [代码约定](docs/agent/conventions.md)

### 外部资源


---

## 🔄 文档更新

- **版本**：1.0.0
- **最后更新**：2026-03-20T07:19:49.112Z
- **更新方式**：
  - 项目结构变更时，运行 `"初始化 codeflicker"` 重新生成
  - 手动修改后，提交到版本控制
  - 团队成员应定期同步最新版本

---

*本文档由 bootstrap-ai-flow enhanced 自动生成，符合 Codeflicker 官方规范*
*作用：提供自定义指令 → 指导 AI 行为 → 确保代码生成一致性*
