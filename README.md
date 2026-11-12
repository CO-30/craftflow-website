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
機能が完成したら、`DEV` を `'<span class="status status-ok">提供中</span>'` に変えます。

### 画面スクリーンショットを載せる
実際のアプリ画面を `img/` に置き、`tools/build.py` の「画面イメージは準備中です」の箇所を `<img>` に差し替えます。
架空の画面を実際の製品画面として載せないでください。

### 公開URLが変わったとき
`tools/build.py` の `SITE_URL` と、`404.html` 生成部分の `/craftflow-website/` を変更して再生成。

## 公開（GitHub Pages）
リポジトリの Settings → Pages → Source を「Deploy from a branch」、Branch を `main` / `/ (root)` にします。
無料プランの GitHub Pages はリポジトリを公開（Public）にする必要があります。サイトに秘密情報や顧客情報は置かないでください。

## 費用
GitHub Pages・Google Fonts・Google フォームはすべて無料。現在の費用は 0 円です。
