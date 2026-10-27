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
   - **開発マイルストーン計画 (M1 〜 M6)**
   - 各マイルストーンごとの作業内容、成果物、完了基準（Definition of Done）

5. **[05_external_tts_brainstorming.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/05_external_tts_brainstorming.md)**
   - **外部TTS（Qwen3 TTS等）連携構想 & ブレスト**
   - 分離アーキテクチャ（GPUマシンでの音声生成とUT_novelの結合）、ファイルインポート/API連携、単語アライメント同期の構想検討

6. **[06_copyright_character_migration_plan.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/06_copyright_character_migration_plan.md)**
   - **著作権準拠キャラクター素材移行計画**
   - 既存のUndertale素材（sans, toriel）の完全排除、オリジナル1-bitキャラクター（dev_boy_1, dev_girl_1）への統一、台本・ドキュメント・作例コードの刷新ステップ

7. **[07_theme_engine_and_r4_mode_plan.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/07_theme_engine_and_r4_mode_plan.md)**
   - **テンプレートエンジン基盤 & R4モード開発計画**
   - 台本とテンプレートの完全分離、自己完結型4テンプレート（undertale/r4 × 16:9/9:16）、疎結合アーキテクチャの基本設計

8. **[08_template_and_r4_milestones.md](file:///home/ubuntu/AgentWorkspace/UT_novel/memo/PLAN/08_template_and_r4_milestones.md)**
   - **テンプレートエンジン基盤 & R4モード 開発マイルストーン計画 (T-M1 〜 T-M5)**
   - テンプレート基盤構築からUndertale移行、R4横型・縦型実装、CLI連携・検証までの詳細DoDと検証手順

