---
title: "8.86 億參數的語音模型，在手機瀏覽器裡即時複製你的聲音"
slug: zonos3-mini
summary: "Zyphra 開源的 ZONOS3-Mini 是即時 TTS 模型，幾秒參考音檔就能複製音色，官方自稱瀏覽器內第一段音訊不到 570 毫秒，運算全在裝置上跑。"
category: audio
tags: [語音合成, 聲音複製, 邊緣運算]
date: 2026-11-16
featured: true
rank: 3
cover:
  motif: audio
  palette: cyan
tool:
  name: "ZONOS3-Mini"
  maker: "Zyphra"
  url: "https://zyphra.com/zonos3-mini/localplayground/lite"
  type: "零樣本聲音複製的即時語音合成模型（TTS）"
  open_source: true
  cost: "模型與權重 Apache 2.0、推論程式 MIT，免費；官方雲端 Zyphra Cloud 另計費"
sources:
  - label: "Zyphra 官方發表頁（2026-11-09）"
    url: "https://www.zyphra.com/our-work/zonos3-mini/"
  - label: "Zyphra 官方技術部落格（Hugging Face，2026-11-11）"
    url: "https://huggingface.co/blog/Zyphra/zonos3-mini"
  - label: "ZONOS3-Mini Technical Report（arXiv:2611.16525）"
    url: "https://arxiv.org/abs/2611.16525"
  - label: "官方 GitHub repo（推論伺服器與程式碼）"
    url: "https://github.com/Zyphra/ZONOS3-Mini"
  - label: "Hugging Face 模型卡與預設聲音清單"
    url: "https://huggingface.co/Zyphra/ZONOS3-Mini"
  - label: "第三方實測：無 GPU 的 4 核心 Linux VM 跑 C++/ggml 版"
    url: "https://aifrontierpost.com/articles/zonos3-mini-voice-cloning-tts-tutorial/"
  - label: "第三方實測：雲端 8 vCPU VM 的 CPU 計時（2026-11-12）"
    url: "https://webdiga.com/zonos3-mini-local-tts/"
highlights:
  - "稀疏專家網路，總參數 8.86 億、每次只啟用約 1 億"
  - "自製的語音編碼器把音訊壓成每秒 15 格"
  - "自家評測報出 6.71% 錯誤率，尚無獨立複現"
  - "只用兩天半、112 張 H100 就訓練完成，權重開源"
extend:
  - "接進手機語音助理，回覆不必等雲端往返，斷線也能講話（推測）。"
  - "遊戲與有聲書可用同一顆模型替每個角色配音，離線批次生成（推測）。"
  - "配上本地 LLM，能做成聲音完全不出裝置的對話小硬體（推測）。"
---

給它幾秒鐘的錄音，它就能用那個聲音說話，而且整段運算留在你自己的裝置上。Zyphra 在 2026 年 11 月 9 日釋出的 ZONOS3-Mini，是零樣本聲音複製的即時 TTS 模型，官方自稱在 Pixel 9 的手機瀏覽器裡，第一段音訊不到 570 毫秒就出來。

## 打開網頁就能玩

Zyphra 的網頁 playground 是門檻最低的入口：第一次進站下載模型，之後瀏覽器會快取，運算全部透過 WebGPU 在你自己的 GPU 上跑，不用安裝也不用伺服器（`zyphra.com/zonos3-mini/localplayground/lite`）。除了複製聲音，它內建 27 個預設聲音，能調年齡、口音、情緒與語速。要接進自己的服務，可用 SGLang-Omni 起一個 OpenAI 相容的 `/v1/audio/speech` 端點，串流吐出 44.1kHz 音訊。

## 為什麼這麼小還能這麼快

它是 11 層語言模型混用 gated DeltaNet 與全域注意力，加上 latent MoE，總參數 886M、每個 token 只啟用 100M（技術報告的數字，官方部落格寫 800M）。另一個關鍵是自製的 ZAC-1 codec：把 44.1kHz 音訊壓成 15Hz 的 frame，序列長度只有前一代 86Hz codec 的 1/5.7。官方說這顆模型只用 112 張 H100 訓練 2.5 天。

## 數字要看是誰說的

官方在自家 ZTTS2-Eval（55 個語言集，35 clean、20 in the wild）報出 macro WER 6.71%，並稱在開源模型中排第一；自家設計的 benchmark、自報數據，沒有獨立複現。延遲數字自家也有出入：部落格寫瀏覽器內不到 570 毫秒與 150 毫秒，同一份技術報告的 WebGPU 段落卻寫低於 800 與 450 毫秒。伺服器端官方自稱單張 H100 上單請求 85 毫秒出聲、8 個並行時中位數 80 毫秒，並說 64 個並行時峰值吞吐達 457 倍即時。

## 已經有人真的跑起來

有人用 4 核心、沒有 GPU 的 Linux VM 跑起 C++/ggml 版本；另一份在雲端 VM 的實測量到英文約 2.0 至 2.3 倍即時、複製 13 秒參考音檔約 1.5 倍即時。官方也釋出 MLX、WebGPU、CUDA 與 ggml 版本，量化檔從 0.66GB 到 1.03GB；配音可以完全離線，不必付雲端 API 的錢。

## 還沒被驗證的地方

模型卡說支援 43 種語言，playground 選單只列 10 種（官方回覆：任何語言的文字都能用預設聲音念）。音質沒有獨立評測，單人實測心得也顯示不同語言落差明顯。發布資料沒提到水印或濫用防護——幾秒音檔就能複製音色，用別人的聲音前先取得同意。
