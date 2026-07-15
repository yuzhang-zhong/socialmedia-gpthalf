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

SocialMedia GPTHalf is a Codex Skill for examining public social-media content without presenting uncertain detection as fact. It separates origin evidence, writing-pattern observations, and likely reader reactions because those are three different questions.

### Why this project exists

Generative models did not invent spam, astroturfing, content farms, engagement bait, fake expertise, or corporate grief posts. They reduced the cost of producing, translating, personalizing, and repeating them. When ranking systems reward frequency and emotional response, cheaper production creates more content without creating more truth.

The scarce resource online is therefore shifting. Content is abundant; credible intent, accountable authorship, and earned attention are not. A polished post may represent lived experience, careful editing, outsourced marketing, a model-generated draft, or a mixture of all four. The published text is a lossy trace of that process, not an audit log.

Platforms now acknowledge the scale problem. In July 2026, [TikTok announced tests aimed at accounts that mass-produce AI spam and crowd out original creators](https://newsroom.tiktok.com/helping-people-spot-and-understand-ai-generated-content-on-tiktok?lang=en-GB). Meta previously changed “Made with AI” to “AI info” after industry indicators labeled some lightly edited media in ways that [did not match people’s expectations](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/). The hard problem is no longer spotting an “AI aesthetic.” It is preserving context across tools and reposts, then explaining that context without overstating it.

Text detectors can make the same mistake at a larger moral scale. A percentage looks objective, but the detector never observed the drafting process. It cannot see whether a person outlined, translated, rewrote, prompted, or accepted a suggestion. A published study of seven detectors reported a 61.3% average false-positive rate on its sample of human-written TOEFL essays, showing how predictable language can become [a proxy for linguistic background rather than AI authorship](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/).

The label “AI-generated” can then become a shortcut for judgments that should be stated directly. Readers may actually object to manipulation, counterfeit intimacy, empty authority, opportunistic branding, or industrial repetition. Humans can produce all of those. AI-assisted work can also be specific, disclosed, useful, and respectful.

This distinction matters because reader aversion is evidence about reception, not evidence about origin. A post can be human-written and unbearable. Another can use AI and still respect its audience. Treating “annoying,” “generic,” and “machine-made” as synonyms hides the social behavior that deserves criticism.

### The project’s position

GPTHalf rejects the promise of one totalizing “AI score.” It follows three claims:

- **Provenance should answer provenance:** verified disclosures, platform labels, and valid Content Credentials can support scoped origin claims
- **Patterns should remain patterns:** model-like wording can guide inspection, but it cannot reconstruct authorship from the final text
- **Reception should answer reception:** concrete excerpts can explain why supporters, neutral readers, and skeptics may react differently

The word “Half” is deliberate. The tool should know where its evidence ends. Honest uncertainty is more useful than false precision when a result may affect a person’s reputation.

### What the Skill does

The Skill keeps its three analytical layers independent:

| Layer | Purpose | Output boundary |
| --- | --- | --- |
| Origin assessment | Check disclosures, platform signals, local C2PA data, and optional selected-image signals | Missing evidence never proves human authorship |
| Writing-pattern analysis | Highlight grounded Simplified-Chinese document and sentence patterns | Pattern density is not an AI probability |
| Human Reception | Estimate reactions from supporter, neutral-reader, and skeptic stances | Estimated reactions are not measured audience behavior or origin evidence |

It accepts public URLs, pasted text, attached images, or combinations of them. It can produce `report.json` and `report.md`. It does not provide account surveillance, bulk enforcement, video analysis, or a standalone web interface.

### Install and invoke

Clone the Skill into a project and install its optional runtime dependencies:

```bash
skill_dir=.agents/skills/socialmedia-gpthalf
git clone \
  https://github.com/yuzhang-zhong/socialmedia-gpthalf.git \
  "$skill_dir"
pip install -r "$skill_dir/scripts/requirements.txt"
```

Invoke it with a public post, text, or image:

```text
Use $socialmedia-gpthalf to analyze this public social media post for AI-origin evidence and likely human reader reactions.
```

See the [input and output contract](references/input-output-contract.md) for structured analysis.

### Use results responsibly

- Do not translate missing AI evidence into “human-authored” or “authentic”
- Do not use reader aversion as proof of AI authorship
- Do not treat one image’s provenance as proof about its caption or the whole post
- Do not upload sensitive content for external analysis without explicit, asset-level consent
- Do not use reports for punishment, hiring, legal findings, education sanctions, or automatic bans

## 中文

SocialMedia GPTHalf 是一个 Codex Skill，用于检查公开社交媒体内容，同时避免把不确定的检测包装成事实。它严格区分来源证据、写作模式和读者反应，因为这是三个不同的问题。

### 为什么要做这个项目

生成式模型没有发明垃圾信息、水军、内容农场、情绪诱饵、伪造的专业感或品牌借势。它只是大幅降低了生产、翻译、个性化和重复投放这些内容的成本。当平台排序机制奖励发布频率和情绪反应时，生产成本下降带来的是更多内容，而不是更多真实。

互联网的稀缺资源因此正在改变。内容已经过剩，可信的表达动机、可追责的作者身份和真正赢得的注意力却没有增加。一篇流畅的帖子可能来自亲身经验、认真编辑、外包营销、模型起草，也可能混合了全部过程。最终文本只是创作过程留下的不完整痕迹，不是一份审计记录。

平台已经开始承认规模化问题。2026 年 7 月，[TikTok 宣布测试针对批量发布 AI 垃圾内容、挤压原创作者的账号检测](https://newsroom.tiktok.com/helping-people-spot-and-understand-ai-generated-content-on-tiktok?lang=en-GB)。Meta 此前也把“Made with AI”改为“AI info”，因为行业标记曾把轻微 AI 编辑的媒体贴上与[公众预期不符的标签](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)。真正困难的问题已经不是识别某种“AI 味”，而是在跨工具编辑和转载后保存上下文，并且不过度解读这些上下文。

文本检测器可能把同样的错误放大成道德判断。一个百分比看起来客观，但检测器从未观察真实的写作过程。它不知道作者是否列过提纲、做过翻译、反复改写、使用提示词或只接受了一条建议。一项针对七种检测器的研究显示，在其人类撰写的托福作文样本上，平均误报率达到 61.3%。这说明可预测的语言可能成为[语言背景的替代指标，而不是 AI 作者身份的证据](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/)。

“AI 生成”随后很容易变成一种道德捷径，代替本来应该被直接说出的批评。读者真正反感的可能是操控、伪造亲密感、空洞权威、商业借势和工业化重复。这些问题都可以由人类制造。AI 辅助的内容也可能具体、透明、有用，并且尊重读者。

这种区分非常重要，因为反感只能说明阅读感受，不能证明内容来源。人工写作完全可能令人难以忍受，AI 辅助内容也可能对受众保持诚实。把“令人反感”“模板化”和“机器生成”当作同义词，反而会遮蔽真正应该被批评的社会行为。

### 项目的核心立场

GPTHalf 拒绝用一个总分概括全部问题。它坚持三项原则：

- **来源证据只回答来源：** 有效披露、平台标签和 Content Credentials 只能支持范围明确的来源判断
- **写作模式只保留为模式：** 模型式措辞可以提示检查方向，但不能从最终文本反推出完整创作过程
- **读者反应只回答感受：** 具体片段可以解释支持者、中立读者和怀疑者为何产生不同反应

名字中的“Half”是有意为之。工具应该知道自己的证据在哪里停止。当结果可能影响一个人的声誉时，诚实的不确定性比虚假的精确更有价值。

### Skill 做什么

Skill 始终分开三个分析层：

| 分析层 | 分析目的 | 输出边界 |
| --- | --- | --- |
| 来源核验 | 检查披露、平台信号、本地 C2PA 数据和可选的指定图片信号 | 缺少证据永远不能证明由人类创作 |
| 写作模式分析 | 标记有原文依据的简体中文文档级和句子级模式 | 模式密度不是 AI 概率 |
| Human Reception | 推测支持者、中立读者和怀疑者的阅读反应 | 推测反应不是真实受众测量，也不是来源证据 |

它支持公开 URL、粘贴文本、附加图片或组合输入，并可生成 `report.json` 与 `report.md`。当前不包含账号监控、批量执法、视频分析或独立 Web 界面。

### 安装并调用

将 Skill 克隆到项目目录，并安装可选运行依赖：

```bash
skill_dir=.agents/skills/socialmedia-gpthalf
git clone \
  https://github.com/yuzhang-zhong/socialmedia-gpthalf.git \
  "$skill_dir"
pip install -r "$skill_dir/scripts/requirements.txt"
```

随后使用公开帖子、文本或图片调用：

```text
使用 $socialmedia-gpthalf 分析这个公开社交媒体帖子，分别核验 AI 来源证据和可能的人类阅读反应。
```

结构化分析方式见[输入输出契约](references/input-output-contract.md)。

### 负责任地使用结果

- 不把“没有发现 AI 证据”解释为“人类创作”或“真实可信”
- 不把读者反感当作 AI 作者身份的证明
- 不把一张图片的来源信息扩大为对配文或整个帖子的证明
- 未经逐项明确授权，不把敏感内容上传到外部分析服务
- 不把报告用于处罚、招聘、司法判断、教育处分或平台自动封禁

<p align="center"><sub>Logo created for SocialMedia GPTHalf with OpenAI ImageGen.</sub></p>
