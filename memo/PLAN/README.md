# UT_novel 開発計画 (PLAN)

Undertaleスタイルの対話（ダイアログ）と背景動画を、**Markdown形式の台本ファイルから自動生成するCLI動画ジェネレーター**の開発計画です。

---

## 計画ドキュメント構成

1. **[01_concept_and_spec.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/01_concept_and_spec.md)**
   - プロダクトの基本コンセプト、目的、ターゲット
   - 英語ベースのテキスト処理仕様（Word Wrapping、句読点ポーズ、ピクセルフォント）
   - デュアル音声システム（Voice Blip文字送り音 / TTS音声合成同期）
   - Markdown台本フォーマット仕様（Frontmatter、セリフ記法、演出タグ）

2. **[02_architecture.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/02_architecture.md)**
   - 音声主導（Audio-driven）のシステムアーキテクチャ
   - TTS Provider抽象化構造（Piper TTS / Custom Audio / Cloud）
   - 技術選定（Python + Pillow + PyDub + FFmpeg）
   - ディレクトリ構成案

3. **[03_roadmap.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/03_roadmap.md)**
   - 全体ロードマップ（Phase 1 〜 Phase 4）
   - フェーズ別の機能要件とタスク詳細

4. **[04_milestones.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/04_milestones.md)**
   - **具体的な開発マイルストーン計画 (M1 〜 M6)**
   - 各マイルストーンごとの作業内容、成果物、完了基準（Definition of Done）
