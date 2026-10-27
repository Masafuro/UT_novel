# 02. アーキテクチャ & システム設計 (Architecture & Design)

## 1. システム全体概要

本システムは、Markdown台本から構文解析を行い、**「音声生成（TTSまたは文字送りSE）」を先行して確定させた上で、そのタイミングに合わせた映像レンダリング**を行うオーディオ・ドリブン（Audio-driven）なパイプラインを採用します。

```mermaid
flowchart TD
    Script[Markdown 台本 (.md)] --> Parser[1. Parser & Tokenizer]
    Parser --> ScriptModel[台本データモデル]
    
    subgraph AudioPipeline [音声パイプライン (Audio-First)]
        ScriptModel --> AudioRouter{音声モード判定}
        AudioRouter -->|mode: tts| TTSProvider[TTS Engine (Piper / Cloud / Custom)]
        AudioRouter -->|mode: blip| BlipEngine[Voice Blip Engine (文字送りSE)]
        TTSProvider --> AudioMixer[Audio Mixer (BGM / SE合成)]
        BlipEngine --> AudioMixer
        AudioMixer --> AudioTrack[完成音声トラック (combined_audio.wav)]
        AudioMixer --> AudioTimings[文字・セリフ単位のタイムスタンプ情報]
    end
    
    subgraph VisualPipeline [映像パイプライン]
        ScriptModel --> VisualEngine[2. Visual Renderer]
        AudioTimings -.->|タイミング・同期情報| VisualEngine
        Assets[(Assets: Fonts, Face Sprites, BG Video)] --> VisualEngine
        VisualEngine --> FramePipe[映像ストリーム (RGB24 Raw Frames)]
    end
    
    FramePipe --> FFmpeg[3. FFmpeg Encoder]
    AudioTrack --> FFmpeg
    
    FFmpeg --> OutputVideo[出力動画 (output.mp4)]
```

---

## 2. モジュール構成と責務

### (1) `parser` (台本パーサー)
- **Frontmatter Parser**: YAML設定（解像度、キャラクター定義、TTS設定、BGM）を読み込み。
- **Text Preprocessor (Word Wrap)**:
  - 英語の単語（Word）境界を認識し、ダイアログボックスの最大幅に収まるよう自動改行を事前計算。
  - 改行位置とインライン演出タグ（`[wait]`, `[color]`, `[shake]`）の整合性を保持。
- **AST / Timeline Event Model**:
  - セリフ行、ウェイト、演出タグを中間イベント列（データクラス）に変換。

### (2) `audio` (音声エンジン & TTSプロバイダー)
- **TTS Provider 抽象基底クラス (`BaseTTSProvider`)**:
  - `synthesize(text, voice_id, speed) -> AudioSegment, WordTimings`
  - **実装プロバイダー**:
    - `PiperTTSProvider`: 軽量・高品質なオープンソースオフライン英語TTS（初期推奨）
    - `CustomFileProvider`: 既存のWAV/MP3ファイルを直接使用
    - `OpenAITTSProvider` / `ElevenLabsProvider`: 将来的なクラウドAPI拡張
- **Voice Blip Engine**:
  - Undertale本家のピコピコ文字音を生成。
  - スペース無音、句読点でのポーズ時間をミリ秒単位でトラックに配置。
- **Audio Mixer**:
  - BGMのループ処理、音量バランス調整、フェードイン/アウト。
  - 行単位・単語単位の開始時刻・終了時刻（タイムスタンプ）を映像エンジンに提供。

### (3) `visual` (映像レンダラー)
- **同期型タイプライター描画**:
  - **TTSモード**: 音声の再生尺（デュレーション）に合わせて文字表示を等速（または単語同期）で進行。
  - **Blipモード**: 指定されたFPS・タイピング速度（例: 2フレームに1文字）で進行。
- **キャラクター顔グラフィック & リップシンク**:
  - 音声が鳴っている間（またはタイピング進行中）は口パク用スプライト（または上下微振動）をアニメーション再生。発話終了で静止表情に復帰。
- **Undertale UIスタイル**:
  - 黒背景＋白の二重枠線ダイアログボックス。
  - 英語ドットフォント（PixelOperator, Determination等）のレンダリング。
  - `[shake]` (文字の微細なランダム揺れ)、`[color]` (文字色変更) の描画。
- **背景ビデオ・画像合成**:
  - 背景動画（MP4）をループ再生し、その上にダイアログをアルファ合成。

### (4) `encoder` (動画エンコーダー)
- `Pillow` で描画されたフレームバッファを、パイプ（`subprocess`）を通じて `FFmpeg` の標準入力に流し込む。
- 事前に作成された完成音声トラックと合流させ、MP4 (H.264 / AAC) としてディスクへ書き出し。

---

## 3. ディレクトリ構成案

```text
UT_novel/
├── assets/                  # デフォルト素材
│   ├── fonts/               # PixelOperator等のドットフォント
│   ├── se/                  # Undertale風文字送り音（Voice Blips）、決定音等
│   └── tts_models/          # Piper等のローカル英語TTSモデル（必要時）
├── examples/                # サンプル台本・素材
│   ├── english_blip_sample/ # Voice Blip版サンプル
│   └── english_tts_sample/  # TTS連携版サンプル
├── src/
│   └── ut_novel/
│       ├── __init__.py
│       ├── cli.py           # CLIエントリポイント
│       ├── models.py        # タイムライン・台本のデータモデル
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── frontmatter.py
│       │   ├── word_wrap.py # 英語用単語改行処理
│       │   └── script_parser.py
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── mixer.py     # BGM / SE合成
│       │   ├── blip.py      # Undertale風文字送り音エンジン
│       │   └── tts/         # TTSプロバイダー群
│       │       ├── base.py
│       │       ├── piper.py # ローカルTTS
│       │       └── custom.py# ユーザー指定音声
│       ├── visual/
│       │   ├── __init__.py
│       │   ├── textbox.py   # ダイアログ枠描画
│       │   ├── font_renderer.py # ピクセルフォント & タグ描画
│       │   ├── portrait.py  # 顔グラ & 口パクリップシンク
│       │   └── composer.py  # 背景動画とのフレーム合成
│       └── encoder/
│           ├── __init__.py
│           └── ffmpeg_pipe.py # FFmpegパイプ処理
├── tests/                   # 単体テスト
├── memo/
│   └── PLAN/                # 開発計画ドキュメント
├── requirements.txt
├── README.md
└── LICENSE
```
