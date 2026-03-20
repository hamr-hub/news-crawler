```md
# YAML Contracts（tech-solution & plan-from-tech-solution）

本文件定义“可机读协议”，用于：
- tech-solution 产出技术方案时的 YAML 区块
- plan-from-tech-solution 拆分任务与测试时的 YAML 区块
- verify-from-tech-solution 做阻塞式门禁与路径级覆盖校验

## 1. tech-solution YAML

### 1.1 位置要求
- 必须位于 docs/tasks/{taskId}/tech-solution.md 的末尾
- 必须包裹在 ```yaml 代码块中

### 1.2 字段定义
```yaml
meta:
  title: string
  date: "YYYY-MM-DD"
  owners: string[]
  links:
    prd: string
    figma: string
flags:
  - name: string
    type: "query"|"launch_options"|"kconf"|"ab"
    priority: number
    default: string|number|boolean
    description: string
api:
  - name: string
    layer: "services"|"query"
    endpoint: string
    method: "GET"|"POST"
    request: string[]
    response: string[]
    errors: string[]
file_changes:
  - path: string
    change: "add"|"modify"|"remove"
    summary: string
    risk: "low"|"medium"|"high"
    test_points: string[]
tracking:
  - event: string
    type: "show"|"click"|"pv"|"custom"
    when: string
    params: string[]
validation:
  acceptance: string[]
  rollback: string[]
  monitoring: string[]
open_questions: string[]
```

### 1.3 P0 门禁（verify 会阻塞）
- flags/api/file_changes/tracking 必须非空
- validation.acceptance/rollback 必须非空

## 2. plan-from-tech-solution YAML

### 2.1 字段定义
```yaml
plan:
  meta:
    source_tech_doc: string
    scope: "P0"|"P1"
  tasks:
    - id: string
      priority: "P0"|"P1"|"P2"
      title: string
      files: string[]
      depends_on: string[]
      definition_of_done: string[]
  tests:
    - id: string
      priority: "P0"|"P1"|"P2"
      target: string
      type: "pure"|"hook"|"component"
      file: string
      given: string
      when: string
      then: string[]
  commands:
    test: string
    lint: string
    typecheck: string
    build: string
  acceptance: string[]
  rollback: string[]
  monitoring: string[]
  open_questions: string[]
```

### 2.2 P0 门禁（verify 会阻塞）
- tasks/tests 非空
- commands.test 与 commands.lint 非空

## 3. 路径级覆盖规则（verify）
- tech.file_changes[*].path 必须被 plan.tasks[*].files 覆盖
  - 允许：tech change=add 且 path 不存在（视为新建）
  - 不允许：tech change=modify/remove 且 path 不在 plan.tasks.files

## 4. 建议写法
- tech.file_changes.path 统一写相对路径（如 src/...），避免绝对路径
- plan.tasks.files 尽量列到文件粒度，不要只写目录
```

---
