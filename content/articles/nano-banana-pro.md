---
title: "Nano Banana Pro：海報上的字，AI 這次寫對了"
slug: nano-banana-pro
summary: "Google DeepMind 推出的圖像生成與編輯模型，官方自稱能在圖上渲染正確可讀的文字，做資訊圖表、海報與 mockup 都合用。"
category: image
tags: [圖像生成, 文字渲染, 資訊圖表, 品牌素材]
date: 2026-11-16
featured: true
rank: 1
cover:
  motif: image
  palette: amber
tool:
  name: "Nano Banana Pro"
  maker: "Google DeepMind"
  url: "https://blog.google/innovation-and-ai/products/nano-banana-pro/"
  type: "圖像生成與編輯模型（Gemini 3 Pro Image）"
  open_source: false
  cost: "Gemini API 每張 1K／2K 圖 0.134 美元、4K 0.24 美元；Gemini app 內隨訂閱方案提供"
sources:
  - label: "Google 官方部落格：Nano Banana Pro 發表（2025-11-20）"
    url: "https://blog.google/innovation-and-ai/products/nano-banana-pro/"
  - label: "Google Workspace Updates：Nano Banana Pro 進 Slides、Vids 與 NotebookLM（2025-11-20）"
    url: "https://workspaceupdates.googleblog.com/2025/11/workspace-nano-banana-pro.html"
  - label: "Gemini API 模型文件：Gemini 3 Pro Image（Nano Banana Pro）"
    url: "https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image"
  - label: "Google 官方部落格：Nano Banana 2 發表（2026-02-26）"
    url: "https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/"
  - label: "Google Cloud 部落格：Nano Banana 2 與 Pro 正式 GA（2026-05-28）"
    url: "https://cloud.google.com/blog/products/ai-machine-learning/nano-banana-2-and-nano-banana-pro-are-generally-available/"
  - label: "Google 開發者部落格：原始 Nano Banana．Gemini 2.5 Flash Image（2025-08-26）"
    url: "https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/"
highlights:
  - "官方自稱目前最會渲染文字的圖像模型，從一行標語到整段文字都寫得對"
  - "最多混合 14 張參考圖、維持最多 5 個人的長相一致"
  - "API 每張 1K／2K 圖 0.134 美元、4K 0.24 美元"
  - "它是推理模型，會先畫最多兩張不算錢的「思考圖」再定稿"
extend:
  - "接上 Google 搜尋的即時資料，隨手生出今天的氣象資訊圖（推測）"
  - "把整份財報 PDF 丟進去，直接產出一頁能放進簡報的視覺化重點（推測）"
  - "串進內部設計流程，讓非設計師也能生出風格一致的品牌素材（推測）"
---

## 一句話說它是什麼

Nano Banana Pro（技術名 Gemini 3 Pro Image）是 Google DeepMind 2025 年 11 月發表的圖像模型，官方稱它是目前最能生出正確可讀文字的模型。

## 它到底能做什麼

- **文字與翻譯**：官方示範把包裝上的英文換成韓文。文件列 15 種建議語言，含日、韓、印地與簡中，繁中未列入。
- **資訊圖表**：把筆記變流程圖、資料變圖表，還能用 Google 搜尋接地抓即時天氣。
- **素材控制**：最多混 14 張參考圖、維持 5 個人的長相一致，可調光線與角度，輸出 2K／4K。
- **Thinking 模式**：它是推理模型，會先畫最多兩張不算錢的「思考圖」驗構圖。

## 為什麼值得注意

生圖模型長年搞不定圖上的文字，海報、菜單、介面 mockup 幾乎不能用。它補上這塊，把「好看的圖」推進到「能用的素材」。

## 實際可以怎麼用

- 一句話把英文菜單翻成中文重排。
- 走官方 API（`gemini-3-pro-image`）量產產品 mockup。
- 在 NotebookLM 把整份資料來源變成一張資訊圖表。

## 費用與後續

Gemini API 每張 1K／2K 圖 0.134 美元、4K 0.24 美元，Batch 半價；輸出嵌 SynthID 浮水印。2026 年 2 月 Google 再推更快的 Nano Banana 2（Gemini 3.1 Flash Image），同年 5 月起在 Gemini API 與 Vertex AI 一般提供。

## 還沒被驗證的地方

「最強文字渲染」多來自官方自稱與媒體轉述，缺第三方複現；4K 在 2026 年 5 月 GA 時仍只是 preview。Nano Banana 2 的數字不能套在 Pro 上。
