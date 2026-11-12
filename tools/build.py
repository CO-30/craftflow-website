#!/usr/bin/env python3
"""CRAFTFLOW サイト生成スクリプト

ヘッダー・フッター・メタ情報・製品情報を全ページで揃えるために使います。
文言や機能の状況を直したいときはこのファイルを編集して

    python3 tools/build.py

を実行すると、ルートにある各 HTML と sitemap.xml / robots.txt が書き換わります。
（Python 3 だけで動きます。追加インストールは不要です）
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://co-30.github.io/craftflow-website/"  # 公開URLが変わったらここを変更
BASE_PATH = "/craftflow-website/"  # 404ページ用（公開URLのパス部分）
UPDATED = "2026-11-12"
ASSET_VER = "3"  # CSS/JS/画像を変えたら数字を上げる（キャッシュ対策）

NAV = [
    ("products.html", "製品"),
    ("pricing.html", "料金"),
    ("faq.html", "よくある質問"),
]

# ---------------------------------------------------------------- 機能の状況
# 試作版で動作を確認できたもの＝PROTO、開発を進めているもの＝DEV、検討段階＝PLAN
# 正式に提供を始めたら LIVE に切り替える
PROTO = ("proto", "試作版に搭載")
DEV = ("dev", "開発中")
PLAN = ("plan", "検討中")
LIVE = ("live", "提供中")

PRODUCT_STATUS = "開発中・試作版あり"


def status(s):
    return f'<span class="status status-{s[0]}">{s[1]}</span>'


# ---------------------------------------------------------------- 図形
# ブランドマーク：さしがね（曲尺）。職人の基準を測る道具。
MARK = '''<svg class="mark" viewBox="0 0 28 28" aria-hidden="true"><path d="M4 3h5v16h16v5H4z" fill="currentColor"/><path d="M9 7h2.5M9 11h3.5M9 15h2.5M13 19v-2.5M17 19v-3.5M21 19v-2.5" stroke="#17232E" stroke-width="1.2"/></svg>'''


def img(src, alt, w, h, cls="", lazy=True, sizes=None):
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{src}?v={ASSET_VER}" alt="{escape(alt)}" width="{w}" height="{h}"{load}>'


def annotated(r, shot, markers, alt, w=1600, h=1000, lazy=True, small=None):
    """製品画面に符号（番号）を打つ。markers = [(x%, y%, 説明), ...]"""
    pins = "".join(
        f'<span class="pin" style="left:{x}%;top:{y}%" aria-hidden="true">{i}</span>'
        for i, (x, y, _t) in enumerate(markers, 1)
    )
    legend = "".join(f'<li><span class="pin-n" aria-hidden="true">{i}</span>{escape(t)}</li>' for i, (_x, _y, t) in enumerate(markers, 1))
    return f'''<figure class="annotated">
  <div class="screen">{img(r + "img/screens/" + shot + ".webp", alt, w, h, lazy=lazy)}{pins}</div>
  <ol class="legend">{legend}</ol>
</figure>'''


def phone(r, shot, alt, cap=None):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="phone"><div class="phone-frame">{img(r + "img/screens/" + shot + ".webp", alt, 600, 1298)}</div>{c}</figure>'


def screen(r, shot, alt, cap=None, w=1600, h=1000):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="shot"><div class="screen">{img(r + "img/screens/" + shot + ".webp", alt, w, h)}</div>{c}</figure>'


# ---------------------------------------------------------------- 製品
PRODUCTS = [
    {
        "slug": "nuriq",
        "name": "NURIQ",
        "kana": "ヌリック",
        "trade": "左官",
        "category": "左官工事の数量拾い・見積もり",
        "catch": "図面のPDFから、左官の数量を拾う。",
        "lead": "仕上表から左官の工事だけを抜き出し、平面図の上で面積や長さを測って、見積書まで作るソフトです。",
        "short": "仕上表から左官の項目を抜き出し、図面上で面積を測って見積書まで。",
        "for": ["左官業者・左官職人", "建設会社の積算・見積もり担当", "左官工事を含む見積もりを作る方"],
        "problems": [
            ("拾い出しに半日かかる", "壁・床・天井ごとに、図面と電卓を何度も往復して面積を出している。"),
            ("どの工事が左官の範囲か、毎回仕上表を読む", "タイルや塗装と混ざった仕上表から、自社が請ける工事を探し出している。"),
            ("数字の根拠を説明しにくい", "どの図面のどこを測ったのか、あとから確かめられない。"),
        ],
        "features": [
            ("図面PDFの読み込みと、図面の種類・縮尺の自動判定", PROTO),
            ("仕上表から左官工事の項目を抜き出す（タイル・塗装などは除外）", PROTO),
            ("線で囲まれた範囲をクリックして面積を測る（範囲検出）", PROTO),
            ("面積・長さ・壁（周長×高さ）・箇所の計測と控除", PROTO),
            ("拾った範囲を建物の3Dで確認", PROTO),
            ("単価を入れて見積書を作成し、Excel・印刷で出力", PROTO),
            ("スキャンした図面（画像だけのPDF）の自動読み取り", PLAN),
            ("複数の会社で使うための設定・ライセンス管理", DEV),
        ],
        "notes": [
            "図面はお使いのパソコンのブラウザの中で処理し、外部に送信しない作りです。",
            "自動で入った数量には「要確認」と表示され、確定は担当者が行います。",
        ],
        "flow": [
            ("図面のPDFを開く", "全ページの種類（仕上表・平面図・立面図など）と縮尺を自動で判定します。"),
            ("拾う項目が並ぶ", "仕上表から左官の工事だけが、場所と部位ごとに一覧になります。"),
            ("図面の上で測る", "項目を選ぶと該当する図面が開き、範囲をクリックして面積を測ります。"),
            ("見積書にする", "会社ごとの単価を入れて見積書を作り、Excelや印刷で出力します。"),
        ],
        "gallery": [
            ("nuriq-items-crop", "仕上表のページと、抜き出された左官工事の拾い項目", "仕上表を読み取り、左官の工事だけを場所・部位ごとに並べた状態。", 1200, 552),
            ("nuriq-3d-crop", "平面図を3Dにして、拾った範囲を色分けした画面", "拾った範囲と、まだ測っていない項目の位置を3Dで確認。", 1200, 795),
        ],
        "kw": "左官 見積もり ソフト,左官 数量拾い,左官工事 積算,仕上表 拾い出し",
        "faq": [
            ("どんな図面に対応しますか？", "試作版はPDFの図面に対応しています。CADから書き出したPDFなら、文字や線を読み取って図面の種類・縮尺・仕上表を判定します。スキャンした画像だけのPDFは、計測と見積もりはできますが、自動の読み取りには対応していません。"),
            ("全部自動で拾ってくれますか？", "いいえ。自動で数量を入れられるのは、図面に面積表がある場所や、線で囲まれた範囲がはっきりしている場所などに限られます。自動で入れた数量には「要確認」と表示し、最終的な判断は担当者が行う設計です。"),
            ("いつから使えますか？", "提供開始時期は未定です。先行利用（試用）をご希望の方は、お問い合わせからお知らせください。"),
        ],
    },
    {
        "slug": "piping",
        "name": "配管見積もりシステム",
        "kana": "仮称",
        "trade": "配管・水道設備",
        "category": "配管ルート作成・材料拾い・見積もり",
        "catch": "配管を描けば、継手まで数えてくれる。",
        "lead": "建物の間取りに配管ルートを描くと、管の長さ・継手・支持金具を集計し、見積もりと申請用の図面につなげるソフトです。新築・修理・リフォームの配管工事を想定しています。",
        "short": "間取りに配管を描くと、長さ・継手・支持金具を集計。3Dと申請図面にも。",
        "for": ["水道設備業者", "配管工事業者", "設備工事の個人事業主・小規模会社"],
        "problems": [
            ("管の長さと継手を目で数えている", "図面に定規を当てて区間ごとに測り、エルボやチーズの数を数えている。"),
            ("お客様に工事の中身が伝わりにくい", "どこをどう通すのか、平面図と言葉だけでは説明しづらい。"),
            ("申請用の図面を毎回描き直している", "排水の縦断図や給水の立面図を、工事のたびに一から作っている。"),
        ],
        "features": [
            ("間取りと配管ルートを2Dで作成し、3Dで同時に表示", PROTO),
            ("管の長さ・継手・支持金具の自動集計", PROTO),
            ("現場で測った長さ（実測長）を反映", PROTO),
            ("単価を入れて見積もりを作成し、PDF・Excelで出力", PROTO),
            ("配管データから排水縦断図・給水立面図を作図", PROTO),
            ("スマートフォン・タブレットでの表示", PROTO),
            ("自治体ごとの申請様式への対応", DEV),
        ],
        "notes": [
            "申請用の図面は、提出先の自治体の様式に合っているかを確認してからお使いください。",
        ],
        "flow": [
            ("間取りを作る", "建物の外周をなぞると外壁になります。図面の写真やPDFを下に敷いて描くこともできます。"),
            ("器具を置く", "メーター・トイレ・キッチンなどをタップして配置します。"),
            ("配管をつなぐ", "器具の接続口から指でなぞって配管します。2Dと3Dの両方で確認できます。"),
            ("集計して見積もる", "長さ・継手・支持金具が集計され、単価を入れて見積書にします。"),
        ],
        "gallery": [
            ("piping-parts", "継手や支持金具を自動で集計した部品の一覧", "配管のつながりから、継手・支持金具の数を自動で集計。"),
            ("piping-shinsei", "配管データから作図した排水設備の縦断図", "配管データから作図した排水設備の縦断図。"),
        ],
        "phone": ("piping-mobile", "スマートフォンで表示した配管の作図画面"),
        "kw": "配管 見積もり ソフト,配管材料 拾い出し,水道工事 見積もり,配管 3D",
        "faq": [
            ("修理やリフォームにも使えますか？", "新築・修理・リフォームのいずれにも使えるよう開発しています。具体的な対応範囲は提供開始時にご案内します。"),
            ("作図した申請図面をそのまま提出できますか？", "試作版では、配管データから排水縦断図・給水立面図などを作図できます。提出先の自治体ごとに様式や記載事項が異なるため、そのまま提出できるかは様式との確認が必要です。対応方法は提供開始時にご案内します。"),
            ("製品名は決まっていますか？", "現在は仮称です。正式名称は決まり次第このページでお知らせします。"),
        ],
    },
    {
        "slug": "estimate",
        "name": "見積・請求アプリ",
        "kana": "仮称",
        "trade": "見積・請求",
        "category": "見積書・請求書・領収書の作成と管理",
        "catch": "見積書を、現場でスマホから送る。",
        "lead": "スマートフォンで見積書・請求書・領収書を作り、PDFにしてLINEやメールで送れるアプリです。見積書から請求書、請求書から領収書へ、入力し直さずに切り替えられます。",
        "short": "スマホで見積書・請求書・領収書を作り、PDFで送る。入金と売上もまとめて管理。",
        "for": ["個人事業主・一人親方", "建設業・設備業の小規模事業者", "事務担当を置いていない事業者"],
        "problems": [
            ("書類づくりが夜の仕事になる", "現場が終わってから事務所に戻り、見積書や請求書を作っている。"),
            ("同じ内容を何度も打ち直している", "見積書と同じ品目を、請求書や領収書にもう一度入力している。"),
            ("入金されたか、すぐに分からない", "どの請求がまだ未入金なのか、紙やファイルを探して確かめている。"),
        ],
        "features": [
            ("見積書・請求書・領収書の作成", PROTO),
            ("見積書→請求書→領収書への切り替え（入力し直し不要）", PROTO),
            ("PDFの作成と、LINE・メール用の送付文", PROTO),
            ("書類の一覧・検索と、入金状況の管理", PROTO),
            ("年間・月別の売上集計", PROTO),
            ("税抜・税込（内税）の入力切り替え", PROTO),
            ("データは端末内に保存し、バックアップを書き出し", PROTO),
            ("インボイス制度に沿った記載内容の確認", PLAN),
        ],
        "notes": [
            "Googleスプレッドシートとの同期は、使う方が任意で設定する仕組みです。",
        ],
        "flow": [
            ("現場で見積書を作る", "よく使う品目は定型から呼び出し、金額と消費税は自動で計算します。"),
            ("PDFで送る", "作った書類をPDFにして、LINEやメールの送付文と一緒に送ります。"),
            ("請求書に切り替える", "工事が終わったら、見積書の内容から請求書を作ります。"),
            ("入金を記録する", "入金を記録すると領収書を作れます。未入金の請求は一覧で分かります。"),
        ],
        "gallery": [],
        "phones": [
            ("estimate-items", "見積書の明細を入力している画面", "明細を入力すると、金額と消費税をその場で計算。"),
            ("estimate-preview", "作成した見積書のプレビュー画面", "書類の見た目を確かめて、PDFにして送る。"),
            ("estimate-list", "見積・請求・領収の書類一覧と入金状況", "見積・請求・領収と、入金の状況をまとめて確認。"),
        ],
        "kw": "建設業 見積書 アプリ,個人事業主 請求書 アプリ,一人親方 見積書,領収書 アプリ スマホ",
        "faq": [
            ("インボイス制度に対応していますか？", "試作版には登録番号を入力する欄がありますが、制度に沿った記載内容の確認はこれからです。対応内容は提供開始時にご案内します。"),
            ("パソコンでも使えますか？", "ブラウザで動くアプリのため、パソコンでも開けます。画面はスマートフォンでの操作を中心に作っています。"),
            ("作った書類はどこに保存されますか？", "試作版では、使っている端末のブラウザの中に保存されます。設定画面からバックアップ用のファイルを書き出せます。"),
        ],
    },
]
P = {p["slug"]: p for p in PRODUCTS}

COMMON_FAQ = [
    ("個人事業主でも利用できますか？", "はい。CRAFTFLOW の製品は、個人事業主・一人親方・小規模事業者の方に使っていただくことを前提に開発しています。"),
    ("スマートフォンでも使えますか？", "見積・請求アプリはスマートフォンでの利用を中心に作っています。NURIQと配管見積もりシステムは、パソコン・タブレットでの作業を中心に、スマートフォンでも表示できる試作版があります。正式な対応環境は提供開始時にご案内します。"),
    ("Windows・Macに対応していますか？", "試作版はいずれもWebブラウザ（Google Chromeなど）で動く形で開発しているため、Windows・Macのどちらでも使える見込みです。正式な動作環境は提供開始時にご案内します。"),
    ("無料体験はできますか？", "試作版を使った体験（試用）を検討しています。条件や開始時期が決まり次第お知らせします。ご希望の方はお問い合わせください。"),
    ("月額料金はいくらですか？", "料金はまだ決まっていません。料金・提供開始時期についてはお問い合わせください。"),
    ("解約はできますか？", "契約・解約の条件は、販売開始前に利用規約で定めて公開します。"),
    ("データの保存方法は？", "試作版では、図面や書類のデータをお使いの端末のブラウザ内に保存し、CRAFTFLOWのサーバーには送らない作りです（見積・請求アプリは、Googleスプレッドシートとの同期を任意で設定できます）。正式な保存方法は提供開始時にご案内します。なお、このウェブサイト自体にはお客様の情報を保存していません。"),
    ("サポートはありますか？", "お問い合わせからのご質問に対応します。提供開始後のサポート内容は製品ごとにご案内します。"),
]


def pname(p, small=True):
    """製品名（仮称表記つき）"""
    name = escape(p["name"])
    if p["kana"] == "仮称":
        return f'{name}<span class="kari">（仮称）</span>'
    return name


def plain_name(p):
    return p["name"] + ("（仮称）" if p["kana"] == "仮称" else "")


# ---------------------------------------------------------------- 共通レイアウト
def page(path, title, description, body, current=None, keywords="", body_class=""):
    depth = path.count("/")
    r = "../" * depth
    url = SITE_URL + ("" if path == "index.html" else path)
    nav_items = "".join(
        f'<li><a href="{r}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a></li>'
        for href, label in NAV
    )
    kw = f'\n<meta name="keywords" content="{escape(keywords)}">' if keywords else ""
    full_title = title if path == "index.html" else f"{title}｜CRAFTFLOW"
    bc = f' class="{body_class}"' if body_class else ""
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(description)}">{kw}
<link rel="canonical" href="{url}">
<meta property="og:type" content="{"website" if path == "index.html" else "article"}">
<meta property="og:site_name" content="CRAFTFLOW">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}img/ogp.png">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#17232E">
<link rel="icon" href="{r}img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+JP:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{r}css/site.css?v={ASSET_VER}">
</head>
<body{bc}>
<a class="skip" href="#main">本文へ移動</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r}index.html" aria-label="CRAFTFLOW トップページ">{MARK}<span>CRAFTFLOW</span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">メニュー</button>
    <nav id="site-nav" class="site-nav" aria-label="メインメニュー">
      <ul>{nav_items}<li class="nav-cta"><a href="{r}contact.html">お問い合わせ</a></li></ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="{r}index.html">{MARK}<span>CRAFTFLOW</span></a>
        <p lang="en" class="motto">Tools for the people who build.</p>
        <p>建設・設備業の小さな事業者のための業務ソフト。</p>
      </div>
      <nav class="footer-nav" aria-label="フッターメニュー">
        <div><h2>製品</h2><ul>
          <li><a href="{r}products/nuriq.html">NURIQ（左官）</a></li>
          <li><a href="{r}products/piping.html">配管見積もりシステム（仮称）</a></li>
          <li><a href="{r}products/estimate.html">見積・請求アプリ（仮称）</a></li>
        </ul></div>
        <div><h2>ご案内</h2><ul>
          <li><a href="{r}products.html">製品一覧</a></li>
          <li><a href="{r}pricing.html">料金</a></li>
          <li><a href="{r}faq.html">よくある質問</a></li>
          <li><a href="{r}contact.html">お問い合わせ・先行利用</a></li>
        </ul></div>
      </nav>
    </div>
    <p class="copyright">&copy; 2026 CRAFTFLOW　掲載している製品画面は開発中の試作版です。</p>
  </div>
</footer>
<script src="{r}js/config.js?v={ASSET_VER}"></script>
<script src="{r}js/site.js?v={ASSET_VER}"></script>
</body>
</html>
'''


def faq_html(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{escape(q)}</summary><div class="answer"><p>{escape(a)}</p></div></details>'
        for q, a in items
    ) + "</div>"


def contact_block(r, title, text, product="", dark=False):
    q = f"?product={escape(product)}" if product else ""
    cls = "contact-block is-dark" if dark else "contact-block"
    return f'''<section class="{cls}"><div class="wrap">
  <div class="contact-inner">
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="actions"><a class="btn btn-bronze" href="{r}contact.html{q}">先行利用・体験を相談する</a><a class="link" href="{r}faq.html">よくある質問を見る</a></div>
  </div>
</div></section>'''


def feature_list(p):
    return '<ul class="feature-list">' + "".join(
        f"<li><span>{escape(a)}</span>{status(s)}</li>" for a, s in p["features"]
    ) + "</ul>"


def flow_list(p):
    return '<ol class="flow">' + "".join(
        f"<li><h3>{escape(a)}</h3><p>{escape(b)}</p></li>" for a, b in p["flow"]
    ) + "</ol>"


# ---------------------------------------------------------------- トップ
HERO_PINS = [
    (0.8, 54.4, "仕上表から、左官の工事だけを拾い項目に"),
    (59.2, 8.3, "図面の縮尺を、寸法と照合して判定"),
    (48.2, 63.0, "線で囲まれた範囲をクリックして面積を測る"),
]


def index():
    r = ""
    n, pp, e = P["nuriq"], P["piping"], P["estimate"]
    pains = [
        (n, "左官", ["仕上表からどれが左官の工事かを探し、図面と電卓で面積を出している。", "拾った数字を見積書に打ち直している。"]),
        (pp, "配管・水道設備", ["管の長さを定規で測り、エルボやチーズの数を目で数えている。", "申請用の縦断図や立面図を毎回描いている。"]),
        (e, "見積・請求", ["現場が終わってから、事務所で見積書や請求書を作っている。", "未入金の請求がどれか、すぐに分からない。"]),
    ]
    pain_html = "".join(
        f'''<div class="pain">
  <h3>{t}</h3>
  <ul>{"".join(f"<li>{escape(x)}</li>" for x in xs)}</ul>
  <a class="link" href="products/{p["slug"]}.html">{escape(p["name"])}{"（仮称）" if p["kana"] == "仮称" else ""}で解決する</a>
</div>''' for p, t, xs in pains)

    nuriq_points = "".join(f"<li>{escape(a)}</li>" for a, _s in n["features"][:6] if _s == PROTO)
    pipe_points = "".join(f"<li>{escape(a)}</li>" for a, _s in pp["features"][:5])
    est_phones = "".join(phone(r, s, alt, escape(cap)) for s, alt, cap in e["phones"])

    principles = [
        ("職種ごとに、道具を分ける", "左官は仕上表と面積、配管は継手と勾配、事務は書類の切り替え。仕事ごとに必要な画面はまったく違うため、1つの大きなシステムにまとめず、職種ごとに作っています。"),
        ("判断は、現場の人に残す", "自動で入れた数量には「要確認」と表示し、確定は人が行います。どこまでを自社の工事として請けるかなど、会社ごとに違う決まりも使う人が選べるようにしています。"),
        ("図面と書類を、外に出さない", "試作版は、図面や書類をお使いの端末のブラウザの中で処理します。お客様からお預かりした図面を、クラウドに送る必要がありません。"),
        ("使うたびに費用がかかる仕組みにしない", "試作版は、使うたびに料金が発生する外部サービスを使わずに動きます。小さな事業者が続けやすい料金にするための選択です。"),
    ]
    prin_html = "".join(f"<div class=\"principle\"><h3>{a}</h3><p>{b}</p></div>" for a, b in principles)

    stage_rows = "".join(
        f'''<tr><th scope="row"><a href="products/{p["slug"]}.html">{pname(p)}</a></th>
<td data-label="試作版"><span class="stage stage-done">動作確認済み</span></td>
<td data-label="現場での試用"><span class="stage stage-now">試用の希望を受付中</span></td>
<td data-label="提供開始"><span class="stage stage-todo">未定</span></td></tr>''' for p in PRODUCTS)

    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="motto" lang="en">Tools for the people who build.</p>
      <h1><span class="nb">現場の仕事に、</span><span class="nb">ちょうどいい道具を。</span></h1>
      <p class="hero-lead">左官の数量拾い、配管の材料拾い、見積書と請求書。建設・設備業の小さな事業者のために、職種ごとの業務ソフトを開発しています。</p>
      <div class="actions">
        <a class="btn btn-bronze" href="contact.html">先行利用・体験を相談する</a>
        <a class="btn btn-line-light" href="#products">製品を見る</a>
      </div>
      <p class="hero-note">3製品とも開発中です。このサイトの製品画面は、すべて開発中の試作版を実際に動かして撮影したものです。</p>
    </div>
  </div>
</section>
<div class="shot-overlap"><div class="wrap">
    <figure class="annotated hero-figure">
      <div class="screen screen-lg">
        <picture>
          <source media="(max-width: 699px)" srcset="img/screens/nuriq-plan-sm.webp?v={ASSET_VER}" width="900" height="661">
          {img("img/screens/nuriq-plan.webp", "NURIQの試作版で、サンプル図面の平面図から倉庫の床面積12.60㎡を測った画面", 1600, 1000, lazy=False)}
        </picture>
        {"".join(f'<span class="pin pin-sm-hide" style="left:{x}%;top:{y}%" aria-hidden="true">{i}</span>' for i, (x, y, _t) in enumerate(HERO_PINS, 1))}
        <span class="pin pin-sm-only" style="left:55.3%;top:76.4%" aria-hidden="true">3</span>
      </div>
      <figcaption>
        <p class="cap-title">NURIQ 試作版の画面（図面は説明用に作った架空のサンプル）</p>
        <ol class="legend">{"".join(f'<li{" class=\"lg-only\"" if i < 3 else ""}><span class="pin-n" aria-hidden="true">{i}</span>{escape(t)}</li>' for i, (_x, _y, t) in enumerate(HERO_PINS, 1))}</ol>
      </figcaption>
    </figure>
</div></div>

<section class="section pains" aria-labelledby="h-pains"><div class="wrap">
  <div class="section-head">
    <h2 id="h-pains">現場が終わってから、もう一仕事。</h2>
    <p>見積もりの拾い出しも、書類づくりも、職種によって手間のかかる所が違います。CRAFTFLOWは、その一つひとつに専用の道具を用意します。</p>
  </div>
  <div class="pain-grid">{pain_html}</div>
</div></section>

<div id="products" class="products-anchor"></div>

<section class="product-feature pf-nuriq" aria-labelledby="h-nuriq"><div class="wrap pf-grid">
  <div class="pf-copy">
    <p class="pf-trade">左官工事向け</p>
    <h2 id="h-nuriq" class="pf-name">NURIQ<span class="kana">ヌリック</span></h2>
    <p class="pf-catch">{escape(n["catch"])}</p>
    <p>{escape(n["lead"])}</p>
    <p class="pf-sub">試作版でできること</p>
    <ul class="check-list">{nuriq_points}</ul>
    <p class="pf-status">{status(("dev", PRODUCT_STATUS))}</p>
    <div class="actions"><a class="btn btn-navy" href="products/nuriq.html">NURIQの詳細</a><a class="link" href="contact.html?product=NURIQ">体験を相談する</a></div>
  </div>
  <div class="pf-media">
    {screen(r, "nuriq-items-crop", "NURIQで仕上表から左官工事の拾い項目を作った画面", "仕上表を読み取り、タイル・塗装などを除いた左官の工事だけを並べた状態。", 1200, 552)}
    {screen(r, "nuriq-3d-crop", "NURIQで平面図を3D表示し、拾った範囲を色分けした画面", "拾った範囲を3Dで確認。オレンジは自動で測った範囲と、まだ測っていない項目の位置。", 1200, 795)}
  </div>
</div></section>

<section class="product-feature pf-piping is-dark" aria-labelledby="h-piping"><div class="wrap">
  <div class="pf-head">
    <div>
      <p class="pf-trade">配管・水道設備工事向け</p>
      <h2 id="h-piping" class="pf-name is-long">配管見積もりシステム<span class="kana">仮称</span></h2>
    </div>
    <p class="pf-catch">{escape(pp["catch"])}</p>
  </div>
  <div class="pf-stage">
    {screen(r, "piping-plan3d", "配管見積もりシステムの試作版で、平面図と3Dを並べて配管を作図した画面")}
    {phone(r, "piping-mobile", "スマートフォンで表示した配管見積もりシステムの作図画面")}
  </div>
  <div class="pf-cols">
    <p>{escape(pp["lead"])}</p>
    <div>
      <p class="pf-sub">試作版でできること</p>
      <ul class="check-list">{pipe_points}</ul>
      <p class="pf-status">{status(("dev", PRODUCT_STATUS))}</p>
      <div class="actions"><a class="btn btn-bronze" href="products/piping.html">配管見積もりシステムの詳細</a><a class="link" href="contact.html?product=配管見積もりシステム">体験を相談する</a></div>
    </div>
  </div>
</div></section>

<section class="product-feature pf-estimate" aria-labelledby="h-estimate"><div class="wrap">
  <div class="pf-head">
    <div>
      <p class="pf-trade">個人事業主・一人親方向け</p>
      <h2 id="h-estimate" class="pf-name is-long">見積・請求アプリ<span class="kana">仮称</span></h2>
    </div>
    <p class="pf-catch">{escape(e["catch"])}</p>
  </div>
  <div class="phone-row">{est_phones}</div>
  <div class="pf-cols">
    <p>{escape(e["lead"])}</p>
    <div>
      <p class="pf-status">{status(("dev", PRODUCT_STATUS))}</p>
      <div class="actions"><a class="btn btn-navy" href="products/estimate.html">見積・請求アプリの詳細</a><a class="link" href="contact.html?product=見積・請求アプリ">体験を相談する</a></div>
    </div>
  </div>
</div></section>

<section class="section principles-sec is-dark" aria-labelledby="h-principles"><div class="wrap">
  <div class="section-head">
    <h2 id="h-principles">CRAFTFLOWのつくり方</h2>
    <p>機能の数ではなく、現場で毎日使えるかどうかで決めています。</p>
  </div>
  <div class="principles">{prin_html}</div>
</div></section>

<section class="section" aria-labelledby="h-progress"><div class="wrap">
  <div class="section-head">
    <h2 id="h-progress">開発の進み具合</h2>
    <p>3製品とも、試作版が動く段階です。実際の図面や書類で試していただき、使いにくい所を直してから提供を始めます。</p>
  </div>
  <div class="table-scroll"><table class="stage-table">
    <thead><tr><th scope="col">製品</th><th scope="col">試作版</th><th scope="col">現場での試用</th><th scope="col">提供開始</th></tr></thead>
    <tbody>{stage_rows}</tbody>
  </table></div>
  <p class="note">試用にご協力いただける方には、提供開始前の画面で実際の業務を試していただき、ご意見をもとに改善します。条件は個別にご相談ください。</p>
</div></section>

<section class="section section-alt" aria-labelledby="h-faq"><div class="wrap narrow">
  <div class="section-head"><h2 id="h-faq">よくある質問</h2></div>
  {faq_html(COMMON_FAQ[:4])}
  <p class="more-row"><a class="link" href="faq.html">すべての質問を見る</a></p>
</div></section>
{contact_block(r, '<span class="nb">まずは、</span><span class="nb">いまの仕事のやり方を</span><span class="nb">聞かせてください。</span>', "使っている図面や書類、困っている作業をお知らせいただければ、合いそうな製品と試用の進め方をご案内します。", dark=True)}'''
    return page("index.html", "CRAFTFLOW｜建設・設備業向け業務ソフト（左官の数量拾い・配管見積もり・見積請求）",
                "左官工事の数量拾い（NURIQ）、配管ルートと材料拾い・見積もり、見積書・請求書のスマホアプリ。建設・設備業の小規模事業者向けに業務ソフトを開発するCRAFTFLOWの公式サイトです。",
                body, keywords="左官 見積もり ソフト,左官 数量拾い,配管 見積もり ソフト,配管材料 拾い出し,建設業 見積書 アプリ,個人事業主 請求書 アプリ",
                body_class="is-home")


# ---------------------------------------------------------------- 製品一覧
def products_page():
    r = ""
    thumbs = {"nuriq": ("nuriq-plan", 1600, 1000), "piping": ("piping-plan3d", 1600, 1000)}
    rows = []
    for p in PRODUCTS:
        if p["slug"] == "estimate":
            media = '<div class="phone-pair">' + "".join(phone(r, s, alt) for s, alt, _c in p["phones"][:2]) + "</div>"
        else:
            s, w, h = thumbs[p["slug"]]
            media = f'<div class="screen">{img("img/screens/" + s + ".webp", plain_name(p) + "の試作版の画面", w, h)}</div>'
        rows.append(f'''<article class="product-row">
  <div class="pr-media">{media}</div>
  <div class="pr-copy">
    <p class="pf-trade">{escape(p["trade"])}</p>
    <h2 class="pr-name">{pname(p)}</h2>
    <p class="pr-cat">{escape(p["category"])}</p>
    <p>{escape(p["short"])}</p>
    <p class="pf-status">{status(("dev", PRODUCT_STATUS))}</p>
    <div class="actions"><a class="btn btn-navy" href="products/{p["slug"]}.html">{escape(p["name"])}の詳細</a></div>
  </div>
</article>''')
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a><span aria-hidden="true">／</span>製品</p>
  <h1>製品</h1>
  <p class="page-lead">職種ごとの仕事に合わせた3つの業務ソフトを開発しています。いずれも開発中で、掲載している画面は試作版を動かして撮影したものです。</p>
</div></section>
<section class="section"><div class="wrap product-rows">{"".join(rows)}</div></section>
{contact_block(r, "どの製品が合うか、相談したい方へ", "仕事の内容をお聞きして、合いそうな製品と試用の進め方をご案内します。")}'''
    return page("products.html", "製品一覧", "左官工事の数量拾い・見積もりソフトNURIQ、配管見積もりシステム（仮称）、見積・請求アプリ（仮称）。CRAFTFLOWが開発中の3製品の概要です。", body, current="products.html",
                keywords="左官 見積もり ソフト,配管 見積もり ソフト,建設業 見積書 アプリ")


# ---------------------------------------------------------------- 製品詳細
DETAIL_PINS = {
    "nuriq": ("nuriq-plan", "NURIQの試作版で、サンプル図面の平面図から倉庫の床面積を測った画面", HERO_PINS),
    "piping": ("piping-plan3d", "配管見積もりシステムの試作版で、平面図と3Dを並べて配管を作図した画面", [
        (17.6, 18.0, "階ごとに間取りを作り、床下・2階も切り替え"),
        (31.0, 50.0, "器具の接続口から指でなぞって配管"),
        (64.0, 45.0, "描いた配管が3Dにそのまま表示される"),
        (25.5, 90.2, "材料費と合計金額が画面の下に出る"),
    ]),
}


def product_page(p):
    r = "../"
    slug = p["slug"]
    name_html = pname(p)
    kana = "（仮称）" if p["kana"] == "仮称" else f'（{p["kana"]}）'
    probs = "".join(f"<li><h3>{escape(a)}</h3><p>{escape(b)}</p></li>" for a, b in p["problems"])
    fors = "".join(f"<li>{escape(x)}</li>" for x in p["for"])
    notes = "".join(f"<li>{escape(x)}</li>" for x in p["notes"])

    if slug in DETAIL_PINS:
        shot, alt, pins = DETAIL_PINS[slug]
        head_media = f'<div class="shot-overlap"><div class="wrap">{annotated(r, shot, pins, alt, lazy=False)}</div></div>'
        gallery = '<div class="gallery">' + "".join(screen(r, g[0], g[1], escape(g[2]), *(g[3:] or (1600, 1000))) for g in p["gallery"]) + "</div>"
        if p.get("phone"):
            s, alt = p["phone"]
            gallery += f'<div class="gallery-phone">{phone(r, s, alt, "スマートフォンでも同じ工事を開いて確認できます。")}</div>'
    else:
        head_media = '<div class="shot-overlap"><div class="wrap detail-phones">' + "".join(phone(r, s, alt, escape(cap)) for s, alt, cap in p["phones"]) + "</div></div>"
        gallery = ""

    gallery_sec = f'''<section class="section section-alt" aria-labelledby="h-gallery"><div class="wrap">
  <div class="section-head"><h2 id="h-gallery">試作版の画面</h2><p>開発中の試作版を、説明用のサンプルデータで動かして撮影しました。</p></div>
  {gallery}
</div></section>''' if gallery else ""

    body = f'''
<section class="page-head product-head has-overlap"><div class="wrap">
  <p class="breadcrumb"><a href="../index.html">ホーム</a><span aria-hidden="true">／</span><a href="../products.html">製品</a><span aria-hidden="true">／</span>{escape(p["name"])}</p>
  <p class="pf-trade">{escape(p["category"])}</p>
  <h1 class="product-title{" is-long" if len(p["name"]) > 6 else ""}">{name_html}{'<span class="kana">ヌリック</span>' if slug == "nuriq" else ""}</h1>
  <p class="pf-catch">{escape(p["catch"])}</p>
  <p class="page-lead">{escape(p["lead"])}</p>
  <div class="actions">
    <a class="btn btn-bronze" href="../contact.html?product={escape(p["name"])}">先行利用・体験を相談する</a>
    {status(("dev", PRODUCT_STATUS))}
  </div>
</div>
</section>
{head_media}

<section class="section" aria-labelledby="h-problems"><div class="wrap">
  <div class="section-head"><h2 id="h-problems">こんな手間を減らします</h2></div>
  <ul class="problem-list">{probs}</ul>
</div></section>

<section class="section section-alt" aria-labelledby="h-features"><div class="wrap split">
  <div>
    <h2 id="h-features">主な機能</h2>
    <p>試作版で動作を確かめた機能と、開発・検討中の機能を分けて記載しています。提供開始時の内容は変わる場合があります。</p>
    <dl class="status-key">
      <div><dt>{status(PROTO)}</dt><dd>試作版で動作を確認済み</dd></div>
      <div><dt>{status(DEV)}</dt><dd>開発を進めている機能</dd></div>
      <div><dt>{status(PLAN)}</dt><dd>対応を検討している機能</dd></div>
    </dl>
  </div>
  <div>
    {feature_list(p)}
    <ul class="notes">{notes}</ul>
  </div>
</div></section>

{gallery_sec}

<section class="section" aria-labelledby="h-flow"><div class="wrap">
  <div class="section-head"><h2 id="h-flow">使い方の流れ</h2></div>
  {flow_list(p)}
</div></section>

<section class="section section-alt"><div class="wrap split">
  <div><h2>こんな方に</h2><ul class="plain-list">{fors}</ul></div>
  <div><h2>料金</h2><p class="price-tbd">未定</p><p>料金・提供開始時期については、お問い合わせください。<a href="../pricing.html">料金についての考え方</a></p></div>
</div></section>

<section class="section" aria-labelledby="h-pfaq"><div class="wrap narrow">
  <div class="section-head"><h2 id="h-pfaq">よくある質問</h2></div>
  {faq_html(p["faq"])}
</div></section>
{contact_block(r, f'<span class="nb">{escape(p["name"])}を</span><span class="nb">試してみたい方へ</span>', "いまの仕事の進め方と、使っている図面や書類の形式をお知らせください。試用の進め方をご案内します。", p["name"], dark=True)}'''
    return page(f'products/{slug}.html', f'{plain_name(p)}｜{p["category"]}',
                f'{p["lead"]}（開発中・試作版あり）', body, current="products.html", keywords=p["kw"])


# ---------------------------------------------------------------- 料金
def pricing():
    r = ""
    rows = "".join(f'<tr><th scope="row"><a href="products/{p["slug"]}.html">{pname(p)}</a></th><td>未定</td><td>{status(("dev", PRODUCT_STATUS))}</td></tr>' for p in PRODUCTS)
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a><span aria-hidden="true">／</span>料金</p>
  <h1>料金</h1>
  <p class="page-lead">料金はまだ決まっていません。月額制を基本に、個人事業主や小規模事業者が続けやすい料金を検討しています。</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="table-scroll"><table class="price-table">
    <thead><tr><th scope="col">製品</th><th scope="col">料金</th><th scope="col">状況</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p class="note">料金・提供開始時期については、お問い合わせください。</p>
</div></section>
<section class="section section-alt"><div class="wrap split">
  <div><h2>検討中の提供形態</h2><p>以下は検討中の内容で、提供を約束するものではありません。決まり次第このページでお知らせします。</p></div>
  <ul class="plain-list">
    <li>無料体験（試用）</li><li>月額プラン</li><li>年額プラン</li><li>機能を追加した上位プラン</li><li>追加機能のオプション</li>
  </ul>
</div></section>
<section class="section"><div class="wrap split">
  <div><h2>料金の考え方</h2></div>
  <div class="prose">
    <p>試作版は、使うたびに料金が発生する外部サービスを使わずに動く作りにしています。利用量に応じて費用が増えにくいため、小さな事業者でも続けやすい料金を目指せます。</p>
    <p>職種ごとに製品を分けているので、必要な製品だけを選んで使えるようにする予定です。</p>
  </div>
</div></section>
{contact_block(r, "料金について問い合わせる", "ご希望の製品と利用人数などをお知らせいただければ、決まり次第ご案内します。")}'''
    return page("pricing.html", "料金", "CRAFTFLOW製品の料金について。料金は現在検討中です。料金・提供開始時期についてはお問い合わせください。", body, current="pricing.html")


# ---------------------------------------------------------------- FAQ
def faq_page():
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a><span aria-hidden="true">／</span>よくある質問</p>
  <h1>よくある質問</h1>
  <p class="page-lead">ここにない質問は、お問い合わせからどうぞ。製品ごとの質問は、各製品のページにもあります。</p>
</div></section>
<section class="section"><div class="wrap narrow">{faq_html(COMMON_FAQ)}</div></section>
{contact_block("", "ほかに知りたいことがあれば", "使っている図面や書類、困っている作業など、どんなことでもお問い合わせください。")}'''
    return page("faq.html", "よくある質問", "CRAFTFLOW製品の利用条件、対応端末、料金、無料体験、データの保存、サポートなどについてのよくある質問です。", body, current="faq.html")


# ---------------------------------------------------------------- お問い合わせ
def contact():
    opts = "".join(f"<li>{escape(plain_name(p))}</li>" for p in PRODUCTS)
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a><span aria-hidden="true">／</span>お問い合わせ</p>
  <h1>お問い合わせ・先行利用</h1>
  <p class="page-lead">製品についての質問、先行利用（試用）や体験のご希望、導入の相談はこちらから。</p>
</div></section>
<section class="section"><div class="wrap split">
  <div>
    <h2>お伺いする内容</h2>
    <ul class="contact-fields">
      <li>会社名・屋号</li><li>お名前</li><li>メールアドレス</li><li>希望製品</li><li>お問い合わせ内容</li>
    </ul>
    <h2 class="mt">対象の製品</h2>
    <ul class="plain-list">{opts}</ul>
    <p class="note">いただいた情報は、お問い合わせへの回答と製品のご案内にのみ使用します。</p>
    <p id="product-hint" class="note" hidden>ご希望の製品：<strong></strong>（フォームの「希望製品」でお選びください）</p>
  </div>
  <div id="form-holder">
    <div class="notice">
      <p><strong>お問い合わせフォームは現在準備中です。</strong></p>
      <p>受付を開始するまで、もうしばらくお待ちください。準備ができ次第、このページから送信できるようになります。</p>
    </div>
  </div>
</div></section>'''
    return page("contact.html", "お問い合わせ・先行利用", "CRAFTFLOW製品へのお問い合わせ、先行利用（試用）・体験のご希望、導入の相談はこちらから。", body)


def not_found():
    body = '''
<section class="page-head"><div class="wrap">
  <h1>ページが見つかりません</h1>
  <p class="page-lead">URLが変わったか、ページが削除された可能性があります。</p>
  <div class="actions"><a class="btn btn-bronze" href="index.html">トップページへ戻る</a></div>
</div></section>'''
    html = page("404.html", "ページが見つかりません", "お探しのページは見つかりませんでした。", body)
    # 404 はどの階層からでも表示されるため、リンクを絶対パスにする
    b = BASE_PATH
    for a in ('href="css/', 'src="js/', 'href="img/', 'href="index.html', 'href="products', 'href="pricing', 'href="faq', 'href="contact'):
        attr, rest = a.split('="')
        html = html.replace(a, f'{attr}="{b}{rest}')
    return html


def main():
    files = {
        "index.html": index(),
        "products.html": products_page(),
        "pricing.html": pricing(),
        "faq.html": faq_page(),
        "contact.html": contact(),
        "404.html": not_found(),
    }
    for p in PRODUCTS:
        files[f'products/{p["slug"]}.html'] = product_page(p)
    for path, html in files.items():
        out = ROOT / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    urls = [k for k in files if k != "404.html"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        loc = SITE_URL + ("" if u == "index.html" else u)
        sm += f"  <url><loc>{loc}</loc><lastmod>{UPDATED}</lastmod></url>\n"
    sm += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    print("built", len(files), "pages")


if __name__ == "__main__":
    main()
