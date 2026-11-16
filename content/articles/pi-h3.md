---
title: "pi-H3：2 步生出 5 秒影片，比播放還快，連解碼器都省了"
slug: pi-h3
summary: "只要 2 或 4 步就生出影片：最後一步直接預測像素、跳過 VAE 解碼器，官方自稱單張 B200 上 3.8 秒生成 5 秒立體聲影片。"
category: video
tags: [影片生成, 少步蒸餾, 無解碼器, MiniMax H3]
date: 2026-11-16
featured: true
rank: 2
cover:
  motif: video
  palette: violet
tool:
  name: "pi-H3"
  maker: "Stanford University（部分工作於 Luma AI 完成）"
  url: "https://huggingface.co/spaces/Lakonik/pi-H3"
  type: "少步影片生成模型（MiniMax H3 蒸餾版）"
  open_source: true
  cost: "Hugging Face demo 免費試用；權重與推理程式碼 2026-11-16 當週釋出"
sources:
  - label: "官方部落格：pi-H3: Video Generation in 2–4 Steps Without a VAE Decoder（2026-11-10）"
    url: "https://hanshengchen.com/blog/pi-h3/"
  - label: "Hugging Face demo（帳號 Lakonik）"
    url: "https://huggingface.co/spaces/Lakonik/pi-H3"
  - label: "MiniMax H3 開源公告（2026-08-03）"
    url: "https://www.minimax.io/news/minimax-h3-open-source"
  - label: "Sol-H3 論文（arXiv:2609.35110）"
    url: "https://arxiv.org/abs/2609.35110"
  - label: "LakonLab（權重與程式碼預定釋出處）"
    url: "https://github.com/Lakonik/LakonLab"
highlights:
  - "只要 2 或 4 個 sampling step 就完成整段影片，最後一步直接預測像素"
  - "官方自稱單張 B200 上 5 秒 768p 立體聲影片端到端 3.8 秒，比播放還快"
  - "官方自稱比 Sol-H3 快 2.4–2.7 倍（2 步），但尚無第三方複現"
  - "video VAE decoder 整段被刪掉，改由 denoiser 最後一步自己算像素"
extend:
  - "若 DWD 能推廣到其他高壓縮比模型，未來文生圖也可能不必再過解碼器（推測）"
  - "步數壓到 2 步，讓手機或消費級顯卡即時生成影片變得有機會（推測）"
  - "同一套思路已用在 Qwen-Image、FLUX.1 的 4 步流程上，圖像端可能更快普及（推測）"
---

## 把「慢慢去噪」壓到只剩兩步

一般影片生成模型要跑幾十步去噪，最後還得過一段 VAE 解碼才看得到畫面。pi-H3 把前者砍到 2 或 4 步，後者整個刪掉——作者稱這個方法為 DWD（Decoding Without a Decoder）：最後一步不送去解碼，而是讓 denoiser 自己直接吐出乾淨的像素。

官方數字是這樣：在單張 NVIDIA B200 上，端到端生成 5 秒 768p、帶立體聲的影片只要 3.8 秒，10 秒版本 9.2 秒，兩者都比影片實際播放時間短。15 秒版本是 18.6 秒，這一段就慢過播放了。它建立在 MiniMax 於 2026 年 8 月開源的 H3 之上，是 H3 的蒸餾加速版，不是取代。

## 快到什麼程度

官方公布的比較如下，全部是官方自報、尚無獨立複現：

- 2 步版本比 Sol-H3 快 2.4–2.7 倍，4 步版本快 1.2–1.4 倍
- 計時涵蓋 5–15 秒影片，範圍從文字編碼一路算到影片與音訊解碼完成
- 官方自己也標明：Sol-H3 的數字取自它自己的論文、量在 GB200 上，pi-H3 則量在 B200，兩者硬體不同

## 為什麼快

官方把加速拆成三件事：步數變少、解碼器拿掉、FP8 量化。方法上是兩個技術疊起來：

- **pi-Flow v2**：資料免費的少步蒸餾法，是作者群 ICLR 2026 那篇 pi-Flow 的完整升級版，改善 2 步時容易出現的結構崩壞
- **DWD**：最後一步不進 VAE decoder，改由 denoiser 直接預測乾淨像素；這一步略貴，但換掉整個解碼階段

官方也承認 DWD 用在 H3 上仍是實驗階段——H3 每個 token 對應 4×32×32×3 通道像素，壓縮比異常高，他們還沒足夠算力把它調到最好。

## 現在能玩到什麼

Hugging Face 的 demo 已經上線、可以免費試。權重與推理程式碼排在 11 月 16–22 那週釋出，訓練程式碼晚一點、透過作者自己的 LakonLab 開源；ComfyUI 端則由既有的 ComfyUI-piFlow 擴充支援（需 ComfyUI 0.23.0 以上）。

## 還沒被驗證的地方

3.8 秒、2.4–2.7 倍這些數字目前全部來自官方部落格，沒有第三方跑過同一組測試；Sol-H3 的對照又量在不同硬體上，跨硬體比較本來就容易把差距拉大。要等權重真的下來、有人在消費級顯卡上跑一遍，才知道它「快」換來的是不是畫質。
