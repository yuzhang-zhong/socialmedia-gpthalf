<p align="center">
  <img src="assets/socialmedia-gpthalf-logo.png" width="220" alt="SocialMedia GPTHalf logo">
</p>

<h1 align="center">SocialMedia GPTHalf</h1>

<p align="center">
  Check AI-origin evidence and likely reader reactions to public social-media content.<br>
  检查公开社交媒体内容的 AI 来源证据，以及读者可能产生的反应。
</p>

<p align="center">
  <a href="#english">English</a> · <a href="#中文">中文</a>
</p>

## English

SocialMedia GPTHalf is a Codex Skill for checking public posts, webpages, text, and images. It reports the evidence it can find and makes its limits clear.

### Why I built it

AI has made it cheap to publish at scale. One draft can be translated and rewritten for several platforms in minutes. That is useful, but it also lets content farms publish fake expertise and engagement bait at a much lower cost.

Most AI detectors reduce the question to a percentage. The number looks precise, but the evidence usually is not. A detector only sees the finished text. It cannot see who wrote the outline, how much a person edited, or whether AI changed one sentence or the whole post.

One study of seven detectors found a 61.3% average false-positive rate on its sample of human-written TOEFL essays. In that case, predictable language became [a signal of language background rather than AI authorship](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/).

Platform labels help when the metadata survives. They still miss content after some edits and reposts. Meta changed "Made with AI" to "AI info" after lightly edited media received labels that [did not match what people expected](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/). TikTok is also testing systems aimed at accounts that [post AI spam and crowd out original creators](https://newsroom.tiktok.com/helping-people-spot-and-understand-ai-generated-content-on-tiktok?lang=en-GB).

When people say a post "sounds like AI," they may mean that it is vague, repetitive, salesy, or emotionally empty. That reaction is worth explaining, but it does not prove who wrote the post. People write generic copy too, and AI-assisted writing can be specific and honest.

GPTHalf handles these questions separately. It checks origin evidence, points out visible writing patterns, and estimates how different readers may respond. It does not combine them into an "AI score."

### What it checks

| Part | What it uses | Limit |
| --- | --- | --- |
| Origin | Author disclosures, platform labels, C2PA data, and optional image checks | Missing evidence does not prove human authorship |
| Text patterns | Quoted Simplified-Chinese document and sentence patterns | A pattern match is not an AI probability |
| Reader response | Supporter, neutral-reader, and skeptic views tied to excerpts | These are estimates, not audience research or origin evidence |

The Skill accepts a public URL, pasted text, images, or a combination. It can write `report.json` and `report.md`. It does not monitor accounts, scan posts in bulk, or make enforcement decisions.

### Install

```bash
skill_dir=.agents/skills/socialmedia-gpthalf
git clone \
  https://github.com/yuzhang-zhong/socialmedia-gpthalf.git \
  "$skill_dir"
pip install -r "$skill_dir/scripts/requirements.txt"
```

### Use

```text
Use $socialmedia-gpthalf to analyze this public social media post for AI-origin evidence and likely human reader reactions.
```

See the [input and output contract](references/input-output-contract.md) for structured analysis.

### Limits

- No AI evidence does not mean "written by a human"
- A negative reader reaction does not prove AI use
- Evidence found in one image does not automatically apply to the caption or the whole post
- External image analysis requires permission for each image
- Reports should not be used for punishment, hiring, legal findings, school sanctions, or automatic bans

## 中文

SocialMedia GPTHalf 是一个 Codex Skill，用来检查公开帖子、网页、文本和图片。它会说明找到了什么证据，也会明确哪些地方无法判断。

### 为什么做这个项目

AI 把批量发布内容的成本降得很低。一份草稿可以在几分钟内翻译和改写，再投到不同平台。这当然方便，但内容农场也能用更低的成本批量生产假专业和情绪诱饵。

很多 AI 检测工具把问题简化成一个百分比。数字看起来很明确，证据却未必有那么明确。检测器只能看到最后的成稿。它不知道提纲是谁写的，也不知道人改了多少，或者 AI 只动了一句话还是写了整篇。

误报不是小问题。一项针对七种检测器的研究显示，在其人类撰写的托福作文样本上，平均误报率达到 61.3%。在这个案例里，可预测的语言更像是在反映[写作者的语言背景，而不是 AI 作者身份](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/)。

平台标签可以提供帮助，但前提是元数据没有在编辑和转载中丢失。Meta 把 "Made with AI" 改成 "AI info"，原因之一是轻微使用 AI 编辑的媒体也被贴上了[不符合用户预期的标签](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)。TikTok 也开始测试针对[批量发布 AI 垃圾内容、挤压原创作者的账号检测](https://newsroom.tiktok.com/helping-people-spot-and-understand-ai-generated-content-on-tiktok?lang=en-GB)。

人们说一篇帖子 "像 AI"，有时是在说它空泛、重复、像广告，或者没有真实情绪。这种阅读感受值得分析，但不能拿来证明作者身份。人也会写出模板文案，AI 辅助的内容也可能具体、坦诚。

GPTHalf 把这些问题分开处理。它检查来源证据，指出文本中能看到的写作模式，再分析不同读者可能怎么理解。它不会把这些内容混成一个 "AI 率"。

### 检查内容

| 部分 | 使用的依据 | 判断边界 |
| --- | --- | --- |
| 来源 | 作者披露、平台标签、C2PA 数据和可选图片检查 | 没有证据不能证明由人类创作 |
| 文本模式 | 带原文引用的简体中文文档级和句子级模式 | 命中模式不等于 AI 概率 |
| 读者反应 | 支持者、中立读者和怀疑者对具体片段的反应 | 这里只是推测，不是真实受众调查，也不是来源证据 |

Skill 支持公开 URL、粘贴文本、图片或组合输入，可以生成 `report.json` 和 `report.md`。它不监控账号，不批量扫描帖子，也不负责处罚或封禁。

### 安装

```bash
skill_dir=.agents/skills/socialmedia-gpthalf
git clone \
  https://github.com/yuzhang-zhong/socialmedia-gpthalf.git \
  "$skill_dir"
pip install -r "$skill_dir/scripts/requirements.txt"
```

### 使用

```text
使用 $socialmedia-gpthalf 分析这个公开社交媒体帖子，分别核验 AI 来源证据和可能的人类阅读反应。
```

结构化分析方式见[输入输出契约](references/input-output-contract.md)。

### 使用限制

- 没有发现 AI 证据，不等于证明由人类创作
- 读者反感，不能证明内容使用了 AI
- 一张图片中的来源证据，不能自动扩大到配文或整个帖子
- 外部图片分析需要逐张授权
- 报告不应该用于处罚、招聘、司法判断、教育处分或自动封禁

<p align="center"><sub>Logo created for SocialMedia GPTHalf with OpenAI ImageGen.</sub></p>
