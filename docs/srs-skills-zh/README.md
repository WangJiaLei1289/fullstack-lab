# srs-skills

[Tiếng Việt](./README.md) · [English](./README.en.md)

AI 技能包：从想法出发，生成完整的**软件需求规格说明书**（Software Requirements Specification，IEEE 830-1998）文档。

## 技能索引

| 技能 | 作用 |
|---|---|
| [srs-workflow](./skills/srs-workflow/) | 编排从想法到交接的整条流水线 |
| [srs-generator](./skills/srs-generator/) | 从已有需求快速生成 SRS |
| [sr-brainstorm](./skills/sr-brainstorm/) | 通过 5 轮提问获取需求 |
| [sr-spec](./skills/sr-spec/) | 把头脑风暴汇总成规格 |
| [sr-plan](./skills/sr-plan/) | 为每个 SRS 章节制定蓝图 |
| [sr-generate](./skills/sr-generate/) | 生成 IEEE 830 文档 |
| [sr-validate](./skills/sr-validate/) | 校验并自动修复结构错误 |
| [sr-improve](./skills/sr-improve/) | 建立改进待办列表 |
| [sr-save](./skills/sr-save/) | 保存上下文，供后续会话继续 |

---

## 安装

把技能复制到你的项目里：

```bash
cp -r srs-skills/skills/sr-* <your-project>/skills/
cp -r srs-skills/skills/srs-workflow/references <your-project>/skills/srs-workflow/
cp -r srs-skills/skills/srs-generator/references <your-project>/skills/srs-generator/
```

或者直接在 Claude Code 中打开 `srs-skills/` 目录，即可立即使用。

---

## 选择合适的工作流

| 场景 | 命令 |
|-----------|---------|
| 有想法 / 主题，但还没有需求 | 使用下面的 `/sr:*` 流水线 |
| 已经有现成的需求文本 | `/cl:srs` —— 直接分析并生成 SRS |

---

## 完整流水线：`/sr:*`

按顺序逐步执行。每一步都会读取上一步的输出。

### `/sr:brainstorm`

输入你的主题。AI 会分 5 轮提问，每个问题都有选项可选：

- 第 1 轮 —— 参与者与用户
- 第 2 轮 —— 核心功能
- 第 3 轮 —— 范围（IN / OUT）
- 第 4 轮 —— 技术约束 + NFR 目标
- 第 5 轮 —— 业务规则与边界情况

AI **绝不猜测**——只要不清楚就必须追问。只有当没有遗留待办项时才结束。

> 输出：`projects/{slug}/brainstorm.md`

---

### `/sr:spec`

读取 `brainstorm.md`，写出完整规格：参与者、功能、业务规则、NFR 基线、假设、待办项。不限字数。

> 输出：`projects/{slug}/spec.md`

---

### `/sr:plan`

读取 `spec.md`，创建 **12 个独立的计划文件**——每个文件都是 SRS 对应章节（§1–§3、附录 A/B）的详细蓝图，包含 FR 桩和 NFR 目标。

完成后会运行 `plan_validator.py` 统计 FR/NFR（避免人工计数出错），然后 AI 请你审阅并批准，之后才生成 SRS。

> 输出：`projects/{slug}/plan/`（12 个文件）

---

### `/sr:generate`

动笔之前先跑门禁 `plan_validator.py --dir projects/{slug}/plan/`：
- **BLOCKED**（缺文件、FR 编号有缺口、缺少 shall……）→ 停下，要求回到 `/sr:plan` 修改
- **READY WITH WARNINGS**（还有未跟进的 `[NEEDS USER INPUT]`）→ 询问是否确认继续
- **READY** → 生成

目的：在花 token 重写 300 多页 SRS 之前，先把计划里的结构错误（成本更低）抓出来。

读取已批准的计划文件，生成完整的 SRS——**不限字数**，可达 300 多页。每个章节是一个独立文件。

每条 FR 必须包含：
- `The system shall ...` 子句
- Given / When / Then 验收标准

每条 NFR 必须有数值化的响应度量（不要用「fast」「good」这类形容词）。

> 输出：`projects/{slug}/srs/`（11 个文件 + 总索引）

---

### `/sr:validate`

对整个 `srs/` 目录运行 `srs_validator.py`。按 IEEE 830 检查：
- 必需章节齐全
- FR 编号没有缺口
- 每条 FR 都有 shall + GWT
- 每条 NFR 都有数值目标
- 没有未解决的 `[TBD]` / `[CONTEXT-GAP]` 标记

ERRORs 会在当前会话中立即修复。WARNs 会传递到下一步。

判定：**COMPLIANT** / **PARTIALLY COMPLIANT** / **NON-COMPLIANT**

---

### `/sr:improve`

生成改进报告：被推迟的功能、技术风险、NFR 缺口、需要拆得更细的 FR，以及来自校验步骤的警告。

> 输出：`projects/{slug}/improvement-report.md`

---

### `/sr:save`

把项目的全部上下文保存进 6 个小文件，好让后续的 Claude 会话无需重读整份 SRS 就能重新加载。

> 输出：`projects/{slug}/_context/`（愿景、功能、技术栈、术语表、质量标准、会话记录）

---

## 快速 SRS：`/cl:srs`

适用于已经有现成需求文本的情况。把文本粘贴进去，AI 会：

1. 扫描 7 类歧义（含糊的量词、未定义的参与者、相互矛盾……）
2. 按优先级提出澄清问题（先问 P1 阻塞项）
3. 生成符合 IEEE 830 的单文件 SRS

---

## CLI 脚本（可选）

```bash
# Scan requirements text trước khi đưa vào AI
python scripts/gap_scanner.py requirements.txt

# Validate plan/ trước khi generate (Phase 4 gate)
python scripts/plan_validator.py --dir projects/{slug}/plan/
python scripts/plan_validator.py --dir projects/{slug}/plan/ --stats   # đếm FR/NFR/open items

# Validate SRS thủ công
python scripts/srs_validator.py --dir projects/{slug}/srs/
python scripts/srs_validator.py --dir projects/{slug}/srs/ --strict   # WARN = ERROR
python scripts/srs_validator.py --dir projects/{slug}/srs/ --format json
python scripts/srs_validator.py --dir projects/{slug}/srs/ --stats    # đếm FR/NFR/open items

# Khởi tạo context scaffold cho project mới
python scripts/init_project.py {slug}
```

---

## 命令汇总

```
/sr:brainstorm  →  /sr:spec  →  /sr:plan  →  /sr:generate  →  /sr:validate  →  /sr:improve  →  /sr:save

hoặc: /cl:srs   (nếu đã có requirements text)
```
