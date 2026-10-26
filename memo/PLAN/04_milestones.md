# 04. 開発マイルストーン計画 (Milestone Plan)

本プロジェクトを確実に前進させるため、検証可能な成果物（Deliverable）を定義した **6つのマイルストーン** に分割して進行します。各マイルストーンには明確な「完了定義（Definition of Done）」と「検証手順」を設けています。

---

## マイルストーン一覧

```
[M1: プロジェクト基盤 & 静的描画]
        │
        ▼
[M2: タイピング & Voice Blip 動画 (MVP)]  ★ 最初の動く動画
        │
        ▼
[M3: 英語Word Wrap & 複数セリフ進行]
        │
        ▼
[M4: TTS連携 & 音声同期リップシンク]      ★ AIボイス対応
        │
        ▼
[M5: 背景動画合成 & インライン演出タグ]   ★ リッチ映像化
        │
        ▼
[M6: 縦型/横型最適化 & BGM & CLI完成]   ★ リリース品質
```

---

## 詳細マイルストーン定義

### Milestone 1 (M1): プロジェクト基盤 & 静的ダイアログ描画 【完了】
- **目的**: 開発環境、依存パッケージ、基本アセット（フォント・SE）を揃え、Undertale風ダイアログ枠の1コマ静止画を正しくレンダリングできる状態にする。
- **成果物**: `src/ut_novel/visual/textbox.py`, `output/m1_test_portrait.png`
- **完了基準 (DoD)**:
  - [x] コマンドを実行すると、Undertale風テキストボックスにアスタリスクと指定テキストが描画されたテスト画像（`test_frame.png`）が出力されること。

---

### Milestone 2 (M2): タイピング動画 & Voice Blip 音声合成（MVP達成）【完了】
- **目的**: 英語のセリフ1行を、文字送りアニメーション（タイプライター効果）と英語Voice Blip（ピコピコ音）を伴ってMP4動画として書き出せる最小限の動画生成パイプラインを確立する。
- **成果物**: `src/ut_novel/timeline.py`, `src/ut_novel/audio/blip.py`, `output/m2_test.mp4`
- **完了基準 (DoD)**:
  - [x] 1行の英語セリフ（例: `* Hello, my child.`）から、文字送り音付きのタイピング動画（`output_m2.mp4`）が生成・正常再生できること。

---

### Milestone 3 (M3): 英語Word Wrapping & 複数セリフシーケンス 【完了】
- **目的**: 実用的な台本を扱えるようにし、長文英語の自然な改行と、複数セリフの連続再生（セリフ完了後の読み待ち時間含む）を実現する。
- **成果物**: `src/ut_novel/parser/`, `src/ut_novel/engine.py`, `src/ut_novel/cli.py`, `output/m3_sequence.mp4`
- **完了基準 (DoD)**:
  - [x] 3〜4行の会話が記述されたMarkdownファイルから、単語の途切れなく複数セリフが順次進行する動画が生成できること。

---

### Milestone 4 (M4): TTS連携 & 音声主導リップシンク 【完了】
- **目的**: 英語AI音声合成（TTS）を組み込み、音声尺に合わせてタイピング速度とキャラクター口パクが自動同期するオーディオ・ドリブン機構を実装する。
- **成果物**: `src/ut_novel/audio/tts/`, `src/ut_novel/timeline.py` (AudioDrivenTimeline), `output/m4_tts_lipsync.mp4`
- **完了基準 (DoD)**:
  - [x] 台本で `voice_mode: tts` を指定したキャラクターが、英語AI音声に合わせて口パクしながらタイピングされる動画が生成できること。

---

### Milestone 5 (M5): 背景動画合成 & インライン演出タグ 【完了】
- **目的**: 静止画だけでなく背景ループ動画を合成し、Undertale特有の感情豊かな演出タグを処理できるようにする。
- **成果物**: `src/ut_novel/visual/bg_video.py`, `src/ut_novel/parser/rich_text.py`, `output/m5_rich_effects.mp4`
- **完了基準 (DoD)**:
  - [x] 動く背景の上で、文字揺れや色変更、ウェイトが効いたリッチな演出動画が生成できること。

---

### Milestone 6 (M6): 縦型/横型最適化 & BGMミキシング & CLI完成 【完了】
- **目的**: YouTube Shorts（9:16）と通常動画（16:9）の両方に対応し、BGMループ処理と使いやすいCLIツールとして完成させる。
- **成果物**: `src/ut_novel/models.py` (Preset), `src/ut_novel/audio/mixer.py`, `src/ut_novel/cli.py`, `README.md`, `output/m6_shorts_vertical.mp4`
- **完了基準 (DoD)**:
  - [x] 付属のサンプル台本から `ut-novel` コマンド一発で縦型/横型の完成動画が書き出せ、一般ユーザーが使える状態になっていること。
