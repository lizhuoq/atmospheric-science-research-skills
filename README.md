# Atmospheric Science Research Skills

[English](#english) | [中文](#中文)

## English

An evidence-first, reproducible, and testable Agent Skill suite for atmospheric-science research. It helps Codex, Claude Code, and GitHub Copilot discover current literature, read papers with source locators, design observational or modeling studies, audit data and statistics, draft manuscripts from real results, and check whether conclusions exceed the evidence.

The suite contains one lightweight entry point, `$atmospheric-science-research`, and twelve task-oriented specialist Skills. The bundled 3,000-record corpus is an optional development and regression-test fixture—not a fixed knowledge base. For a new topic, the workflow searches current scholarly sources and reads lawfully accessible full text or papers supplied by the user. No copyrighted PDF is distributed.

### Install

Requirements: Python 3.10+ and a compatible Agent Skills runtime. Clone the repository, then install all Skills for your platform:

```bash
git clone https://github.com/lizhuoq/atmospheric-science-research-skills.git
cd atmospheric-science-research-skills

# Codex: project scope (.agents/skills)
python scripts/install_skill.py --platform codex --scope project --all

# Claude Code: project scope (.claude/skills)
python scripts/install_skill.py --platform claude --scope project --all

# GitHub Copilot: project scope (.github/skills)
python scripts/install_skill.py --platform copilot --scope project --all
```

Use `--scope user --all` for a user-level installation. Add `--force` when updating an existing installation. Restart the agent session after first installation.

### Use

Invoke the main entry point for an end-to-end task:

```text
Use $atmospheric-science-research to develop an evidence-grounded SCI study
on urban effects on extreme precipitation. Search current literature, read
the relevant full text, design the analysis, and do not invent results.
```

Invoke a specialist directly for a narrow task:

```text
Use $atmospheric-literature-search to build a reproducible literature set.
Use $atmospheric-paper-reader to extract claims with page and figure locators.
Use $atmospheric-statistical-analysis to audit CRPS, reliability, leakage,
dependence, and uncertainty in an ensemble forecast evaluation.
Use $atmospheric-claim-audit to check every conclusion against its evidence.
```

### Skill reference and minimal examples

Use the main entry point when the request spans several research stages. Call a specialist directly when the desired output is narrow and already clear. The `$name` form works in Codex and other runtimes that support explicit Skill names; Claude Code may expose the same names as `/name`. In GitHub Copilot, paste the example as a natural-language Chat or agent-mode request.

| Skill | When to use it | Minimal example |
|---|---|---|
| `$atmospheric-science-research` | End-to-end work that crosses literature, design, analysis, writing, or review. It routes to only the specialists needed. | `Use $atmospheric-science-research to plan an evidence-grounded study of urban effects on extreme rainfall.` |
| `$atmospheric-literature-search` | Build or update a reproducible literature set; search multiple scholarly sources, deduplicate, screen, verify versions, and record access status. | `Use $atmospheric-literature-search to find 2020–present studies of aerosol–cloud interactions over East Asia and return a screened evidence table.` |
| `$atmospheric-paper-reader` | Read supplied or lawfully acquired full text and extract atomic claims with page, section, table, equation, or figure locators. | `Use $atmospheric-paper-reader to extract the datasets, methods, findings, and limitations from these papers with exact source locators.` |
| `$atmospheric-research-design` | Turn a question and verified evidence into hypotheses, variables, observations/simulations, validation, sensitivity tests, and a reproducible plan. | `Use $atmospheric-research-design to design an observational study of heatwave–ozone coupling, including confounders and validation.` |
| `$atmospheric-statistical-analysis` | Design or audit statistics, causal inference, time-series/spatial methods, extremes, ML validation, or forecast verification. | `Use $atmospheric-statistical-analysis to audit this ensemble evaluation for CRPS, reliability, dependence, leakage, and uncertainty.` |
| `$atmospheric-data-qc` | Check units, coordinates, calendars, timestamps, flags, missingness, aggregation, regridding, representativeness, and provenance before analysis. | `Use $atmospheric-data-qc to audit the harmonization of ERA5, station, and satellite precipitation data.` |
| `$atmospheric-figure-analysis` | Interpret or audit maps, profiles, time series, tables, equations, captions, graphical integrity, and whether figures support the claims. | `Use $atmospheric-figure-analysis to assess what Figure 3 supports, its uncertainty, and any panel or caption inconsistencies.` |
| `$atmospheric-model-experiment` | Design or audit NWP, WRF, CTM, climate, LES, or Earth-system experiments, including forcing, boundaries, spin-up, parameterizations, ensembles, and validation. | `Use $atmospheric-model-experiment to design WRF sensitivity experiments for urban convection without changing multiple factors at once.` |
| `$atmospheric-extremes-attribution` | Analyze extreme-event definitions, return periods, trends, mechanisms, factual/counterfactual ensembles, risk ratios, and attribution strength. | `Use $atmospheric-extremes-attribution to audit whether this heatwave study supports a causal attribution claim.` |
| `$atmospheric-composition-air-quality` | Work on atmospheric chemistry, aerosols, emissions, CTMs, PM/ozone, source apportionment, meteorological normalization, exposure, or health interpretation. | `Use $atmospheric-composition-air-quality to design a PM2.5 source-attribution study and identify exposure-error risks.` |
| `$atmospheric-manuscript-writer` | Draft or revise manuscript sections from verified literature and user-owned methods/results; it must not invent results or citations. | `Use $atmospheric-manuscript-writer to draft the Methods from this protocol and Results from these supplied outputs only.` |
| `$atmospheric-claim-audit` | Check abstracts, conclusions, reviews, and policy-facing statements against citations, scope, design, uncertainty, and causal strength. | `Use $atmospheric-claim-audit to label every conclusion as supported, overstated, contradicted, or unverifiable.` |
| `$atmospheric-peer-review` | Produce a pre-submission audit, referee report, revision check, or response-to-reviewer assessment focused on validity and evidence. | `Use $atmospheric-peer-review to review this manuscript and separate major validity issues from optional improvements.` |

The examples are starting points, not rigid commands. Add the study region, period, atmospheric scale, allowed sources, desired output, and any supplied data or papers. If a task needs current literature, the agent should search accessible scholarly services first and must not treat the bundled metadata as the final evidence base.

Claude Code may also expose Skills as slash commands, for example `/atmospheric-science-research`. In Copilot, use the same natural-language requests in Chat or agent mode. Availability of Web of Science, Scopus, publisher full text, or other subscribed sources depends on the user's accounts and runtime; the Skills never bypass access controls.

Validate a checkout with:

```bash
python scripts/validate_skill_suite.py
python -m unittest discover -s tests -v
python scripts/check_publication_safety.py
```

See the Chinese section below for detailed Windows/macOS/Linux installation, update, uninstall, troubleshooting, copyright, and reproducibility instructions.

## 中文

面向大气科学研究的证据优先、可复现、可测试 Agent Skill 工程。项目使用 30 本代表性期刊、2016–2025 年 3,000 条论文元数据和 1,081 份本地已校验全文进行开发与评测；这些论文是示例语料和测试基准，不是 Skill 的固定知识库或使用范围。论文 PDF 不属于开源发布内容。

当前提供 13 个可安装 Skill。`atmospheric-science-research` 是轻量总入口，只负责理解研究目标、选择必要的任务型 Skill、维护证据链并整合交付，不重复专业 Skill 的详细流程。内置 3,000 条索引只用于离线演示、术语扩展与回归测试。

## Skill 命令与最小用法

跨越多个科研阶段时使用总入口；目标明确且单一时直接调用专业 Skill。Codex 等平台可使用 `$名称` 显式调用；Claude Code 也可能显示为 `/名称`；GitHub Copilot 中直接把示例作为 Chat 或 agent mode 的自然语言请求即可。

| Skill | 何时使用 | 最小调用示例 |
|---|---|---|
| `$atmospheric-science-research` | 轻量总入口；任务横跨文献、研究设计、分析、写作或审查时，自动选择必要的专业 Skill。 | `使用 $atmospheric-science-research，规划一项城市化影响极端降水的证据驱动研究。` |
| `$atmospheric-literature-search` | 从多个学术来源实时检索、去重、筛选、核验版本并记录全文获取状态。 | `使用 $atmospheric-literature-search，检索 2020 年以来东亚气溶胶—云相互作用研究，并输出可复现的筛选表。` |
| `$atmospheric-paper-reader` | 深读用户提供或合法取得的全文，从正文、方法、公式、表格和图中抽取带定位的原子证据。 | `使用 $atmospheric-paper-reader，从这些论文提取数据、方法、发现和局限，并标明页码及图表号。` |
| `$atmospheric-research-design` | 将问题与已核验证据转成假设、变量、观测/模拟方案、验证、敏感性分析和复现计划。 | `使用 $atmospheric-research-design，设计热浪—臭氧耦合观测研究，并处理混杂因素和验证。` |
| `$atmospheric-statistical-analysis` | 设计或审查统计、因果、时空、极值、机器学习验证和预报检验。 | `使用 $atmospheric-statistical-analysis，检查集合预报评估中的 CRPS、可靠性、数据泄漏、依赖性和不确定性。` |
| `$atmospheric-data-qc` | 分析前检查单位、坐标、日历、时间戳、质量标志、缺测、聚合、重网格、代表性和谱系。 | `使用 $atmospheric-data-qc，审查 ERA5、站点和卫星降水数据的统一处理方案。` |
| `$atmospheric-figure-analysis` | 解读或审查地图、剖面、时间序列、表格、公式、图注和图文证据一致性。 | `使用 $atmospheric-figure-analysis，判断图 3 实际支持哪些结论、存在何种不确定性和面板不一致。` |
| `$atmospheric-model-experiment` | 设计或审查 NWP、WRF、CTM、气候、LES 或地球系统模式的强迫、边界、spin-up、参数化、集合和验证。 | `使用 $atmospheric-model-experiment，设计城市对流的 WRF 敏感性试验，避免一次改变多个因素。` |
| `$atmospheric-extremes-attribution` | 处理极端定义、重现期、趋势、机制、事实/反事实集合、风险比和归因强度。 | `使用 $atmospheric-extremes-attribution，审查该热浪研究是否足以支持因果归因。` |
| `$atmospheric-composition-air-quality` | 处理大气化学、气溶胶、排放、CTM、PM/臭氧、源解析、气象归一化、暴露和健康解释。 | `使用 $atmospheric-composition-air-quality，设计 PM2.5 源解析研究并识别暴露误差风险。` |
| `$atmospheric-manuscript-writer` | 仅依据已核验证据和用户真实方法/结果撰写或修改论文，不得虚构结果和引文。 | `使用 $atmospheric-manuscript-writer，只根据这份方案和已提供输出撰写 Methods 与 Results。` |
| `$atmospheric-claim-audit` | 逐条检查摘要、结论、综述或政策陈述的引文支持、范围、设计、不确定性和因果强度。 | `使用 $atmospheric-claim-audit，把每条结论标记为有支持、过度表述、相互矛盾或无法核验。` |
| `$atmospheric-peer-review` | 进行投稿前审查、同行评审、修订核查或回复审稿人检查，优先关注有效性和证据。 | `使用 $atmospheric-peer-review，审查这篇稿件，并区分重大有效性问题与可选改进。` |

这些示例是起点而不是固定语法。可继续补充研究区域、时段、大气尺度、允许使用的来源、期望输出，以及已有数据或论文。需要当前文献时，代理应先检索实际可访问的学术来源，不能把仓库附带元数据当作最终证据库。

## 核心工作流

```text
研究问题 → 检索式与来源路由 → 去重与筛选 → 合法全文获取
        → 正文/图表阅读 → 原子证据记录 → 综合与冲突分析
        → 研究设计/SCI 草稿 → 引文、尺度、因果与不确定性审查
```

Skill 会根据任务组合 Web of Science、Scopus、OpenAlex、Google Scholar、Semantic Scholar、NASA ADS、Crossref/DataCite、Unpaywall、DOAJ、PubMed/PubMed Central、EarthArXiv/ESSOAr、出版社与机构仓储等来源。具体可用性取决于宿主代理、API、订阅和用户的机构权限；Skill 不附带数据库订阅或凭据，也不会绕过付费墙或访问控制。详见 `skills/atmospheric-science-research/references/literature-discovery.md`。

## 快速开始

需要 Python 3.10+，核心构建和测试不依赖第三方包。

```powershell
python scripts/build_milestone1.py --check
python -m unittest discover -s tests -v
python skills/atmospheric-science-research/scripts/query_corpus.py aerosol cloud --split train --limit 10
python skills/atmospheric-science-research/scripts/validate_evidence.py skills/atmospheric-science-research/tests/fixtures/valid-evidence.jsonl
```

安装后的 Skill 不依赖本仓库的 PDF 或 `data/` 目录。离线时仍可用内置版权安全索引演示查询和执行方法检查；但为新的 SCI 主题建立当前、完整且可核验的证据基础，需要宿主代理具备联网检索能力，或由用户提供相关论文。论文下载到用户自己的 Git 忽略工作目录，不能进入 Skill 发布包。

## 安装指南

首先克隆仓库并进入项目目录：

```powershell
git clone https://github.com/lizhuoq/atmospheric-science-research-skills.git
cd atmospheric-science-research-skills
python scripts/build_milestone1.py --check
python -m unittest discover -s tests -v
```

也可以使用跨平台安装器；将 `--skill` 替换为 13 个 Skill 中的任意一个：

```powershell
python scripts/install_skill.py --platform codex --scope project --skill atmospheric-science-research
python scripts/install_skill.py --platform claude --scope project --skill atmospheric-statistical-analysis
python scripts/install_skill.py --platform copilot --scope project --skill atmospheric-data-qc
```

推荐一次安装完整套件，以便总入口自动路由：

```powershell
python scripts/install_skill.py --platform codex --scope project --all
python scripts/install_skill.py --platform claude --scope project --all
python scripts/install_skill.py --platform copilot --scope project --all
```

更新已有安装时追加 `--force`。也可以用 `--scope user --all` 安装到个人级目录。

从旧版升级时，应删除已废弃的 `atmospheric-evidence-synthesis`、`atmospheric-forecast-evaluation` 和 `atmospheric-remote-sensing-validation` 安装目录，再安装完整套件。它们仍有价值的规则已经迁移到新的任务型 Skill 中。

安装第三方 Skill 前应先检查 `SKILL.md`、引用文件和可执行脚本。

### Codex

Codex 原生支持项目级和个人级 Skills。项目级目录为 `.agents/skills/`，个人级目录为 `~/.agents/skills/`。项目安装适合需要使用本仓库元数据和拆分文件的完整功能。

项目级安装，Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force .agents\skills | Out-Null
Copy-Item -Recurse -Force skills\atmospheric-science-research .agents\skills\
```

项目级安装，macOS/Linux：

```bash
mkdir -p .agents/skills
cp -R skills/atmospheric-science-research .agents/skills/
```

个人级安装：

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
Copy-Item -Recurse -Force skills\atmospheric-science-research "$HOME\.agents\skills\"
```

```bash
# macOS/Linux
mkdir -p ~/.agents/skills
cp -R skills/atmospheric-science-research ~/.agents/skills/
```

重新打开 Codex 任务后，可显式调用：

```text
使用 $atmospheric-science-research，完成关于气溶胶影响区域降水的检索、证据综合、研究设计和论文写作审查。
```

也可以直接描述匹配任务，由 Codex 根据 Skill 的 `description` 自动选择。Codex 官方说明见 [Customization — Skills](https://learn.chatgpt.com/docs/customization/overview#skills)。

### Claude Code

Claude Code 的项目级目录为 `.claude/skills/`，个人级目录为 `~/.claude/skills/`。

项目级安装，Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force .claude\skills | Out-Null
Copy-Item -Recurse -Force skills\atmospheric-science-research .claude\skills\
```

项目级安装，macOS/Linux：

```bash
mkdir -p .claude/skills
cp -R skills/atmospheric-science-research .claude/skills/
```

个人级安装使用同样的复制方式，将目标目录改为 `$HOME\.claude\skills\`（Windows）或 `~/.claude/skills/`（macOS/Linux）。如果在 Claude Code 已运行后首次创建顶层 skills 目录，建议重启该会话以确保发现新目录。

使用时可以让 Claude 自动匹配，也可以显式调用：

```text
/atmospheric-science-research 研究极端降水变化，从实时文献检索开始并最终检查结论是否越界。
```

用 `/skills` 检查是否已发现该 Skill。官方说明见 [Extend Claude with skills](https://code.claude.com/docs/en/skills)。

### GitHub Copilot

GitHub Copilot Agent Skills 支持 Copilot cloud agent、code review、Copilot CLI、Copilot app，以及 VS Code agent mode。推荐的项目级目录是 `.github/skills/`；Copilot 也支持项目中的 `.agents/skills/` 和 `.claude/skills/`。个人级目录为 `~/.copilot/skills/` 或 `~/.agents/skills/`。

项目级安装，Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force .github\skills | Out-Null
Copy-Item -Recurse -Force skills\atmospheric-science-research .github\skills\
```

项目级安装，macOS/Linux：

```bash
mkdir -p .github/skills
cp -R skills/atmospheric-science-research .github/skills/
```

个人级安装时，将目标改为 `$HOME\.copilot\skills\`（Windows）或 `~/.copilot/skills/`（macOS/Linux）。如果仓库发布后可通过 GitHub CLI 安装，也可以使用以下流程；`gh skill` 目前属于 public preview，命令和行为可能变化：

```bash
gh skill preview lizhuoq/atmospheric-science-research-skills atmospheric-science-research
gh skill install lizhuoq/atmospheric-science-research-skills atmospheric-science-research
```

在 Copilot Chat 或 agent mode 中使用自然语言触发：

```text
Use the atmospheric-science-research skill to research a PM2.5 exposure question from current literature through manuscript claim audit.
```

Copilot 会依据 Skill 描述决定是否加载它。如果需要稳定的仓库级常驻规则，应另外使用 `.github/copilot-instructions.md`；不要把完整研究工作流重复复制到该文件。官方说明见 [Adding agent skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)。

### 安装验证

三种平台都可以先要求代理回答：

```text
列出 atmospheric-science-research 可路由的任务型 Skill、实时文献检索边界，以及不得用元数据代替全文证据的要求。不要执行研究任务。
```

正确结果应能识别实时检索、全文阅读、证据定位、专业分析、写作和主张审查的边界。随后运行本地脚本验证：

```powershell
python skills/atmospheric-science-research/scripts/query_corpus.py aerosol --split train --limit 3
python skills/atmospheric-science-research/scripts/validate_evidence.py skills/atmospheric-science-research/tests/fixtures/valid-evidence.jsonl
python scripts/validate_skill_suite.py
```

### 更新与卸载

更新仓库后重新复制 Skill 目录即可覆盖旧版本。卸载时删除相应平台下的 `atmospheric-science-research/` 目录；不要删除原始仓库的 `data/metadata/`、`data/splits/` 或本地 `data/papers/`。若 Skill 仍出现在已有会话中，启动一个新会话再检查。

### 常见问题

- **Skill 未被自动触发**：显式写出 Skill 名称，并确认 `SKILL.md` 位于正确的二级目录中。
- **查询脚本找不到 `references/corpus-index.csv`**：安装包不完整。重新复制整个 Skill 目录，而不是只复制 `SKILL.md`。
- **只有元数据，没有全文结论**：这是预期行为。元数据只能用于候选检索，科学事实必须从合法取得的全文中定位。
- **无法访问 Web of Science/Scopus 等订阅库**：改用可访问的 OpenAlex、Crossref、Semantic Scholar、NASA ADS、开放仓储和出版社页面，并在检索记录中披露覆盖限制；不要声称已经检索不可用的数据库。
- **代理尝试使用盲测论文编写规则**：停止该轮任务并重新明确只允许 `train` 记录成为规则来源。
- **Windows 路径问题**：从仓库根目录运行命令，并确认 Python 3.10+ 可通过 `python --version` 找到。

## 目录

- `skills/`：可移植 Skill、参考文件、脚本和测试夹具。
- `schemas/`：结构化证据契约。
- `data/metadata/`：可审计书目台账。
- `data/derived/`：可重建主题分类。
- `data/splits/`：固定拆分、种子和输入哈希。
- `reports/`：语料审计与主题覆盖报告。
- `docs/`：架构、方法、评测、版权与设计决策。
- `data/papers/`：本地全文，必须保持 Git 忽略。

## 复现与审计

`scripts/build_milestone1.py` 仅读取冻结元数据，不访问网络。它用透明的多标签词表分类，并按主题、年份和期刊进行确定性贪心分层，生成 70/15/15 的训练、开发和盲测集。运行 `--check` 可检测派生产物是否过期。

PDF 完整性与解析抽样使用：

```powershell
python scripts/audit_corpus.py --sample-per-journal 3
```

该命令需要 `pypdf` 才能做解析抽样；不使用它也可运行核心测试。不要重新运行 `collect_openalex.py` 或下载脚本来修改已冻结语料，除非新的、经记录的采集阶段明确要求这样做。

## 科学与数据边界

- 单篇论文结论不是普遍规律；证据记录必须保留 DOI、题名、年份、来源定位、适用条件、限制、强度和冲突状态。
- 只有训练集可用于编写规则；开发集仅调优工作流；盲测集仅用于冻结后的最终评估。
- Skill 要求区分观测、模式和理论推断，区分相关、预测和因果，并检查单位、尺度、时间基准、变量定义、统计假设、模式配置及验证资料。
- 不得伪造 DOI、引文、数据集、数值或来源定位。

## 版权与许可证

Apache-2.0 仅覆盖贡献者创作的代码、文档、schema 和其他原创成果，不覆盖论文、出版社版式、第三方摘要/元数据、图表或订阅内容。`data/papers/`、全文解析缓存和可重构正文的中间文件不得提交。发布前运行：

```powershell
python scripts/check_publication_safety.py
```

详细政策见 `docs/copyright-and-data-policy.md`。引用本项目不替代引用原始论文。

## 文档入口

- [语料审计](reports/corpus-audit.md)
- [主题分类](reports/topic-classification.md)
- [Skill 架构](docs/architecture.md)
- [语料与拆分方法](docs/corpus-methodology.md)
- [评测计划](docs/evaluation.md)
- [下一阶段优先级](docs/next-phase-priorities.md)
- [参考开源模式](docs/open-source-patterns.md)
- [贡献指南](CONTRIBUTING.md)
