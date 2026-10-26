# 01. コンセプト & 仕様定義 (Concept & Specification)

## 1. 概要 (Overview)
`UT_novel` は、ユーザーが記述した **Markdown形式の台本ファイル** を読み込み、**Undertale風の会話シーンと背景動画を合成した動画 (MP4)** をコマンド一発で自動生成するツールです。

基本言語は **英語 (English)** をベースとして設計されており、Undertale特有のピコピコ文字送り音（Voice Blips）に加えて、**AI音声合成（TTS: Text-to-Speech）との自動同期** を初期設計から標準機能として視野に入れています。

### 主なターゲット・ユースケース
- **ショート動画制作**: YouTube Shorts / TikTok / Instagram Reels 用の縦型（9:16）英語・多言語会話動画
- **横型動画制作**: 通常のYouTube動画用（16:9）の会話シーンや解説動画
- **二次創作・AIノベル制作**: Undertale風のファン創作、AIキャラクターによる対話動画の量産

---

## 2. 音声システムのデュアル設計 (Dual Audio Modes)

本ツールはキャラクターごとに2種類の音声モードをサポートします。

### モードA: `blip` モード (Undertaleクラシックスタイル)
- **文字送り音**: アルファベット（`a-z`, `A-Z`, `0-9`）が表示されるたびに、キャラ固有の短いSE（0.05秒程度のWAV）を再生。
- **スペース無音**: 単語間のスペース `' '` では音を鳴らさない（Undertale独特のリズム）。
- **句読点ウェイト**: `,`（約0.2秒）、`.`, `!`, `?`（約0.4〜0.5秒）で音を鳴らさずに停止。

### モードB: `tts` モード (英語AI音声合成 & 自動リップシンク)
- **音声生成**: セリフテキストからTTSプロバイダーを介して英語音声を自動生成。
- **音声同期タイピング**: 生成された音声の長さ（デュレーション）および単語タイミングに合わせて、文字のタイピング速度・セリフ全体の表示期間を完全自動同期。
- **リップシンク**: 音声が再生されている間、キャラクターの顔グラフィックが口パク・アニメーションを行う。
- **カスタム音声指定**: ユーザーが録音した手動音声ファイル（`.wav` / `.mp3`）の割り当ても可能。

---

## 3. Markdown台本仕様 (Script Specification)

### サンプル台本 (`sample.md`)
```markdown
---
title: "Meeting in the Ruins"
aspect_ratio: "16:9"       # "16:9" (1920x1080) または "9:16" (1080x1920)
fps: 30
bg: "assets/bg/ruins_hall.mp4" # 背景動画 または 静止画
bgm: "assets/bgm/fallen_down.mp3"
bgm_volume: 0.6

characters:
  toriel:
    name: "Toriel"
    font: "determination"
    # 音声設定: "blip" (文字音) または "tts" (音声合成)
    voice_mode: "blip"
    blip_sound: "assets/se/voice_toriel.wav"
    default_face: "smile"
    faces:
      smile: "assets/char/toriel/smile.png"
      worried: "assets/char/toriel/worried.png"
  
  sans:
    name: "sans"
    font: "comic_sans"
    voice_mode: "tts"
    tts:
      provider: "piper" # "piper" (ローカル軽量), "openai", "elevenlabs" 等
      voice_id: "en_US-lessac-medium"
      speed: 1.0
    default_face: "normal"
    faces:
      normal: "assets/char/sans/normal.png"
      wink: "assets/char/sans/wink.png"

  narrator:
    font: "determination"
    voice_mode: "blip"
    blip_sound: "assets/se/voice_default.wav"
---

# シーン開始

* toriel(smile): Hello, my child.[wait: 0.3] Welcome to the RUINS.
* toriel(worried): Do not be afraid, I will guide you through the catacombs.

# TTSで喋るキャラクターの例
* sans(wink): hey. you look like you've been working down to the [shake]bone[/shake].

# 直接音声ファイルを指定する場合の例
* narrator: [voice: "assets/voice/custom_take.wav"] (A strange silence fills the room.)
```

---

## 4. 英語ベースのテキスト・レイアウト処理

1. **Word Wrapping (単語単位の自動改行)**
   - 英語は単語の途中で不自然に改行されると可読性が著しく低下します。テキストボックス幅に応じて、スペース区切りの単語単位で次行へ折り返す処理を標準搭載します。
2. **フォントの切り替え**
   - `determination` (標準のピクセルフォント: Determination Sans / Mono)
   - `comic_sans` (Sans用)
   - `papyrus` (Papyrus用)
3. **インライン演出タグ**
   - `[wait: 秒数]` : 文字送りを一時停止（例: `Wait...[wait: 0.6]What?`）
   - `[shake]`...`[/shake]` : 揺れる文字演出
   - `[color: #hex|name]` : 重要単語等の文字色変更（例: `[color: #ffff00]DETERMINATION[/color]`）
   - `[se: sound_name]` : 特定のタイミングで効果音を再生
   - `[voice: path/to/file.wav]` : 行単位でカスタム音声ファイルを指定

---

## 5. 出力仕様

- **動画形式**: MP4 (H.264 / AAC)
- **解像度**:
  - 16:9 横型: `1920x1080` (YouTube用)
  - 9:16 縦型: `1080x1920` (Shorts / TikTok / Reels用)
- **フレームレート**: 30fps (または 60fps)
