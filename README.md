# CRAFTFLOW 公式サイト

建設・設備業向け業務支援ソフトウェア「CRAFTFLOW」の公式販売サイトです。
HTML / CSS / JavaScript だけで動く静的サイトで、GitHub Pages で無料公開できます。

## ページ構成

| ファイル | 内容 |
|---|---|
| index.html | トップページ |
| products.html | 製品一覧 |
| products/nuriq.html | NURIQ（左官）詳細 |
| products/piping.html | 配管見積もりシステム（仮称）詳細 |
| products/estimate.html | 見積・請求アプリ（仮称）詳細 |
| pricing.html | 料金プラン（未定表示） |
| faq.html | よくある質問 |
| contact.html | お問い合わせ（Google フォーム埋め込み） |
| 404.html | ページが見つからないとき |

## よくある更新作業

### お問い合わせフォームをつなぐ
1. Google フォームで「会社名・屋号／お名前／メールアドレス／希望製品／お問い合わせ内容」の項目を作る
2. `js/config.js` の `formUrl` に埋め込み用 URL（`...viewform?embedded=true`）を、`formOpenUrl` に共有リンクを入れる
3. 空欄の間は「フォーム準備中」と表示され、送信できるようには見えません

### 文言・製品情報・機能の状況を変える
`tools/build.py` の `PRODUCTS` / `COMMON_FAQ` を編集し、`python3 tools/build.py` を実行。
機能の状況は4種類です（`PROTO`＝試作版に搭載、`DEV`＝開発中、`PLAN`＝検討中、`LIVE`＝提供中）。
正式に提供を始めた機能は `LIVE` に変え、製品全体の表示は `PRODUCT_STATUS` を変えます。

### 製品画面（スクリーンショット）
`img/screens/` に、各製品の試作版を実際に動かして撮影した画面（WebP）があります。
- NURIQ の図面は、著作権のある実在の図面を使わず、説明用に作った架空のサンプル図面です
- 配管見積もりシステムはアプリ内の「サンプル工事（練習用）」、見積・請求アプリは架空の会社・顧客で撮影しています
- 画面を差し替えたら `ASSET_VER` を上げて再生成します。画面上の番号（符号）の位置は `HERO_PINS` / `DETAIL_PINS`（%指定）で調整します
- 架空の画面を実際の製品画面として載せないでください

### デザインの決まり
- 色：Deep Navy `#17232E`／Warm White `#F4F2ED`／Bronze `#B58A62`／Slate `#69737A`（`css/site.css` 冒頭の変数）
- 書体：IBM Plex Sans JP（Google Fonts）1種類
- ロゴマーク：さしがね（曲尺）。`tools/build.py` の `MARK` と `img/favicon.svg`

### 公開URLが変わったとき
`tools/build.py` の `SITE_URL` と、`404.html` 生成部分の `/craftflow-website/` を変更して再生成。

## 公開（GitHub Pages）
リポジトリの Settings → Pages → Source を「Deploy from a branch」、Branch を `main` / `/ (root)` にします。
無料プランの GitHub Pages はリポジトリを公開（Public）にする必要があります。サイトに秘密情報や顧客情報は置かないでください。

## 費用
GitHub Pages・Google Fonts・Google フォームはすべて無料。現在の費用は 0 円です。外部のJavaScriptライブラリは使っていません。
