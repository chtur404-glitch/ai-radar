---
title: "DeepMind Genie 4：世界有了聲音，角色還會跟你對話"
slug: genie-4
summary: "DeepMind 的 Genie 4 讓即時生成的世界自帶環境音與角色對話，畫面、聲音一次生成。目前只給信任測試者，還沒有價格與開放日期。"
category: fun
tags: [世界模型, 即時生成, 多模態, 語音生成]
date: 2026-11-16
featured: false
cover:
  motif: fun
  palette: magenta
tool:
  name: "Genie 4"
  maker: "Google DeepMind"
  url: "https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/"
  type: "即時互動世界模型"
  open_source: false
  cost: "目前未公布價格；僅限信任測試者使用"
sources:
  - label: "Google DeepMind 官方部落格：Genie 4（2026-10-27）"
    url: "https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/"
  - label: "Google DeepMind 官方模型頁：Genie 4"
    url: "https://deepmind.google/models/genie/"
  - label: "Google DeepMind 官方部落格：Genie 3（2025-08-05）"
    url: "https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/"
  - label: "Google 官方部落格：Project Genie 開放給 Ultra 訂閱戶（2026-01-29）"
    url: "https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/"
  - label: "TechCrunch：Genie 4 報導（2026-10-27）"
    url: "https://techcrunch.com/2026/10/27/googles-genie-4-world-model-adds-audio-more-realistic-worlds-and-real-time-steering/"
  - label: "The Batch（DeepLearning.AI）：Genie 4 與 Gemini"
    url: "https://www.deeplearning.ai/the-batch/world-models-become-robot-playgrounds"
  - label: "VP Land：Genie 4 實測"
    url: "https://www.vp-land.com/stories/we-turned-real-photos-into-walkable-worlds-with-googles-genie-4-then-debated-dessa-iatse-a"
highlights:
  - "世界不再無聲：音樂、環境音與角色對話跟畫面一起生成"
  - "Gemini 3.8 Flash 當導演，逐格檢查每一步有沒有做到"
  - "TechCrunch 報導場景可撐約兩分鐘，官方只說「幾分鐘」"
  - "目前只有信任測試者能用，沒有價格，也沒有開放日期"
extend:
  - "機器人與代理的無限訓練場：同一個任務可以換場景反覆重練"
  - "拍片勘景：丟一張場地照片就能先走進去，試完鏡位再花錢搭景"
  - "若對話與音訊真的穩定，互動式劇場與語言學習情境都可能成立（推測）"
---

DeepMind 的 Genie 4 生成世界時，聲音和畫面是一起長出來的：風吹過樹葉、樂團演奏，角色還會轉頭跟你講話。官方說這是它第一個原生生成音訊的即時世界模型，前一代 Genie 3 則無聲。

## 一句話說它是什麼

一句話或一張照片當起點，模型即時長出一個能走進去、隨時改天氣、加人加物件的世界，還自帶環境音與對話。

## 它到底能做什麼

- **即時改設定**：鍵盤走動、轉鏡頭，隨時打一句話換天氣、加角色；官方說 Gemini 會把指令改寫成符合當下場景的說法。
- **原生音訊與對話**：每個世界有自己的環境音與音樂，角色能對話，會對你或場景裡的事做出反應。
- **Gemini 在迴圈裡當導演**：Gemini Omni 讓外觀與行為像真的；Gemini 3.8 Flash 是官方說的「迴圈中的引導代理」，一邊看畫面一邊把目標拆成步驟、逐格檢查成功了沒，場景變了就改計畫。

## 為什麼值得注意

Genie 3 在 2025 年 8 月發表時是 720p、24 fps、無聲，一致性只維持「數分鐘」。Genie 4 補上聲音與對話，據 TechCrunch 報導場景可撐約兩分鐘，是 Genie 3 兩倍；但官方只寫「幾分鐘的連續互動」，沒公布解析度、幀率或延遲。

## 實際可以怎麼用

目前只有信任測試者能碰。Project Genie 今年 1 月底先在美國開放給 Ultra 訂閱戶，現在跑的是 Genie 3；官方說 Genie 4 接下來一樣先給訂閱戶與 API 早期夥伴。VP Land 的實測更具體：丟一張古堡照片就能走進它生成的入口大廳，每個 session 兩分鐘，還能錄成影片下載；但鏡頭一轉開，整間酒吧和那隻鯨魚就不見了。

## 還沒被驗證的地方

- 官方自己列的限制：連續互動只有幾分鐘；細節與物件恆存性會漂移，跑得久或改過多次指令後更明顯。複雜物理互動、音訊準確度與可讀文字也都還在研究中。
- 沒有量化評測。The Batch 指出官方只有精選示範片段，沒給量化數據；音訊多準，也只有 Google 自己的影片能看。
- 影片與音訊都帶 SynthID 浮水印，這是官方說法，尚無獨立驗證。
