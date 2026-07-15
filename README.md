<p align="center">
  <img src="assets/socialmedia-gpthalf-logo.png" width="220" alt="SocialMedia GPTHalf logo">
</p>

<h1 align="center">SocialMedia GPTHalf</h1>

<p align="center">
  Evidence-aware AI-origin checks and human-reception analysis for public social media.<br>
  面向公开社交媒体的 AI 来源核验与人类阅读感受分析。
</p>

<p align="center">
  <a href="#english">English</a> · <a href="#中文">中文</a>
</p>

## English

SocialMedia GPTHalf is a Codex Skill for inspecting public posts, webpages, pasted text, and images without presenting uncertain AI detection as fact. It separates verified origin evidence, explainable Simplified-Chinese drafting patterns, and estimated reader reactions so that each conclusion stays within its evidence.

### Why this project exists

Reliable authorship labels are rare on social media. Short posts, edited drafts, translation, genre conventions, and formulaic human writing can all resemble model output. The inverse is also true: generated content can read naturally and contain personal detail.

Reader response creates a separate problem. People may dislike a post because it feels generic, manipulative, overly certain, or poorly matched to the platform. None of those reactions proves AI authorship. A provenance detector that mixes style and aversion into one score can therefore sound confident while answering the wrong question.

SocialMedia GPTHalf asks three narrower questions:

- **Verified origin evidence:** checks author disclosures, platform labels, Content Credentials, and Coalition for Content Provenance and Authenticity (C2PA) manifests
- **Writing-pattern evidence:** reports grounded Simplified-Chinese document and sentence signals without converting them into an “AI percentage”
- **Estimated reader response:** describes reactions from supporter, neutral-reader, and skeptic stances, with excerpts and uncertainty

The name “GPTHalf” reflects this position. AI-origin analysis is not a binary truth machine. Useful results explain where evidence is strong, where it is only descriptive, and where the system cannot decide.

### What the Skill analyzes

The three analysis layers remain independent throughout the workflow:

| Layer | Purpose | Main evidence | What it cannot establish |
| --- | --- | --- | --- |
| Origin assessment | Is there verifiable AI provenance or a strong asset signal? | Author disclosure, platform label, local C2PA verification, optional selected-image analysis | Missing metadata does not prove human authorship |
| Writing-pattern analysis | Does Simplified-Chinese text contain concentrated model-like drafting patterns? | Document structure, sentence concentration, repetition, generic transitions, symmetry, and counter-signals | Pattern matches are not authorship probabilities or verified provenance |
| Human Reception | How may different readers respond? | Specific excerpts, visible purpose, platform context, tone, autonomy, and disclosure expectations | Estimated reactions are not measured audience behavior or AI evidence |

The local text analyzer borrows public ideas such as variation, local concentration, and document-level aggregation. It does not reproduce GPTZero’s proprietary model, training data, weights, calibration, or accuracy. The Skill does not send text to GPTZero or another third-party text detector.

### How an analysis runs

Each case follows an evidence-preserving sequence:

1. Capture public text, images, platform context, disclosures, and the canonical source URL
2. Build a validated `case.json` without bypassing login walls, private pages, paywalls, or verification challenges
3. Draft `reception.json` before viewing detector findings, which reduces AI-label bias in the reader analysis
4. Verify image C2PA data locally and run the local Simplified-Chinese pattern checks
5. Upload only explicitly selected images when you authorize optional external image analysis
6. Produce separate origin, writing-pattern, and Human Reception sections in `report.json` and `report.md`

Provider failures produce a partial report instead of erasing successful local checks. Temporary media is removed after analysis.

### What is included

The repository contains the complete project-level Skill:

- `SKILL.md`: invocation rules, analysis order, safety boundaries, and reporting requirements
- `scripts/`: case validation, local text analysis, C2PA verification, optional image-provider integration, redaction, evaluation, and report generation
- `references/`: evidence policy, Human Reception rubric, input and output contracts, platform workflow, model limitations, and research notes
- `scripts/tests/`: boundary, failure, privacy, provenance, style-pattern, and reception tests

Version 1 supports public X, Reddit, LinkedIn, Instagram, TikTok, Threads, and ordinary webpage inputs when the content is accessible. It accepts URLs, pasted text, attached images, or a combination. It does not provide video or audio analysis, account monitoring, bulk scanning, enforcement, or a standalone web interface.

### Install and invoke the Skill

Clone the repository into your project’s Skill directory and install the optional runtime dependencies:

```bash
skill_dir=.agents/skills/socialmedia-gpthalf
git clone \
  https://github.com/yuzhang-zhong/socialmedia-gpthalf.git \
  "$skill_dir"
pip install -r "$skill_dir/scripts/requirements.txt"
```

Invoke the Skill with a public URL, text, or image:

```text
Use $socialmedia-gpthalf to analyze this public social media post for AI-origin evidence and likely human reader reactions.
```

For a structured case, run the analyzer after preparing validated case and blind-reception inputs:

```bash
python scripts/social_ai_check.py analyze \
  --input case.json \
  --reception reception.json \
  --output-dir output \
  --format both
```

See the [input and output contract](references/input-output-contract.md) for schemas and the [platform workflow](references/platform-workflow.md) for URL handling.

### Interpret results within their limits

Origin verdicts include `verified_ai_provenance`, `strong_ai_indicators`, `conflicting_evidence`, `no_reliable_ai_evidence`, and `insufficient_evidence`. The report preserves asset scope: provenance attached to one image does not automatically apply to the caption or the entire post.

Local Chinese labels such as `strong_pattern_match` and `localized_pattern_match` describe pattern convergence only. They never mean “probably AI-written.” Human Reception findings cite short excerpts and describe plausible friction or positive signals for each reader stance.

Apply these guardrails:

- Do not translate missing AI evidence into “human-authored” or “authentic”
- Do not use reader aversion as evidence of AI authorship
- Do not upload private, medical, financial, minor-related, or otherwise sensitive content by default
- Do not use reports for punishment, hiring, legal findings, education sanctions, or automatic platform bans
- Seek real audience testing when a decision depends on how people will respond

## 中文

SocialMedia GPTHalf 是一个 Codex Skill，用于检查公开帖子、网页、粘贴文本和图片。它不会把不确定的 AI 检测包装成事实，而是严格分开来源证据、可解释的简体中文写作模式，以及推测的人类阅读反应，让每项结论都停留在证据允许的范围内。

### 项目动机

社交媒体上很少存在可靠的作者身份标签。短文本、人工编辑、翻译、文体惯例和模板化的人类写作，都可能呈现模型式特征。反过来，生成内容也可以自然流畅，并包含具体细节。

读者感受又是另一个问题。帖子可能因为空泛、操控感、过度确定或不符合平台语境而令人反感，但这些反应都不能证明内容来自 AI。如果把风格相似和读者反感混入一个分数，检测器可能看起来很确定，实际上却回答了错误的问题。

SocialMedia GPTHalf 因此只回答三个边界清楚的问题：

- **可验证的来源证据：** 检查作者披露、平台标签、Content Credentials，以及内容来源与真实性联盟（C2PA）清单
- **写作模式证据：** 报告有原文依据的简体中文文档级和句子级信号，但不把它们转换成“AI 率”
- **推测的读者反应：** 从支持者、中立读者和怀疑者视角描述可能感受，同时提供短片段和不确定性说明

“GPTHalf”这个名字表达了项目立场：AI 来源分析不是非黑即白的真相机器。有效的报告应该说明证据强在哪里、哪些判断只是描述性的，以及系统从哪里开始无法判断。

### Skill 分析什么

整个流程始终保持三个分析层相互独立：

| 分析层 | 分析目的 | 主要依据 | 不能得出的结论 |
| --- | --- | --- | --- |
| 来源核验 | 是否存在可验证的 AI 来源或较强的资产信号？ | 作者披露、平台标签、本地 C2PA 核验、可选的指定图片分析 | 缺少元数据不能证明由人类创作 |
| 写作模式分析 | 简体中文文本是否集中出现模型式起草模式？ | 文档结构、句子信号集中度、重复、通用转折、对称表达和反向信号 | 模式命中不是作者身份概率，也不是来源证明 |
| Human Reception | 不同立场的读者可能如何反应？ | 具体片段、可见目的、平台语境、语气、读者自主性和披露预期 | 推测反应不是真实受众测量，也不是 AI 证据 |

本地文本分析借鉴公开讨论的变化程度、局部信号集中和文档级聚合等思路，但不复刻 GPTZero 的专有模型、训练数据、权重、校准或准确率。Skill 不会把文本发送给 GPTZero 或其他第三方文本检测器。

### 一次分析如何运行

每个案例按照保留证据边界的顺序处理：

1. 获取公开正文、图片、平台语境、披露信息和规范来源 URL
2. 生成并校验 `case.json`，不绕过登录墙、私密页面、付费墙或验证码
3. 在查看检测结果之前生成 `reception.json`，减少“已知 AI 标签”对读者分析的污染
4. 在本地核验图片 C2PA，并运行简体中文写作模式检查
5. 只有在你授权后，才把逐项指定的图片发送给可选外部图片检测器
6. 在 `report.json` 和 `report.md` 中分别输出来源、写作模式与 Human Reception 结果

单个外部服务失败时，系统仍会保留成功的本地检查并生成部分报告。分析结束后会清理临时媒体文件。

### 仓库包含什么

仓库提供完整的项目级 Skill：

- `SKILL.md`：调用规则、分析顺序、安全边界和报告要求
- `scripts/`：案例校验、本地文本分析、C2PA 核验、可选图片检测器、脱敏、评估和报告生成
- `references/`：证据政策、Human Reception 量表、输入输出契约、平台流程、模型限制和研究记录
- `scripts/tests/`：长度边界、服务失败、隐私、来源证据、写作模式和读者反应测试

首版覆盖能够公开访问的 X、Reddit、LinkedIn、Instagram、TikTok、Threads 和普通网页，支持 URL、粘贴文本、附加图片或组合输入。当前不包含视频或音频分析、账号监控、批量扫描、自动处罚和独立 Web 界面。

### 安装并调用 Skill

将仓库克隆到项目的 Skill 目录，并安装可选运行依赖：

```bash
skill_dir=.agents/skills/socialmedia-gpthalf
git clone \
  https://github.com/yuzhang-zhong/socialmedia-gpthalf.git \
  "$skill_dir"
pip install -r "$skill_dir/scripts/requirements.txt"
```

随后使用公开 URL、文本或图片调用：

```text
使用 $socialmedia-gpthalf 分析这个公开社交媒体帖子，分别核验 AI 来源证据和可能的人类阅读反应。
```

如果已经准备好结构化案例，可在校验 `case.json` 和盲态生成 `reception.json` 后运行：

```bash
python scripts/social_ai_check.py analyze \
  --input case.json \
  --reception reception.json \
  --output-dir output \
  --format both
```

具体结构见[输入输出契约](references/input-output-contract.md)，URL 获取规则见[平台处理流程](references/platform-workflow.md)。

### 在边界内解释结果

来源结论包括 `verified_ai_provenance`、`strong_ai_indicators`、`conflicting_evidence`、`no_reliable_ai_evidence` 和 `insufficient_evidence`。报告会保留证据的资产范围：一张图片带有 AI 来源信息，不代表配文或整个帖子都获得了相同证明。

`strong_pattern_match` 和 `localized_pattern_match` 等中文本地标签只描述模式聚合程度，不能解释为“很可能由 AI 写作”。Human Reception 会为每类读者引用短片段，并区分可能的摩擦点、正向信号和判断限制。

使用报告时必须遵守以下边界：

- 不把“没有发现 AI 证据”解释为“人类创作”或“真实可信”
- 不把读者反感当作 AI 作者身份的证据
- 不默认上传私密、医疗、财务、未成年人或其他敏感内容
- 不把报告用于处罚、招聘、司法判断、教育处分或平台自动封禁
- 当决策依赖真实受众反应时，使用实际读者测试验证

<p align="center"><sub>Logo created for SocialMedia GPTHalf with OpenAI ImageGen.</sub></p>
