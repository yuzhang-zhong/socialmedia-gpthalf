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

---

## English

`socialmedia-gpthalf` is a Codex Skill for examining public posts, webpages, pasted text, and images. It keeps three questions separate:

- **Provenance:** verified disclosures, platform labels, C2PA, and optional image-model signals.
- **Writing patterns:** explainable Simplified-Chinese pattern matches—descriptive only, never an “AI percentage.”
- **Human reception:** grounded reactions from supporter, neutral, and skeptical reader stances.

### Why GPTHalf?

AI detection is rarely binary. The Skill reports what is verified, what merely resembles modeled patterns, what readers may dislike, and where evidence stops.

### Quick start

```bash
git clone https://github.com/yuzhang-zhong/socialmedia-gpthalf.git .agents/skills/socialmedia-gpthalf
pip install -r .agents/skills/socialmedia-gpthalf/scripts/requirements.txt
```

Then invoke:

```text
Use $socialmedia-gpthalf to analyze this public social media post for AI-origin evidence and likely human reader reactions.
```

The analyzer can also produce `report.json` and `report.md` from validated `case.json` and blind `reception.json` inputs. See [the input/output contract](references/input-output-contract.md).

### Guardrails

- Missing AI evidence never proves human authorship.
- Reader aversion never proves AI authorship.
- External image analysis requires explicit consent and per-image selection.
- Local paths, API keys, and raw provider responses are not retained in reports.
- Do not use the output for punishment, hiring, legal findings, or automatic bans.

## 中文

`socialmedia-gpthalf` 是一个 Codex Skill，用于检查公开帖子、网页、粘贴文本和图片。它严格区分三个问题：

- **来源证据：** 作者披露、平台标签、C2PA，以及可选的图片模型信号。
- **写作模式：** 可解释的简体中文模式命中；只做描述，不输出虚假的“AI 率”。
- **阅读感受：** 从支持者、中立读者和怀疑者视角，给出有原文依据的推测反应。

### 为什么叫 GPTHalf？

AI 检测很少是非黑即白。这个 Skill 会分别说明：什么得到了验证、什么只是模式相似、什么可能令人反感，以及证据在哪一步停止。

### 快速开始

```bash
git clone https://github.com/yuzhang-zhong/socialmedia-gpthalf.git .agents/skills/socialmedia-gpthalf
pip install -r .agents/skills/socialmedia-gpthalf/scripts/requirements.txt
```

然后调用：

```text
使用 $socialmedia-gpthalf 分析这个公开社交媒体帖子，分别核验 AI 来源证据和可能的人类阅读反应。
```

统一分析命令可根据校验后的 `case.json` 和盲态生成的 `reception.json` 输出 `report.json` 与 `report.md`。详见[输入输出契约](references/input-output-contract.md)。

### 使用边界

- 没有发现 AI 证据，不等于证明由人类创作。
- 读者反感，不构成 AI 来源证据。
- 外部图片分析必须明确授权并逐图选择。
- 报告不保留本机路径、API 密钥或完整第三方响应。
- 不得用于处罚、招聘、司法判断或平台自动封禁。

---

<p align="center"><sub>Logo created for SocialMedia GPTHalf with OpenAI ImageGen.</sub></p>
