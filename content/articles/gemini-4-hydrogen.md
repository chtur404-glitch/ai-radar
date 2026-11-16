---
title: "Gemini 4 Hydrogen：便宜快手為何贏過自家前線模型"
slug: gemini-4-hydrogen
summary: "跑得快、價格扁平的一顆 Gemini 4 模型，官方稱獨立榜分數勝過自家前線款 Argon，GitHub 也把它排進 Copilot。"
category: coding
tags: [程式開發, GitHub Copilot, 思考檔次]
date: 2026-11-16
featured: false
cover:
  motif: coding
  palette: lime
tool:
  name: "Gemini 4 Hydrogen"
  maker: "Google DeepMind"
  url: "https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-hydrogen/"
  type: "程式開發與 agentic 工作模型"
  open_source: false
  cost: "API 每百萬輸入 token 1.50 美元、輸出 7.50 美元；Copilot 依用量按 Google 牌價計費"
sources:
  - label: "Google 官方部落格：Gemini 4 Hydrogen 開發者公告（2026-11-12）"
    url: "https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-hydrogen/"
  - label: "Google 官方部落格：Introducing Gemini 4 Hydrogen（2026-11-12，11-13 更新）"
    url: "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/"
  - label: "Google DeepMind 官方模型卡：Gemini 4 Hydrogen"
    url: "https://deepmind.google/models/model-cards/gemini-4-hydrogen/"
  - label: "Google Antigravity 官方部落格：Gemini 4 Hydrogen and Orchestrator（2026-11-12）"
    url: "https://antigravity.google/blog/gemini-4-hydrogen-in-google-antigravity/"
  - label: "GitHub Changelog：Gemini 4 Hydrogen in GitHub Copilot（2026-11-13）"
    url: "https://github.blog/changelog/2026-11-13-gemini-4-hydrogen-in-github-copilot/"
  - label: "GitHub Changelog：Upcoming deprecation of selected GitHub Copilot models in December（2026-11-13）"
    url: "https://github.blog/changelog/2026-11-13-upcoming-deprecation-of-selected-github-copilot-models-in-december/"
  - label: "The Decoder：Artificial Analysis 獨立評測結果整理（2026-11-13）"
    url: "https://the-decoder.com/googles-gemini-4-hydrogen-outscores-the-bigger-argon-just-four-weeks-after-its-launch/"
  - label: "TrueStandard：Gemini 4 Hydrogen 引用幻覺測試（2026-11-13）"
    url: "https://truestandard.ai/releases/gemini-4-hydrogen"
highlights:
  - "四個思考檔次，預設 high，最高階是這代新加的 xhigh"
  - "官方自稱在獨立指數拿 51 分，贏過自家前線款 Argon 的 50 分"
  - "GitHub 同日排定 3.8 Flash 在 12 月 14 日下架，接班人就是它"
  - "第三方 DOI 測試：low 檔 113 個引用只捏造 1 個"
extend:
  - "便宜快模型當 worker、前線模型當規劃者，可能成為 agent 專案的預設分工"
  - "工具商把舊模型的下架日寫死，等於逼團隊定期重測自己的提示與設定"
  - "若捏造率真的壓下來，讓模型接內部文件自動寫報告的門檻會明顯降低（推測）"
---

GitHub 在 2026-11-13 把 Gemini 4 Hydrogen 加進 Copilot 的模型選單，同一輪公告還排定了 Gemini 3.8 Flash 的下架日：12 月 14 日，而 GitHub 指定的替代品就是它。更有意思的是，這個便宜、跑得快的等級，在 Google 引用的一份獨立評測上分數超過了自家前線模型 Gemini 4 Argon。

## 一句話說它是什麼

Gemini 4 Hydrogen 是 Gemini 4 家族裡負責動手做的那一顆：寫程式、跑測試、驗證改動、在 repo 裡找問題。官方說它可以直接單獨用，也可以被 Gemini 4 Carbon 或 Argon 這類前線模型叫來當快手，或在 Antigravity 的 Orchestrator 裡跟 Carbon 自動互相接手。

## 它到底能做什麼

- **四個思考檔次**：`low`、`medium`、`high`（預設）與這代新加的 `xhigh`，官方說你只為任務需要的推理深度等待與付費。
- **一百萬 token 的 context，價格不分段**：官方公布每百萬輸入 token 1.50 美元、輸出 7.50 美元。
- **單獨用或混搭**：官方描述 Carbon 當協調者、Hydrogen 當 worker 與 verifier，在多個獨立工作區同時改動與測試。

## 為什麼值得注意

官方自稱的數字是這樣：在 Artificial Analysis Intelligence Index 上，預設 `high` 檔拿 51 分，超過 Argon 的 50 分，`xhigh` 可到 54 分；Terminal-Bench 4.1 拿 57%，而官方說 3.8 Flash 只有 18.2%。官方還稱任務完成速度快 2.5 倍、捏造的宣稱減少 5 倍以上。這些全部出自 Google 自家測試。

第三方只驗證了一部分。The Decoder 轉述 Artificial Analysis 的獨立評測：Hydrogen 在 `xhigh` 大致與 Claude Sonnet 5.5 同級，但終端機類 agentic 工作偏弱，Terminal-Bench 4.0 是 54%，Sonnet 5.5 是 64%。TrueStandard 在 11 月 13 日拿 30 條宣稱測引用真偽，`low` 檔 113 個引用裡捏造 1 個，3.8 Flash 是 141 個裡捏造 31 個；換成各自預設檔次後，差距縮小到 0 對 6.0%。

## 實際可以怎麼用

Copilot 這邊，Pro、Pro+、Max、Business、Enterprise 五種方案都能選，模型選單包含 VS Code、Visual Studio、Copilot CLI、coding agent、Copilot app、github.com、GitHub Mobile、JetBrains IDEs、Xcode、Eclipse 與 Copilot SDK，依用量計費、按 Google 牌價，而且是逐步推送。Google 那邊則在 Gemini API、AI Studio、Android Studio 與 Gemini for business 可用。

## 還沒被驗證的地方

- 「快 2.5 倍」「捏造少 5 倍」都是官方自稱。Google 沒說明用哪個測試、哪個思考檔次，第三方只能確認方向一致，無法確認倍數。
- 官方模型卡自己列的限制：知識截止到 2026 年 3 月，仍可能幻覺，思考檔次開高會吃更多 token。Artificial Analysis 估每題成本從 `high` 的 1.87 美元升到 `xhigh` 的 3.16 美元。
- GitHub 沒說它在 Copilot 裡是不是預設模型，也沒公布 Copilot 專屬的品質或延遲數字。
