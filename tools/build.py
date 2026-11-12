#!/usr/bin/env python3
"""CRAFTFLOW サイト生成スクリプト

ヘッダー・フッター・メタ情報を全ページで揃えるために使います。
文言を直したいときはこのファイルの中身を編集して

    python3 tools/build.py

を実行すると、ルートにある各 HTML と sitemap.xml が書き換わります。
（Python 3 だけで動きます。追加インストールは不要です）
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://co-30.github.io/craftflow-website/"  # 公開URLが変わったらここを変更
UPDATED = "2026-11-12"
ASSET_VER = "2"  # CSS/JSを変えたら数字を上げる（キャッシュ対策）

NAV = [
    ("products.html", "製品"),
    ("pricing.html", "料金"),
    ("faq.html", "よくある質問"),
]

# ---------------------------------------------------------------- icons
LOGO = '''<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true"><rect x="1" y="1" width="30" height="30" rx="7" fill="#F07A1F"/><path d="M22.5 10.5a8 8 0 1 0 0 11M13 16h12M21.5 12.5 25 16l-3.5 3.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h17M14 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

PRODUCT_ART = {
    # wall + trowel + area hatch
    "nuriq": '''<svg viewBox="0 0 240 135" aria-hidden="true"><g fill="none" stroke="#A9B3C7" stroke-width="1.5"><rect x="30" y="20" width="120" height="95"/><path d="M30 45h120M30 70h120M30 95h120M70 20v25M110 20v25M50 45v25M90 45v25M130 45v25M70 70v25M110 70v25"/></g><path d="M30 20h120v95H30z" fill="#F07A1F" fill-opacity=".14"/><g stroke="#F07A1F" stroke-width="1.5"><path d="M30 10h120M30 6v8M150 6v8M160 20v95M156 20h8M156 115h8"/></g><text x="90" y="8" fill="#F07A1F" font-size="9" text-anchor="middle" font-family="Archivo,sans-serif">3,600</text><path d="M178 60l40-14 6 16-40 14z" fill="#F3F5F9"/><path d="M196 72l-6 22" stroke="#F3F5F9" stroke-width="5" stroke-linecap="round"/></svg>''',
    # pipe route
    "piping": '''<svg viewBox="0 0 240 135" aria-hidden="true"><g fill="none" stroke="#A9B3C7" stroke-width="1.2"><path d="M20 115h200M40 115V40l60-25 60 25v75"/><path d="M40 75h120"/></g><path d="M60 115V95h50v-35h40v-20" fill="none" stroke="#F07A1F" stroke-width="5" stroke-linejoin="round"/><g fill="#F3F5F9"><circle cx="60" cy="95" r="4.5"/><circle cx="110" cy="95" r="4.5"/><circle cx="110" cy="60" r="4.5"/><circle cx="150" cy="60" r="4.5"/></g><text x="85" y="88" fill="#F3F5F9" font-size="9" text-anchor="middle" font-family="Archivo,sans-serif">2.4m</text><text x="132" y="54" fill="#F3F5F9" font-size="9" text-anchor="middle" font-family="Archivo,sans-serif">1.6m</text></svg>''',
    # estimate document
    "estimate": '''<svg viewBox="0 0 240 135" aria-hidden="true"><rect x="70" y="12" width="84" height="112" rx="5" fill="#F3F5F9"/><rect x="82" y="24" width="36" height="7" rx="2" fill="#14213A"/><g fill="#A9B3C7"><rect x="82" y="44" width="60" height="4" rx="2"/><rect x="82" y="56" width="48" height="4" rx="2"/><rect x="82" y="68" width="54" height="4" rx="2"/><rect x="82" y="80" width="40" height="4" rx="2"/></g><rect x="82" y="98" width="60" height="14" rx="3" fill="#F07A1F"/><rect x="138" y="34" width="44" height="78" rx="8" fill="#14213A" stroke="#F3F5F9" stroke-width="2.5"/><rect x="146" y="46" width="28" height="4" rx="2" fill="#A9B3C7"/><rect x="146" y="56" width="20" height="4" rx="2" fill="#A9B3C7"/><rect x="146" y="92" width="28" height="9" rx="3" fill="#F07A1F"/></svg>''',
}

HERO_ART = '''<svg viewBox="0 0 640 440" role="img" aria-label="建物の立面図と、図面を表示したタブレットの線画">
  <defs>
    <pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#24355A" stroke-width=".6"/></pattern>
  </defs>
  <rect width="640" height="440" fill="url(#g)"/>
  <!-- building frame: columns and floor slabs -->
  <g fill="none" stroke="#7F8DA8" stroke-width="1.4">
    <path class="draw" d="M70 380V90h300v290M70 162h300M70 234h300M70 306h300M145 90v290M220 90v290M295 90v290"/>
    <path class="draw d2" d="M70 90l60-40h300l-60 40M430 50v290l-60 40M430 122l-60 40M430 194l-60 40M430 266l-60 40"/>
  </g>
  <!-- openings -->
  <g fill="#F3F5F9" fill-opacity=".07" stroke="#A9B3C7" stroke-width="1">
    <rect x="88" y="182" width="38" height="34"/><rect x="163" y="182" width="38" height="34"/><rect x="238" y="182" width="38" height="34"/><rect x="313" y="182" width="38" height="34"/>
    <rect x="88" y="110" width="38" height="34"/><rect x="163" y="110" width="38" height="34"/><rect x="238" y="110" width="38" height="34"/><rect x="313" y="110" width="38" height="34"/>
    <rect x="88" y="254" width="38" height="34"/><rect x="313" y="254" width="38" height="34"/>
  </g>
  <!-- dimension lines (the estimator's view) -->
  <g stroke="#F07A1F" stroke-width="1.4" fill="none">
    <path class="draw d3" d="M70 410h300M70 402v16M370 402v16M40 90v290M32 90h16M32 380h16"/>
  </g>
  <g fill="#F07A1F" font-family="Archivo, sans-serif" font-size="13" font-weight="600">
    <text x="220" y="430" text-anchor="middle">12,000</text>
    <text x="26" y="240" text-anchor="middle" transform="rotate(-90 26 240)">11,600</text>
  </g>
  <!-- tablet with a floor plan -->
  <g transform="translate(372 236) rotate(-6)">
    <rect width="236" height="164" rx="14" fill="#0D1729" stroke="#F3F5F9" stroke-width="3"/>
    <rect x="12" y="12" width="212" height="140" rx="4" fill="#14213A"/>
    <rect x="12" y="12" width="212" height="20" fill="#1C2C4B"/>
    <circle cx="24" cy="22" r="3.5" fill="#F07A1F"/>
    <rect x="34" y="19" width="50" height="6" rx="3" fill="#566074"/>
    <g fill="none" stroke="#F3F5F9" stroke-width="1.6">
      <path d="M30 46h120v92H30zM30 90h60v48M90 46v28M118 90h32"/>
    </g>
    <path d="M30 46h120v92H30z" fill="#F07A1F" fill-opacity=".16"/>
    <g fill="#A9B3C7"><rect x="162" y="48" width="48" height="6" rx="3"/><rect x="162" y="62" width="36" height="6" rx="3"/><rect x="162" y="76" width="44" height="6" rx="3"/></g>
    <rect x="162" y="118" width="48" height="18" rx="4" fill="#F07A1F"/>
  </g>
</svg>'''

ICONS = {
    "phone": '<svg class="feature-icon" viewBox="0 0 40 40" aria-hidden="true"><rect x="11" y="4" width="18" height="32" rx="4" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M17 31h6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "craft": '<svg class="feature-icon" viewBox="0 0 40 40" aria-hidden="true"><path d="M6 34L24 16M22 6l12 12-6 2-8-8z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/></svg>',
    "simple": '<svg class="feature-icon" viewBox="0 0 40 40" aria-hidden="true"><rect x="6" y="6" width="28" height="28" rx="6" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M13 20l5 5 10-11" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "cost": '<svg class="feature-icon" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="14" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M14 13l6 8 6-8M20 21v9M15 23h10M15 27h10" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
}

# ---------------------------------------------------------------- content
DEV = '<span class="status status-dev">開発中</span>'

PRODUCTS = [
    {
        "slug": "nuriq",
        "name": "NURIQ",
        "kana": "ヌリック",
        "category": "左官工事向け 見積もり・拾い出し支援",
        "catch": "図面から、左官の数量拾いをもっと速く。",
        "desc": "図面を使って左官工事の数量を拾い出し、見積もりづくりまでの手間を減らすためのシステムです。",
        "for": ["左官業者・左官職人", "建設会社の積算・見積もり担当", "左官工事を含む工事の見積もりを作る方"],
        "problems": [
            ("拾い出しに時間がかかる", "壁・床・天井ごとに面積を手計算し、何度も図面と電卓を往復している。"),
            ("担当者によって数字がぶれる", "計算の手順が人によって違い、見積もりの根拠を説明しにくい。"),
            ("見積書への転記が手間", "拾った数量を別の表計算や書式に打ち直している。"),
        ],
        "features": [
            ("図面を見ながらの数量拾い出し", DEV),
            ("部位・仕上げごとの面積集計", DEV),
            ("拾い出し結果からの見積もり作成", DEV),
            ("図面のAI解析による自動拾い出し", '<span class="status status-dev">将来対応を検討</span>'),
        ],
        "scene": "現場調査のあと、事務所で図面を開いて部位ごとに範囲を指定。集計された数量をそのまま見積もりに使う、という流れを想定しています。",
        "kw": "左官 見積もり ソフト,左官 数量拾い,左官工事 積算",
        "faq": [
            ("どんな図面に対応しますか？", "対応する図面の形式は開発中のため確定していません。お使いの図面の形式をお問い合わせでお知らせいただければ、対応予定をご案内します。"),
            ("いつから使えますか？", "提供開始時期は未定です。お問い合わせいただいた方には、体験版の準備ができ次第ご連絡します。"),
        ],
    },
    {
        "slug": "piping",
        "name": "配管見積もりシステム",
        "kana": "仮称",
        "category": "配管工事向け ルート作成・材料拾い・見積もり支援",
        "catch": "配管ルートを描けば、長さと材料が見えてくる。",
        "desc": "新築・修理・リフォームの配管工事で、ルートの作成から配管長さ・材料の拾い出し、見積もりまでを支援するシステムです。",
        "for": ["水道設備業者", "配管工事業者", "設備工事の個人事業主・小規模会社"],
        "problems": [
            ("配管の長さを数えるのが大変", "図面に定規を当てて区間ごとに長さを測り、継手の数も目で数えている。"),
            ("お客様に工事内容が伝わりにくい", "どこにどう配管するのか、言葉と平面図だけでは説明しづらい。"),
            ("申請書類づくりに手間がかかる", "工事のたびに届出用の図面や書類を一から用意している。"),
        ],
        "features": [
            ("配管ルートの作成", DEV),
            ("2D・3Dでの建物と配管の表示", DEV),
            ("配管長さ・材料の拾い出し", DEV),
            ("見積もり作成", DEV),
            ("申請・届出書類の作成支援", '<span class="status status-dev">将来対応を検討</span>'),
        ],
        "scene": "建物の平面に沿って配管ルートを引き、3Dで確認。区間ごとの長さと継手の数を集計して、材料の発注や見積もりに使う流れを想定しています。",
        "kw": "配管 見積もり ソフト,配管材料 拾い出し,水道工事 見積もり",
        "faq": [
            ("新築だけでなく修理やリフォームにも使えますか？", "新築・修理・リフォームのいずれにも使えるよう設計を進めています。具体的な対応範囲は提供開始時にご案内します。"),
            ("製品名は決まっていますか？", "現在は仮称です。正式名称は決まり次第このページでお知らせします。"),
        ],
    },
    {
        "slug": "estimate",
        "name": "見積・請求アプリ",
        "kana": "仮称",
        "category": "見積書・請求書の作成と管理",
        "catch": "見積書も請求書も、現場からスマホで。",
        "desc": "見積書・請求書の作成と、顧客情報や書類の管理をスマートフォンからでも行えるようにするアプリです。",
        "for": ["個人事業主・一人親方", "建設業・設備業の小規模事業者", "事務担当を置いていない事業者"],
        "problems": [
            ("書類づくりが夜の仕事になる", "現場が終わってから事務所に戻り、見積書や請求書を作っている。"),
            ("過去の書類が探せない", "どのお客様にいつ何を出したか、ファイルや紙が散らばっている。"),
            ("同じ情報を何度も入力している", "お客様の住所や品目を書類のたびに打ち直している。"),
        ],
        "features": [
            ("見積書の作成", DEV),
            ("請求書の作成（見積書からの変換を含む）", DEV),
            ("顧客情報の管理", DEV),
            ("作成した書類の一覧・検索", DEV),
            ("スマートフォンからの利用", DEV),
        ],
        "scene": "現場での打ち合わせ中に、スマートフォンで見積書を作ってその場で提示。工事が終わったら同じ内容から請求書を作る、という使い方を想定しています。",
        "kw": "建設業 見積書 アプリ,個人事業主 請求書 アプリ,一人親方 見積書",
        "faq": [
            ("インボイス制度に対応しますか？", "対応方針は開発中のため確定していません。提供開始時にご案内します。必要な項目があればお問い合わせでお知らせください。"),
            ("パソコンでも使えますか？", "スマートフォンでの利用を中心に開発していますが、パソコンでの利用可否は提供開始時にご案内します。"),
        ],
    },
]

COMMON_FAQ = [
    ("個人事業主でも利用できますか？", "はい。CRAFTFLOW の製品は、個人事業主・一人親方・小規模事業者の方に使っていただくことを前提に開発しています。"),
    ("スマートフォンでも使えますか？", "スマートフォンでの利用を重視して開発していますが、対応状況は製品ごとに異なります。各製品の提供開始時にご案内します。"),
    ("Windows・Macに対応していますか？", "動作環境は製品ごとに提供開始時に確定します。お使いの環境をお問い合わせでお知らせいただければ、対応予定をご案内します。"),
    ("無料体験はできますか？", "無料体験の実施を検討しています。条件や開始時期が決まり次第、このサイトでお知らせします。ご希望の方はお問い合わせください。"),
    ("月額料金はいくらですか？", "料金はまだ確定していません。料金・提供開始時期についてはお問い合わせください。"),
    ("解約はできますか？", "契約・解約の条件は、販売開始前に利用規約で定めて公開します。"),
    ("データの保存方法は？", "データの保存先や保存方法は製品ごとに提供開始時にご案内します。なお、このウェブサイト自体にはお客様の情報を保存していません。"),
    ("サポートはありますか？", "お問い合わせフォームからのご質問に対応します。提供開始後のサポート内容は製品ごとにご案内します。"),
]


# ---------------------------------------------------------------- layout
def page(path, title, description, body, current=None, keywords=""):
    depth = path.count("/")
    r = "../" * depth
    url = SITE_URL + ("" if path == "index.html" else path)
    nav_items = "".join(
        f'<li><a href="{r}{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a></li>'
        for href, label in NAV
    )
    kw = f'\n<meta name="keywords" content="{escape(keywords)}">' if keywords else ""
    full_title = title if path == "index.html" else f"{title}｜CRAFTFLOW"
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
<meta name="theme-color" content="#14213A">
<link rel="icon" href="{r}img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Zen+Kaku+Gothic+New:wght@400;700;900&display=swap">
<link rel="stylesheet" href="{r}css/site.css?v={ASSET_VER}">
</head>
<body>
<a class="skip" href="#main">本文へ移動</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r}index.html" aria-label="CRAFTFLOW トップページ">{LOGO}CRAFTFLOW</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">メニュー</button>
    <nav id="site-nav" class="site-nav" aria-label="メインメニュー">
      <ul>{nav_items}<li class="nav-cta"><a class="btn btn-primary" href="{r}contact.html">導入について相談する</a></li></ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{r}index.html">{LOGO}CRAFTFLOW</a>
        <p>建設・設備業の現場と事務をつなぐ、<br>実務に寄り添った業務支援ソフトウェア。</p>
      </div>
      <div><h2>製品</h2><ul>
        <li><a href="{r}products/nuriq.html">NURIQ（左官）</a></li>
        <li><a href="{r}products/piping.html">配管見積もりシステム</a></li>
        <li><a href="{r}products/estimate.html">見積・請求アプリ</a></li>
      </ul></div>
      <div><h2>ご案内</h2><ul>
        <li><a href="{r}products.html">製品一覧</a></li>
        <li><a href="{r}pricing.html">料金</a></li>
        <li><a href="{r}faq.html">よくある質問</a></li>
      </ul></div>
      <div><h2>お問い合わせ</h2><ul>
        <li><a href="{r}contact.html">お問い合わせ・体験希望</a></li>
      </ul></div>
    </div>
    <p class="copyright">&copy; 2026 CRAFTFLOW</p>
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


def product_cards(r):
    out = []
    for p in PRODUCTS:
        name = escape(p["name"])
        kana = f'<span class="kana">{"（" + p["kana"] + "）" if p["kana"] != "仮称" else "（仮称）"}</span>'
        out.append(f'''<article class="product">
  <div class="product-visual">{PRODUCT_ART[p["slug"]]}</div>
  <div class="product-body">
    <div class="product-name"><h3>{name}</h3>{kana}</div>
    <p class="product-for">{escape(p["category"])}　{DEV}</p>
    <p class="desc">{escape(p["desc"])}</p>
    <a class="more" href="{r}products/{p["slug"]}.html">{name}の詳細を見る</a>
  </div>
</article>''')
    return '<div class="products">' + "".join(out) + "</div>"


def cta_band(r, title="まずはお気軽にご相談ください", text="導入の時期や、いま困っている業務のことなど、どんなことでもお問い合わせください。", product=""):
    q = f"?product={product}" if product else ""
    return f'''<section class="section"><div class="wrap"><div class="cta-band">
  <div><h2>{title}</h2><p>{text}</p></div>
  <a class="btn btn-primary" href="{r}contact.html{q}">導入について相談する</a>
</div></div></section>'''


# ---------------------------------------------------------------- pages
def index():
    r = ""
    issues = [
        ("見積もりの拾い出しに何時間もかかる", "図面と電卓を往復して、面積や長さを手で数えている。"),
        ("書類づくりが現場のあとに残る", "見積書や請求書は、夜や休日に事務所でまとめて作っている。"),
        ("現場と事務で情報がつながらない", "現場で聞いた内容を、事務所で紙やメモから打ち直している。"),
        ("大きなシステムは高くて合わない", "大企業向けのソフトは機能が多すぎて、費用も見合わない。"),
    ]
    issue_html = "".join(f'<li><span class="box" aria-hidden="true"></span><div><strong>{escape(a)}</strong><span>{escape(b)}</span></div></li>' for a, b in issues)
    steps = [
        ("お問い合わせ", "フォームから、気になる製品や困っている業務をお知らせください。"),
        ("ヒアリング", "いまの業務の進め方と、改善したい点をお聞きします。"),
        ("体験・ご提案", "体験版の準備ができ次第、実際の操作をお試しいただけます。"),
        ("導入", "ご納得いただけたら利用開始。使い方のご質問にも対応します。"),
    ]
    step_html = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in steps)
    feats = [
        ("craft", "現場目線でつくる", "左官・配管・見積もりなど、職種ごとの実務に合わせて設計しています。"),
        ("phone", "スマートフォン重視", "事務所に戻らなくても、現場で使えることを目指しています。"),
        ("simple", "必要な機能にしぼる", "多機能さよりも、毎日の作業が速く終わることを優先します。"),
        ("cost", "小さな事業者が続けやすい", "個人事業主や小規模な会社でも無理なく続けられる提供方法を検討しています。"),
    ]
    feat_html = "".join(f'<div class="feature">{ICONS[i]}<h3>{a}</h3><p>{b}</p></div>' for i, a, b in feats)
    body = f'''
<section class="hero"><div class="wrap"><div class="hero-panel">
  <div class="hero-top"><p class="wordmark">CRAFTFLOW</p><span class="badge">CONSTRUCTION TECH</span></div>
  <div class="hero-visual">{HERO_ART}</div>
  <div class="hero-copy">
    <h1><span class="nb">現場の仕事を、</span><span class="nb">もっとスマートに。</span></h1>
    <p class="hero-lead">建設・設備業の現場と事務をつなぐ、実務に寄り添った業務支援ソフトウェア。</p>
    <ul class="chips"><li>見積もり業務の効率化</li><li>現場と事務をつなぐ</li></ul>
    <div class="btn-row">
      <a class="btn btn-primary" href="products.html">製品を見る</a>
      <a class="btn btn-ghost" href="contact.html">導入について相談する</a>
    </div>
    <a class="hero-products" href="products.html">PRODUCTS {ARROW}</a>
  </div>
</div></div></section>

<section class="section" aria-labelledby="h-issues"><div class="wrap">
  <div class="section-head"><h2 id="h-issues">こんなこと、ありませんか。</h2><p>建設業・設備業の小さな事業者からよく聞く悩みです。</p></div>
  <ul class="issue-list">{issue_html}</ul>
</div></section>

<section class="section section-dark" aria-labelledby="h-solution"><div class="wrap">
  <div class="section-head"><h2 id="h-solution">CRAFTFLOW は、手作業の時間を減らすことに集中します。</h2><p>現場で見たもの、図面に描かれたものを、そのまま見積もりや書類につなげる。そのための道具を職種ごとに用意します。</p></div>
  <div class="solution">
    <div class="solution-item"><h3>拾い出しを速く</h3><p>図面から面積や長さを集計し、手計算と転記の時間を減らします。</p></div>
    <div class="solution-item"><h3>書類を現場で</h3><p>見積書・請求書をスマートフォンで作り、その場でお客様に提示できるようにします。</p></div>
    <div class="solution-item"><h3>説明を分かりやすく</h3><p>配管ルートなどを図で見せて、工事内容をお客様に伝えやすくします。</p></div>
  </div>
</div></section>

<section class="section section-mist" aria-labelledby="h-products"><div class="wrap">
  <div class="section-head"><h2 id="h-products">3つの製品</h2><p>いずれも現在開発中です。提供開始や体験版のご案内を希望される方は、お問い合わせください。</p></div>
  {product_cards(r)}
</div></section>

<section class="section" aria-labelledby="h-features"><div class="wrap">
  <div class="section-head"><h2 id="h-features">CRAFTFLOW の考え方</h2></div>
  <div class="features">{feat_html}</div>
</div></section>

<section class="section section-mist" aria-labelledby="h-steps"><div class="wrap">
  <div class="section-head"><h2 id="h-steps">導入までの流れ</h2></div>
  <ol class="steps">{step_html}</ol>
</div></section>

<section class="section" aria-labelledby="h-faq"><div class="wrap">
  <div class="section-head"><h2 id="h-faq">よくある質問</h2></div>
  {faq_html(COMMON_FAQ[:4])}
  <p><a class="btn btn-outline" href="faq.html" style="margin-top:28px">すべての質問を見る</a></p>
</div></section>
{cta_band(r)}'''
    return page("index.html", "CRAFTFLOW｜建設・設備業向け業務支援ソフトウェア",
                "左官の数量拾い、配管の材料拾い出し、見積書・請求書の作成など、建設・設備業の小規模事業者向けに業務支援ソフトウェアを開発するCRAFTFLOWの公式サイトです。",
                body, keywords="左官 見積もり ソフト,配管 見積もり ソフト,建設業 見積書 アプリ,個人事業主 請求書 アプリ")


def products_page():
    r = ""
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a> / 製品</p>
  <h1>製品一覧</h1>
  <p>職種ごとの実務に合わせた3つの製品を開発しています。各製品は現在開発中で、掲載している機能は開発中・予定のものを含みます。</p>
</div></section>
<section class="section section-mist"><div class="wrap">{product_cards(r)}</div></section>
{cta_band(r, "どの製品が合うか相談したい方へ", "業務の内容をお聞きして、合いそうな製品と提供予定をご案内します。")}'''
    return page("products.html", "製品一覧", "左官工事向けNURIQ、配管見積もりシステム、見積・請求アプリ。CRAFTFLOWが開発中の3製品の概要です。", body, current="products.html")


def product_page(p):
    r = "../"
    name = escape(p["name"])
    kana = "（仮称）" if p["kana"] == "仮称" else f'（{p["kana"]}）'
    probs = "".join(f'<li><span class="box" aria-hidden="true"></span><div><strong>{escape(a)}</strong><span>{escape(b)}</span></div></li>' for a, b in p["problems"])
    feats = "".join(f"<li><span>{escape(a)}</span>{s}</li>" for a, s in p["features"])
    fors = "".join(f"<li>{escape(x)}</li>" for x in p["for"])
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="../index.html">ホーム</a> / <a href="../products.html">製品</a> / {name}</p>
  <p class="mt-0">{escape(p["category"])}　{DEV}</p>
  <h1>{name}<span style="font-size:.5em;font-weight:700">{kana}</span></h1>
  <p>{escape(p["catch"])} {escape(p["desc"])}</p>
  <div class="btn-row" style="margin-top:24px"><a class="btn btn-primary" href="../contact.html?product={escape(p["name"])}">体験版・提供開始の案内を希望する</a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>解決したい課題</h2></div>
  <ul class="issue-list">{probs}</ul>
</div></section>

<section class="section section-mist"><div class="wrap detail-grid">
  <div>
    <h2 class="mt-0">主な機能</h2>
    <p class="note">現在すべて開発中です。正式に提供を開始した機能から、このページの表示を更新します。</p>
    <ul class="func-list">{feats}</ul>
  </div>
  <div>
    <h2 class="mt-0">操作画面</h2>
    <div class="shot"><div><strong>画面イメージは準備中です</strong>実際の製品画面ができ次第、ここに掲載します。</div></div>
  </div>
</div></section>

<section class="section"><div class="wrap detail-grid">
  <div><h2 class="mt-0">利用イメージ</h2><p>{escape(p["scene"])}</p></div>
  <div><h2 class="mt-0">こんな方に</h2><ul class="plain-list">{fors}</ul></div>
</div></section>

<section class="section section-mist"><div class="wrap">
  <div class="section-head"><h2>料金プラン</h2></div>
  <p class="notice">料金・提供開始時期については、お問い合わせください。</p>
  <p><a href="../pricing.html">料金についての考え方を見る</a></p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>よくある質問</h2></div>
  {faq_html(p["faq"])}
</div></section>
{cta_band(r, f"{name}の体験を希望する", "体験版の準備ができ次第ご連絡します。いまの業務の進め方もお聞かせください。", escape(p["name"]))}'''
    return page(f'products/{p["slug"]}.html', f'{p["name"]}{kana}｜{p["category"]}', f'{p["desc"]}（開発中）', body, current="products.html", keywords=p["kw"])


def pricing():
    r = ""
    rows = "".join(f'<tr><th scope="row">{escape(p["name"])}</th><td>未定</td><td>{DEV}</td></tr>' for p in PRODUCTS)
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a> / 料金</p>
  <h1>料金プラン</h1>
  <p>月額制を基本に、個人事業主や小規模事業者が続けやすい料金を検討しています。</p>
</div></section>
<section class="section"><div class="wrap">
  <p class="notice">料金はまだ確定していません。料金・提供開始時期についてはお問い合わせください。</p>
  <div class="table-scroll" style="margin-top:32px"><table class="price-table">
    <thead><tr><th scope="col">製品</th><th scope="col">料金</th><th scope="col">状況</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</div></section>
<section class="section section-mist"><div class="wrap">
  <div class="section-head"><h2>検討中の提供形態</h2><p>以下は検討中の内容で、提供を約束するものではありません。決まり次第このページでお知らせします。</p></div>
  <ul class="plain-list">
    <li>無料体験</li><li>月額プラン</li><li>年額プラン</li><li>機能を追加した上位プラン</li><li>AI機能の追加オプション</li>
  </ul>
</div></section>
{cta_band(r, "料金について問い合わせる", "ご希望の製品と、利用人数などをお知らせいただければ、決まり次第ご案内します。")}'''
    return page("pricing.html", "料金プラン", "CRAFTFLOW製品の料金プランについて。料金は現在検討中です。料金・提供開始時期についてはお問い合わせください。", body, current="pricing.html")


def faq_page():
    body = f'''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a> / よくある質問</p>
  <h1>よくある質問</h1>
  <p>ここにない質問は、お問い合わせフォームからお気軽にどうぞ。</p>
</div></section>
<section class="section"><div class="wrap">{faq_html(COMMON_FAQ)}</div></section>
{cta_band("")}'''
    return page("faq.html", "よくある質問", "CRAFTFLOW製品の利用条件、対応端末、料金、無料体験、サポートなどについてのよくある質問です。", body, current="faq.html")


def contact():
    body = '''
<section class="page-head"><div class="wrap">
  <p class="breadcrumb"><a href="index.html">ホーム</a> / お問い合わせ</p>
  <h1>お問い合わせ・体験希望</h1>
  <p>製品についてのご質問、体験版のご希望、導入のご相談はこちらから。</p>
</div></section>
<section class="section"><div class="wrap detail-grid">
  <div>
    <h2 class="mt-0">お伺いする内容</h2>
    <ul class="contact-fields">
      <li>会社名・屋号</li><li>お名前</li><li>メールアドレス</li><li>希望製品</li><li>お問い合わせ内容</li>
    </ul>
    <p class="note">いただいた情報は、お問い合わせへの回答と製品のご案内にのみ使用します。</p>
    <p id="product-hint" class="note" hidden>ご希望の製品：<strong></strong>（フォームの「希望製品」でお選びください）</p>
  </div>
  <div id="form-holder">
    <div class="notice">
      <p class="mt-0"><strong>お問い合わせフォームは現在準備中です。</strong></p>
      <p style="margin-bottom:0">受付を開始するまで、もうしばらくお待ちください。</p>
    </div>
  </div>
</div></section>'''
    return page("contact.html", "お問い合わせ・体験希望", "CRAFTFLOW製品へのお問い合わせ、体験版のご希望、導入のご相談はこちらから。", body)


def not_found():
    body = '''
<section class="page-head"><div class="wrap">
  <h1>ページが見つかりません</h1>
  <p>URLが変わったか、ページが削除された可能性があります。</p>
  <div class="btn-row" style="margin-top:24px"><a class="btn btn-primary" href="/craftflow-website/index.html">トップページへ戻る</a></div>
</div></section>'''
    html = page("404.html", "ページが見つかりません", "お探しのページは見つかりませんでした。", body)
    # 404 is served from any depth: make asset links absolute
    return html.replace('href="css/', 'href="/craftflow-website/css/').replace('src="js/', 'src="/craftflow-website/js/').replace('href="img/', 'href="/craftflow-website/img/').replace('href="index.html', 'href="/craftflow-website/index.html').replace('href="products', 'href="/craftflow-website/products').replace('href="pricing', 'href="/craftflow-website/pricing').replace('href="faq', 'href="/craftflow-website/faq').replace('href="contact', 'href="/craftflow-website/contact')


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
