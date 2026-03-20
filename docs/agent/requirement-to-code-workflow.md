### SOP-2：每个需求的强制交付链路（推荐写入CI门禁）
1) Read：docs-recursive-read 汇总需求原文与待确认
2) Align：tech-solution 生成 docs/tasks/{taskId}/tech-solution.md 方案（含 tech YAML + 缺口门禁）
3) Align：plan-from-tech-solution 生成任务/单测清单（含 plan YAML + 注意力复述）
4) Gate：verify-from-tech-solution 阻塞校验（P0门禁+路径级覆盖+Evidence Map）
5) Launch：iterate-from-plan-and-tests 先测试自检→再TDD循环到全绿→跑 lint（可选 typecheck/build）
6) Post：commit-report + rd-asset-review（增量）沉淀变更与资产

补充：YAML 协议以 docs/agent/yaml-contracts.md 为准

---
