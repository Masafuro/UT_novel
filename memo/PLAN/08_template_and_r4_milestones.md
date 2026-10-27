# 08. テンプレートエンジン基盤 & R4モード 開発マイルストーン計画

本ドキュメントは、**「画面サイズ・レイアウト・音響を自己完結して保持する4つの独立テンプレート」** を段階的かつ確実に実装・検証するためのマイルストーン計画です。

各マイルストーンごとに明確な**成果物（Deliverable）**、**完了基準（Definition of Done）**、**検証手順**を設けて進行します。

---

## マイルストーン進行フロー

```
[T-M1: テンプレート基盤 & レジストリ構築]
                │
                ▼
[T-M2: Undertale 2系統の移行 & 互換性テスト]  ★ 後方互換性100%維持
                │
                ▼
[T-M3: R4 16:9 横型テンプレート & アセット配備] ★ 新世界観の確立
                │
                ▼
[T-M4: R4 9:16 縦型Shortsテンプレート実装]    ★ スマホ最適化
                │
                ▼
[T-M5: CLI連携・総合検証 & ドキュメント更新]   ★ リリース品質
```

---

## 詳細マイルストーン定義

### Milestone T-M1: テンプレート基盤 & レジストリ構築 (Template Core & Registry)
- **目的**: 
  - `BaseTemplate` 抽象基底クラスと、テンプレートを名前で管理・取得する `TemplateRegistry` を作成する。
  - 台本パーサー（`script_parser.py`）に `template` フィールドを追加し、指定されたテンプレート名を取り出せるようにする。
- **成果物**:
  - `src/ut_novel/templates/base.py`
  - `src/ut_novel/templates/registry.py`
  - `src/ut_novel/parser/script_parser.py` (更新)
- **完了基準 (DoD)**:
  - [x] `BaseTemplate` が `screen_width`, `screen_height`, `default_blip_sound`, `render_frame(...)` を必須インターフェースとして規定していること。
  - [x] `TemplateRegistry.register()` および `TemplateRegistry.get(name)` が正常に機能すること。
  - [x] 台本Frontmatterの `template: "..."` が正しくパースされ、未指定の場合はデフォルト `undertale_16_9` が設定されること。
- **検証手順**:
  - 単体スクリプトを実行し、ダミーテンプレートの登録・取得および台本パース結果をコンソールで確認。

---

### Milestone T-M2: Undertale 2系統の移行 & 後方互換性テスト (Undertale 16:9 / 9:16 Migration)
- **目的**:
  - 既存の `visual/textbox.py` と `DialogBoxConfig` の描画処理を、基底クラスに準拠した2つの独立テンプレート（`undertale_16_9`, `undertale_9_16`）に移行する。
  - `NovelEngine` からアスペクト比の条件分岐や座標計算を排除し、テンプレートから画面サイズと描画ロジックを取得する構造に純化する。
- **成果物**:
  - `src/ut_novel/templates/undertale_16_9.py` (1920x1080 専用設計)
  - `src/ut_novel/templates/undertale_9_16.py` (1080x1920 専用設計)
  - `src/ut_novel/engine.py` (テンプレート駆動型へのリファクタリング)
- **完了基準 (DoD)**:
  - [x] `engine.py` 内部にハードコードされた座標・マージン・アスペクト比計算が完全に撤廃されていること。
  - [x] 既存の作例（`examples/dialogue_ruins.md`, `examples/shorts_encounter.md`）が、台本を書き換えることなく従来と寸分違わぬクオリティで動画出力できること（**リグレッションゼロ**）。
- **検証手順**:
  - 既存の横型・縦型台本をレンダリングし、生成されたMP4動画の解像度・文字送り・口パク・演出タグを目視検証。

---

### Milestone T-M3: R4 16:9 横型テンプレート & アセット配備 (R4 16:9 Template & Assets)
- **目的**:
  - R4の世界観を表現するための高品質モダンサンセリフ欧文フォントとタイトなサイバーUIクリック音を配置する。
  - 1920x1080専用の横スリット型フレーム、上部R4イエローライン、ヘッダーHUD装飾、`>> ` プレフィックスを持つ `r4_16_9` テンプレートを実装する。
- **成果物**:
  - `assets/fonts/` (モダンサンセリフフォント配備)
  - `assets/se/` (R4用タイトUIクリック音配備)
  - `src/ut_novel/templates/r4_16_9.py`
  - `examples/r4_briefing_16_9.md`
  - `output/r4_briefing_16_9.mp4`
- **完了基準 (DoD)**:
  - [x] 1920x1080解像度で、横スリット型ダーク半透明フレーム、上部R4イエローライン、ヘッダーHUD（ステージ名・チーム名等）、`>> ` プレフィックスが美しく描画されること。
  - [x] 文字送り音がタイトなクリック音として同期して再生されること。
  - [x] `examples/r4_briefing_16_9.md` から動画が正常生成され、クールなアーバン・レーシング世界観が再現されていること。
- **検証手順**:
  - `python3 -m ut_novel.cli render --script examples/r4_briefing_16_9.md -o output/r4_briefing_16_9.mp4` を実行し、動画の画質・タイポグラフィ・音響バランスを確認。

---

### Milestone T-M4: R4 9:16 縦型Shortsテンプレート実装 (R4 9:16 Template)
- **目的**:
  - 1080x1920（スマホ縦型）専用にレイアウトされたレーシングモニター風カードHUDを持つ `r4_9_16` テンプレートを実装する。
  - スマホUI（TikTok/Shorts等の上下UI）と干渉しない最適な中央〜下部配置を実現する。
- **成果物**:
  - `src/ut_novel/templates/r4_9_16.py`
  - `examples/r4_briefing_9_16.md`
  - `output/r4_briefing_9_16.mp4`
- **完了基準 (DoD)**:
  - [x] 1080x1920解像度で、レーシングモニター風カードHUDがバランス良く描画されること。
  - [x] ショート動画として視線誘導がスムーズで、テキストの可読性が高いこと。
- **検証手順**:
  - `python3 -m ut_novel.cli render --script examples/r4_briefing_9_16.md -o output/r4_briefing_9_16.mp4` を実行し、スマホ実寸大表示でバランスを目視確認。

---

### Milestone T-M5: CLI連携・総合検証 & ドキュメント更新 (Integration & Docs)
- **目的**:
  - CLIオプション `--template` を追加し、台本側で指定されたテンプレートをコマンドラインから自由に上書きできるようにする。
  - 4つのテンプレートすべての作例・ドキュメントを整理し、ユーザーが迷わず使える状態にする。
- **成果物**:
  - `src/ut_novel/cli.py` (更新: `--template` オプション対応)
  - `README.md` (更新: テンプレート一覧、指定方法、R4作例の紹介)
- **完了基準 (DoD)**:
  - [x] `python3 -m ut_novel.cli render --script ... --template r4_16_9` で上書き実行できること。
  - [x] 全4テンプレート（`undertale_16_9`, `undertale_9_16`, `r4_16_9`, `r4_9_16`）の作例動画がすべて正常に出力できること。
  - [x] README.mdに新しいテンプレート体系が分かりやすく整理されていること。
- **検証手順**:
  - CLIからの上書きテスト、全作例の再レンダリング実行、READMEの記載内容チェック。

