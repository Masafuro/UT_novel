# 07. テンプレートエンジン基盤とR4モード開発計画

## 1. 背景と設計方針 (Background & Core Philosophy)

本プロジェクト「UT_novel」は、Markdown台本からダイアログ動画を自動生成するツールとして完成しました。

これまでの実装では、Undertale風の描画処理や画面アスペクト比（16:9 / 9:16）の計算がエンジン内部に固定・分散していました。しかし、画面サイズやアスペクト比が変われば、フォントサイズ、マージン、立ち絵の配置、UIフレームの比率などの**「最適解」は完全に別物**になります。

そこで、曖昧な自動推測や分散した設定を一切排除し、**「テンプレート（Template）自身が画面解像度（Width, Height）を含めた全レイアウトと演出を自己完結して保持する」** という極めてシンプルな疎結合アーキテクチャに刷新します。

### 核心原則 (Core Principles)
1. **`template` 指定の一本化**:
   - `theme` や `aspect_ratio` といった曖昧なパラメータを廃止・集約し、台本側では **`template: "テンプレート名"`** のみで指定する。
   - 例: `template: "undertale_16_9"`, `template: "undertale_9_16"`, `template: "r4_16_9"`, `template: "r4_9_16"`
2. **デザインの崩れを原理的に防止**:
   - 各テンプレートが「自分自身のキャンバスサイズ（1920x1080 や 1080x1920）」を確定プロパティとして持ち、そのサイズ専用に1px単位で黄金比レイアウトを定義する。
3. **エンジンの純化（Separation of Concerns）**:
   - コアエンジン（`NovelEngine`）は座標やピクセル数を一切知る必要がなく、`TemplateRegistry.get(template_name)` で取得したテンプレートオブジェクトから解像度を受け取ってFFmpegに渡し、各フレームの描画を委譲する。

---

## 2. システム構成と4つの独立テンプレート

```
                    [Markdown 台本 (.md)]
                  └── Frontmatter (template: "r4_16_9")
                              │
                              ▼
                   [TemplateRegistry.get(name)]
                              │
       ┌──────────────┬───────┴───────┬──────────────┐
       ▼              ▼               ▼              ▼
[undertale_16_9] [undertale_9_16]  [r4_16_9]      [r4_9_16]
 (1920x1080)      (1080x1920)     (1920x1080)    (1080x1920)
 - 幅広ピクセル枠  - スマホUI回避枠 - 横スリット型  - 縦型カードHUD
 - 下マージン60px  - 下マージン280px- R4イエロー線 - レーシングUI
 - 56ptフォント   - 46ptフォント   - 42ptモダン字 - 38ptモダン字
```

### テンプレート一覧仕様

| テンプレートID | 画面サイズ (W×H) | レイアウト形式 | フォント | 行頭記号 | 音響 (Blip) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`undertale_16_9`** | 1920 × 1080 | 画面下部中央・幅広白ピクセル枠（下60px） | PixelOperator (56pt) | `* ` | レトロ8-bit Blip |
| **`undertale_9_16`** | 1080 × 1920 | 画面下部・正方形寄りピクセル枠（下280px） | PixelOperator (46pt) | `* ` | レトロ8-bit Blip |
| **`r4_16_9`** | 1920 × 1080 | 忠実なR4 4層構造（外周イエロー額縁 ＋ 白枠ビューポート ＋ 中央黒枠ポートレート ＋ `*Message` タブ付きダークグレー箱） | モダンサンセリフ (42pt) | なし (`*Message`タブ) | サイバークリック音 |
| **`r4_9_16`** | 1080 × 1920 | 忠実なR4 4層構造（スマホ縦型最適化、上下マージン確保、中央黒枠ポートレート ＋ `*Message` タブ） | モダンサンセリフ (38pt) | なし (`*Message`タブ) | サイバークリック音 |

---

## 3. アーキテクチャ設計 (Architecture Design)

### 3.1 ディレクトリ構成

```text
src/ut_novel/
├── templates/                   # ★新規: テンプレート管理パッケージ
│   ├── __init__.py
│   ├── base.py                  # BaseTemplate (抽象基底クラス)
│   ├── registry.py              # TemplateRegistry (テンプレート一覧・登録・検索)
│   ├── undertale_16_9.py        # Undertale 横型テンプレート
│   ├── undertale_9_16.py        # Undertale 縦型Shortsテンプレート
│   ├── r4_16_9.py               # R4 横型テンプレート
│   └── r4_9_16.py               # R4 縦型Shortsテンプレート
├── visual/
│   ├── bg_video.py              # 背景動画ループ再生処理 (共通)
│   └── splash.py                # スプラッシュ画面処理 (共通)
├── parser/
│   └── script_parser.py         # template フィールドのパース
├── engine.py                    # TemplateRegistryと連携するクリーンな実行部
└── cli.py                       # CLI引数 (--template ...)
```

### 3.2 抽象基底クラス (`BaseTemplate`)

テンプレートは「画面サイズ」「音響設定」「フレーム描画ロジック」をすべて内包します。

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from PIL import Image
from ut_novel.parser.rich_text import RichChar

class BaseTemplate(ABC):
    # テンプレート自身が固有の解像度を保持（エンジンがこれを参照）
    screen_width: int
    screen_height: int
    default_blip_sound: str

    @abstractmethod
    def render_frame(
        self,
        base_image: Image.Image,
        visible_rich_chars: List[RichChar],
        speaker_name: Optional[str],
        portrait_image: Optional[Image.Image],
        is_speaking: bool,
        speaking_tick: int,
        frame_index: int,
        show_textbox: bool = True
    ) -> Image.Image:
        """このテンプレートのレイアウト・フォント・装飾に従って1フレームを描画する"""
        pass
```

### 3.3 台本での指定方法（シンプル・一本化）

台本（Markdown）側は、`template` を1つ指定するだけです。
（※未指定の場合はデフォルト `undertale_16_9`）

```markdown
---
title: "Pre-Race Briefing"
template: "r4_16_9"
bg: "assets/bg/garage.mp4"
bgm: "assets/bgm/jazz_loop.wav"

characters:
  commander:
    name: "Robert"
    faces:
      normal: "assets/char/boss/normal.png"
---

* commander(normal): タイヤの熱入れを怠るなよ。[wait: 0.4] お前の走りを信じている。
```

---

## 4. 段階的開発フェーズ (Phase Roadmap)

### Phase 1: テンプレート基盤の設計・実装 (`BaseTemplate` & `TemplateRegistry`)
- `src/ut_novel/templates/base.py` の定義
- `src/ut_novel/templates/registry.py` の実装
- `script_parser.py` に `template` 属性を追加（デフォルト `"undertale_16_9"`）

### Phase 2: Undertale 2系統テンプレートの移植 & 後方互換性テスト
- 既存の `textbox.py` と `DialogBoxConfig` のロジックを以下に分割・移行：
  - `src/ut_novel/templates/undertale_16_9.py`
  - `src/ut_novel/templates/undertale_9_16.py`
- `engine.py` をテンプレート駆動型にリファクタリング。
- **後方互換性検証**:
  - `examples/dialogue_ruins.md`（横型）
  - `examples/shorts_encounter.md`（縦型）
  両方が正しくレンダリングできることを確認。

### Phase 3: R4 2系統テンプレートのアセット準備 & 実装
- **アセット準備**:
  - オープンライセンスの高品質モダンサンセリフ欧文フォントの配置
  - タイトで短いサイバーUIクリック音（Blip用SE）の配置
  - サンプル背景・ポートレートの配置
- **テンプレート実装**:
  - `src/ut_novel/templates/r4_16_9.py`: 横スリット枠、R4イエロー上部ライン、ヘッダーHUD装飾
  - `src/ut_novel/templates/r4_9_16.py`: 縦画面用レーシングモニターカードHUDレイアウト

### Phase 4: 作例作成・総合検証・ドキュメント更新
- `examples/r4_briefing_16_9.md` および `examples/r4_briefing_9_16.md` の作成と動画出力
- 1080p MP4動画の画質・レイアウト・タイポグラフィ・音響の総合確認
- `README.md` の更新（`template` オプションの説明）

---

## 5. 完了基準 (Definition of Done)

- [ ] `template: "undertale_16_9"`, `"undertale_9_16"`, `"r4_16_9"`, `"r4_9_16"` の4つのテンプレートが独立して存在し、台本から完全切り替えできること。
- [ ] 各テンプレートが自身の解像度（Width, Height）を持ち、レイアウト崩れが原理的に発生しないこと。
- [ ] `engine.py` 内部にハードコードされたレイアウト座標・アスペクト比計算が完全に排除されていること。
- [ ] 既存のUndertale作例動画が従来通りのクオリティで出力できること（リグレッションなし）。
- [ ] R4の横型・縦型動画がそれぞれハイクオリティに出力できること。
