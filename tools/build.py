# -*- coding: utf-8 -*-
"""
Генератор статических страниц сайта школы (RU / EN / MN).
Запуск:  python tools/build.py

  /            — русская версия (основная; раздел /sveden/ по Приказу
                 Рособрнадзора № 1493 от 04.08.2023, с микроразметкой itemprop)
  /en/         — английская версия
  /mn/         — монгольская версия

Тексты задаются через L("рус", "eng", "монг"). Данные школы — в SCHOOL.
После правки снова запустите скрипт.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
def asset_ver(rel):
    """Хэш файла для сброса кэша браузера после изменений."""
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]


# Данные, перенесённые со старого сайта (http://erdenetschool.edu.mn, WordPress)
OLD = json.loads((Path(__file__).resolve().parent / "oldsite.json").read_text(encoding="utf-8"))

_TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюяөү",
               ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t",
                "u", "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya", "o", "u"]))


def translit(name):
    """Кириллица → латиница для английской версии (ФИО)."""
    out = "".join(_TR.get(c.lower(), c) for c in name)
    return " ".join(w[:1].upper() + w[1:] for w in out.split())


def fio(name):
    return L(name, translit(name), name)


def phone_fmt(raw):
    """+976(757)73851 → +976 7577-3851"""
    d = re.sub(r"\D", "", raw)
    return f"+{d[:3]} {d[3:7]}-{d[7:]}" if len(d) == 11 else raw


POSTS = {
    "учитель математики": ("Mathematics teacher", "Математикийн багш"),
    "учитель английского языка": ("English teacher", "Англи хэлний багш"),
    "учитель географии": ("Geography teacher", "Газарзүйн багш"),
    "учитель истории": ("History teacher", "Түүхийн багш"),
    "учитель истории и обществознания": ("History and social studies teacher", "Түүх, нийгмийн ухааны багш"),
    "учитель монгольского языка": ("Mongolian language teacher", "Монгол хэлний багш"),
    "учитель монгольской литературы и старописьменного монгольского языка": ("Mongolian literature and classical script teacher", "Монгол уран зохиол, монгол бичгийн багш"),
    "учитель музыки": ("Music teacher", "Хөгжмийн багш"),
    "учитель начальных классов": ("Primary school teacher", "Бага ангийн багш"),
    "учитель русского языка и литературы": ("Russian language and literature teacher", "Орос хэл, уран зохиолын багш"),
    "учитель технологии": ("Technology teacher", "Технологийн багш"),
    "учитель физики": ("Physics teacher", "Физикийн багш"),
    "учитель физической культуры": ("Physical education teacher", "Биеийн тамирын багш"),
    "учитель химии": ("Chemistry teacher", "Химийн багш"),
    "учитель ИЗО, черчения": ("Art and technical drawing teacher", "Дүрслэх урлаг, зураг зүйн багш"),
    "Директор школы": ("Principal", "Захирал"),
    "Ведущий менеджер": ("Lead manager", "Ахлах менежер"),
    "Заместитель директора по учебно-воспитательной работе": ("Deputy Principal for Academic Affairs", "Сургалт, хүмүүжил хариуцсан орлогч захирал"),
}
LEVELS = {"высшее": ("Higher", "Дээд"), "среднее профессиональное": ("Vocational", "Тусгай дунд"),
          "среднее специальное": ("Vocational", "Тусгай дунд")}
CATEGORIES = {"высшая квалификационная категория": ("Highest", "Дээд ангилал"),
              "первая квалификационная категория": ("First", "Нэгдүгээр ангилал")}


def tr(dic, ru):
    if ru in dic:
        en, mn = dic[ru]
        return L(ru[:1].upper() + ru[1:], en, mn)
    return ru or "—"


SITE_URL = "http://erdenetschool.edu.mn"  # замените на адрес сайта

LANGS = [("ru", "RU", "Русский"), ("en", "EN", "English"), ("mn", "MN", "Монгол")]
CUR = "ru"  # текущий язык при генерации


def L(ru, en, mn):
    return {"ru": ru, "en": en, "mn": mn}[CUR]


def ip(name):
    """Микроразметка itemprop — только в русской версии (её проверяет Рособрнадзор)."""
    return f' itemprop="{name}"' if name and CUR == "ru" else ""


def school():
    return {
        "full": L("Средняя общеобразовательная школа № 19 ПГС «Предприятие Эрдэнэт»",
                  "Secondary School No. 19 of Erdenet Mining Corporation",
                  "«Эрдэнэт үйлдвэр» ТӨҮГ-ын 19-р дунд сургууль"),
        "short_full": L("СОШ № 19 ПГС «Предприятие Эрдэнэт»", "School No. 19, Erdenet Mining Corporation", "«Эрдэнэт үйлдвэр» ТӨҮГ-ын 19-р сургууль"),
        "short": L("СОШ № 19", "School No. 19", "19-р дунд сургууль"),
        "city": L("г. Эрдэнэт", "Erdenet", "Эрдэнэт хот"),
        "address": L("61027, Монголия, Орхон аймак, г. Эрдэнэт, сомон Баян-Ундэр",
                     "Bayan-Undur soum, Erdenet, Orkhon Province, 61027, Mongolia",
                     "61027, Монгол Улс, Орхон аймаг, Эрдэнэт хот, Баян-Өндөр сум"),
        "phone": "+976 7577-3858",
        "email": "school19@erdenetmc.mn",
        "hours_short": "8:00–18:30",
        "hours": L("Начало занятий 1-й смены — 8:00, 2-й смены — 13:05; окончание работы — 18:30. Приёмная директора: 8:00–17:00",
                   "1st shift starts at 8:00, 2nd shift at 13:05; school closes at 18:30. Principal's office: 8:00–17:00",
                   "1-р ээлж 8:00, 2-р ээлж 13:05-д эхэлнэ; 18:30-д хаадаг. Захирлын өрөө: 8:00–17:00"),
        "regdate": L("1974 г.", "1974", "1974 он"),
        "languages": L("Русский, монгольский", "Russian, Mongolian", "Орос, монгол"),
        "director": fio("Степанова Светлана Иннокентьевна"),
    }


SVEDEN_SLUGS = ["common", "struct", "document", "education", "eduStandarts", "managers", "employees",
                "objects", "paid_edu", "budget", "vacant", "grants", "inter", "catering"]


def sveden_names():
    return [
        L("Основные сведения", "Basic Information", "Үндсэн мэдээлэл"),
        L("Структура и органы управления образовательной организацией", "Structure and Governing Bodies", "Бүтэц, удирдлагын байгууллага"),
        L("Документы", "Documents", "Баримт бичиг"),
        L("Образование", "Education", "Боловсрол"),
        L("Образовательные стандарты и требования", "Educational Standards and Requirements", "Боловсролын стандарт, шаардлага"),
        L("Руководство", "Management", "Удирдлага"),
        L("Педагогический состав", "Teaching Staff", "Багшийн бүрэлдэхүүн"),
        L("Материально-техническое обеспечение и оснащённость образовательного процесса. Доступная среда",
          "Facilities and Equipment. Accessible Environment",
          "Материаллаг-техникийн хангамж, тоноглол. Хүртээмжтэй орчин"),
        L("Платные образовательные услуги", "Paid Educational Services", "Төлбөртэй боловсролын үйлчилгээ"),
        L("Финансово-хозяйственная деятельность", "Financial and Economic Activities", "Санхүү, аж ахуйн үйл ажиллагаа"),
        L("Вакантные места для приёма (перевода) обучающихся", "Vacancies for Admission (Transfer)", "Элсэлт, шилжилтийн сул орон тоо"),
        L("Стипендии и меры поддержки обучающихся", "Scholarships and Student Support", "Тэтгэлэг, суралцагчдыг дэмжих арга хэмжээ"),
        L("Международное сотрудничество", "International Cooperation", "Олон улсын хамтын ажиллагаа"),
        L("Организация питания в образовательной организации", "School Meals", "Хоол хүнсний зохион байгуулалт"),
    ]


ICONS = ["🏫", "🗂️", "📄", "🎓", "📘", "👤", "👩‍🏫", "🧪", "💳", "📊", "🪑", "🎖️", "🌍", "🍎"]


# ------------------------------------------------------------------ helpers
def lang_prefix(code):
    return "" if code == "ru" else f"{code}/"


def layout(title, body, rel, current="", crumbs=None):
    """rel — путь страницы относительно корня языка, напр. 'sveden/common/index.html'."""
    S = school()
    depth = rel.count("/") + (0 if CUR == "ru" else 1)
    top = "../" * depth          # путь к корню сайта (assets, docs)
    p = top + lang_prefix(CUR)   # путь к корню текущего языка

    nav_items = [
        ("index.html", L("Главная", "Home", "Нүүр"), "home"),
        ("sveden/index.html", L("Сведения об ОО", "About the School", "Сургуулийн тухай"), "sveden"),
        ("index.html#news", L("Новости", "News", "Мэдээ"), "news"),
        ("materials/index.html", L("Образовательные материалы", "Learning Materials", "Сургалтын материал"), "materials"),
        ("index.html#parents", L("Родителям", "For Parents", "Эцэг эхчүүдэд"), "parents"),
        ("contacts.html", L("Контакты", "Contacts", "Холбоо барих"), "contacts"),
    ]
    # Выпадающие подменю: ключ пункта -> [(ссылка, подпись)]
    subs = {
        "sveden": [(f"{p}sveden/{s}/index.html", n) for s, n in zip(SVEDEN_SLUGS, sveden_names())],
        "parents": [
            ("https://e-mongolia.mn/news/n/8642", L("Запись в 1-й класс", "Grade 1 enrolment", "1-р ангид бүртгүүлэх")),
            ("https://myschool.edu.ru/", L("Электронный дневник", "Electronic diary", "Цахим өдрийн тэмдэглэл")),
            (f"{p}sveden/catering/index.html", L("Меню питания", "School menu", "Хоолны цэс")),
            (f"{p}sveden/vacant/index.html", L("Свободные места", "Vacant places", "Сул орон тоо")),
            (f"{p}sveden/paid_edu/index.html", L("Платные услуги", "Paid services", "Төлбөртэй үйлчилгээ")),
            (f"{p}sveden/document/index.html", L("Документы", "Documents", "Баримт бичиг")),
        ],
    }

    def nav_li(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        if key not in subs:
            return f'        <li><a href="{p}{href}"{cur}>{label}</a></li>'
        wide = " submenu--wide" if len(subs[key]) > 8 else ""
        items = "".join(
            f'<li><a href="{h}"' + (' rel="noopener"' if h.startswith("http") else "") + f'>{n}</a></li>'
            for h, n in subs[key]
        )
        return (f'        <li class="has-sub"><a href="{p}{href}"{cur} aria-haspopup="true">{label}</a>'
                f'<ul class="submenu{wide}">{items}</ul></li>')

    nav = "\n".join(nav_li(h, l, k) for h, l, k in nav_items)
    langs = "".join(
        f'<a href="{top}{lang_prefix(c)}{rel}" hreflang="{c}" lang="{c}" title="{name}"'
        f'{" aria-current=\"true\"" if c == CUR else ""}>{short}</a>'
        for c, short, name in LANGS
    )
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{c}" href="{SITE_URL}/{lang_prefix(c)}{rel.replace("index.html", "")}">'
        for c, _, _ in LANGS
    )

    head_block = ""
    if crumbs is not None:
        items = "".join(
            f'<li><a href="{p}{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>'
            for t, h in crumbs
        )
        head_block = f"""
  <section class="page-head">
    <div class="container">
      <nav class="breadcrumbs" aria-label="{L("Навигационная цепочка", "Breadcrumbs", "Байршил")}"><ol>{items}</ol></nav>
      <h1>{title}</h1>
    </div>
  </section>"""

    a11y_on = L("Версия для слабовидящих", "Low vision version", "Хараа муу хүмүүст")
    a11y_off = L("Обычная версия", "Standard version", "Энгийн хувилбар")
    tel = S["phone"].replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

    return f"""<!doctype html>
<html lang="{CUR}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {S["short"]}</title>
  <meta name="description" content="{L("Официальный сайт", "Official website of", "Албан ёсны вэбсайт —")} {S["short"]}, {S["city"]}">
{alternates}
  <link rel="icon" href="{top}favicon.ico" sizes="any">
  <link rel="icon" type="image/png" href="{top}assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="{top}assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="{top}assets/css/style.css?v={asset_ver("assets/css/style.css")}">
  <script>try{{var s=JSON.parse(localStorage.getItem('a11y-settings'));if(s&&s.on)document.documentElement.classList.add('a11y')}}catch(e){{}}</script>
</head>
<body>
<a class="skip-link" href="#main">{L("Перейти к содержимому", "Skip to content", "Агуулга руу шилжих")}</a>

<div class="a11y-panel" role="region" aria-label="{a11y_on}">
  <div class="container">
    <fieldset><legend>{L("Размер шрифта:", "Font size:", "Үсгийн хэмжээ:")}</legend>
      <button type="button" data-a11y-set="fs:1">A</button>
      <button type="button" data-a11y-set="fs:2" style="font-size:1.2em">A</button>
      <button type="button" data-a11y-set="fs:3" style="font-size:1.4em">A</button>
    </fieldset>
    <fieldset><legend>{L("Цвет:", "Colors:", "Өнгө:")}</legend>
      <button type="button" data-a11y-set="scheme:wb" aria-label="{L("Чёрным по белому", "Black on white", "Цагаан дээр хар")}">Ц</button>
      <button type="button" class="scheme-bw" data-a11y-set="scheme:bw" aria-label="{L("Белым по чёрному", "White on black", "Хар дээр цагаан")}">Ц</button>
      <button type="button" class="scheme-blue" data-a11y-set="scheme:blue" aria-label="{L("Тёмно-синим по голубому", "Dark blue on light blue", "Цайвар цэнхэр дээр хар хөх")}">Ц</button>
      <button type="button" class="scheme-beige" data-a11y-set="scheme:beige" aria-label="{L("Коричневым по бежевому", "Brown on beige", "Шаргал дээр бор")}">Ц</button>
    </fieldset>
    <fieldset><legend>{L("Изображения:", "Images:", "Зураг:")}</legend>
      <button type="button" data-a11y-set="noimg:false">{L("Вкл", "On", "Асаах")}</button>
      <button type="button" data-a11y-set="noimg:true">{L("Выкл", "Off", "Унтраах")}</button>
    </fieldset>
    <fieldset><legend>{L("Интервал:", "Spacing:", "Зай:")}</legend>
      <button type="button" data-a11y-set="ls:false">{L("Обычный", "Normal", "Энгийн")}</button>
      <button type="button" data-a11y-set="ls:true">{L("Большой", "Large", "Том")}</button>
    </fieldset>
    <button type="button" class="btn-a11y a11y-panel__reset" aria-pressed="true" data-label-on="{a11y_on}" data-label-off="{a11y_off}"><span class="ico" aria-hidden="true">👁</span><span> {a11y_off}</span></button>
  </div>
</div>

<div class="topbar">
  <div class="container">
    <div class="topbar__info">
      <span><span class="ico" aria-hidden="true">📞</span> <a href="tel:{tel}">{S["phone"]}</a></span>
      <span><span class="ico" aria-hidden="true">✉</span> <a href="mailto:{S["email"]}">{S["email"]}</a></span>
      <span><span class="ico" aria-hidden="true">🕘</span> {S["hours_short"]}</span>
    </div>
    <div class="topbar__tools">
      <nav class="lang-switch" aria-label="{L("Язык", "Language", "Хэл")}">{langs}</nav>
      <button type="button" class="btn-a11y" aria-pressed="false" data-label-on="{a11y_on}" data-label-off="{a11y_off}"><span class="ico" aria-hidden="true">👁</span><span> {a11y_on}</span></button>
    </div>
  </div>
</div>

<header class="header">
  <div class="container">
    <a class="brand" href="{p}index.html">
      <img class="brand__logo" src="{top}assets/img/logo-256.png" width="56" height="56" alt="">
      <span class="brand__name">{S["short"]}<small>{S["city"]}</small></span>
    </a>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false">☰ {L("Меню", "Menu", "Цэс")}</button>
    <nav class="nav" id="main-nav" aria-label="{L("Основное меню", "Main menu", "Үндсэн цэс")}">
      <ul>
{nav}
      </ul>
    </nav>
    <a class="btn btn--primary btn--sm header__cta" href="https://e-mongolia.mn/news/n/8642" rel="noopener">{L("Участвовать", "Participate", "Оролцох")}</a>
  </div>
</header>

<main id="main">{head_block}
{body}
</main>

<footer class="footer">
  <div class="container">
   <div class="footer__panel">
    <div class="footer__grid">
      <div>
        <a class="brand" href="{p}index.html">
          <img class="brand__logo" src="{top}assets/img/logo-256.png" width="56" height="56" alt="">
          <span class="brand__name">{S["short"]}<small>{S["city"]}</small></span>
        </a>
        <p>{S["full"]}</p>
      </div>
      <div>
        <h3>{L("Контакты", "Contacts", "Холбоо барих")}</h3>
        <ul>
          <li>{S["address"]}</li>
          <li><a href="tel:{tel}">{S["phone"]}</a></li>
          <li><a href="mailto:{S["email"]}">{S["email"]}</a></li>
        </ul>
      </div>
      <div>
        <h3>{L("Разделы", "Sections", "Хэсгүүд")}</h3>
        <ul>
          <li><a href="{p}sveden/index.html">{L("Сведения об образовательной организации", "About the School", "Сургуулийн тухай мэдээлэл")}</a></li>
          <li><a href="{p}sveden/document/index.html">{sveden_names()[2]}</a></li>
          <li><a href="{p}sveden/vacant/index.html">{L("Вакантные места", "Vacancies", "Сул орон тоо")}</a></li>
          <li><a href="{p}sveden/catering/index.html">{L("Питание", "School meals", "Хоол хүнс")}</a></li>
          <li><a href="{p}contacts.html">{L("Контакты", "Contacts", "Холбоо барих")}</a></li>
        </ul>
      </div>
      <div>
        <h3>{L("Полезные ссылки", "Useful links", "Хэрэгцээт холбоос")}</h3>
        <ul>
          <li><a href="https://edu.gov.ru/" rel="noopener">{L("Минпросвещения России", "Ministry of Education of Russia", "ОХУ-ын Гэгээрлийн яам")}</a></li>
          <li><a href="https://obrnadzor.gov.ru/" rel="noopener">{L("Рособрнадзор", "Rosobrnadzor", "Рособрнадзор")}</a></li>
          <li><a href="https://www.gosuslugi.ru/" rel="noopener">{L("Госуслуги", "Gosuslugi (public services)", "Госуслуги (төрийн үйлчилгээ)")}</a></li>
          <li><a href="https://myschool.edu.ru/" rel="noopener">{L("ФГИС «Моя школа»", "“My School” platform", "«Моя школа» платформ")}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {S["short"]}, 2026. {L("Все права защищены.", "All rights reserved.", "Бүх эрх хуулиар хамгаалагдсан.")}</span>
      <span><a href="{top}docs/privacy-policy.pdf">{L("Политика обработки персональных данных", "Personal data policy", "Хувийн мэдээлэл боловсруулах бодлого")}</a></span>
    </div>
   </div>
  </div>
</footer>
<script src="{top}assets/js/main.js?v={asset_ver("assets/js/main.js")}"></script>
</body>
</html>
"""


def sveden_page(idx, body):
    slug, names = SVEDEN_SLUGS[idx], sveden_names()
    name = names[idx]
    side = "\n".join(
        f'        <li><a href="../{s}/index.html"{" aria-current=\"page\"" if s == slug else ""}>{n}</a></li>'
        for s, n in zip(SVEDEN_SLUGS, names)
    )
    inner = f"""
  <div class="container layout">
    <aside>
      <nav class="sidenav" aria-label="{L("Подразделы", "Subsections", "Дэд хэсгүүд")}">
        <div class="sidenav__title">{L("Сведения об ОО", "About the School", "Сургуулийн тухай")}</div>
        <ol>
{side}
        </ol>
      </nav>
    </aside>
    <article class="content">
{note(slug)}
{body}
    </article>
  </div>"""
    return layout(name, inner, f"sveden/{slug}/index.html", current="sveden",
                  crumbs=[(L("Главная", "Home", "Нүүр"), "index.html"),
                          (L("Сведения об образовательной организации", "About the School", "Сургуулийн тухай мэдээлэл"), "sveden/index.html"),
                          (name, None)])


# Подразделы, уже заполненные реальными данными со старого сайта
REAL_DATA = {"common", "struct", "document", "eduStandarts", "managers", "employees"}


def note(slug=""):
    if CUR == "ru" and slug in REAL_DATA:
        return ""
    return L(
        '<p class="note">Шаблон: замените примерные данные на сведения вашей организации. Атрибуты <code>itemprop</code> не удаляйте — по ним Рособрнадзор проводит автоматический мониторинг сайта.</p>',
        '<p class="note">This is a translation for information purposes. The official version of this information is the <a href="../../../sveden/index.html">Russian version</a>. Documents are provided in Russian.</p>',
        '<p class="note">Энэ нь мэдээллийн зорилготой орчуулга юм. Албан ёсны хувилбар нь <a href="../../../sveden/index.html">орос хэл дээрх хувилбар</a>. Баримт бичгүүд орос хэл дээр байна.</p>',
    )


def kv(rows):
    """rows: [(label, value, itemprop|None)]"""
    tr = "\n".join(f'        <tr><th scope="row">{l}</th><td{ip(p)}>{v}</td></tr>' for l, v, p in rows)
    return f'<div class="table-wrap"><table class="kv"><tbody>\n{tr}\n      </tbody></table></div>'


def table(head, rows, row_prop=None):
    th = "".join(f"<th>{h[0]}</th>" for h in head)
    body = "".join(
        f'<tr{ip(row_prop)}>' + "".join(f"<td{ip(h[1])}>{v}</td>" for h, v in zip(head, r)) + "</tr>"
        for r in rows
    )
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def docs(items):
    """items: [(title, file, itemprop|None)] — путь к docs/ от страницы подраздела"""
    up = "../../" if CUR == "ru" else "../../../"
    sig = L("✓ подписан ЭП", "✓ e-signed", "✓ цахим гарын үсэгтэй")
    li = "\n".join(
        f'        <li><a href="{up}docs/{f}"{ip(p)}><span class="ext">PDF</span>{t}<span class="sig">{sig}</span></a></li>'
        for t, f, p in items
    )
    return f'<ul class="doc-list">\n{li}\n      </ul>'


_MAP_FILE = Path(__file__).resolve().parent / "docs_map.json"
DOCS_MAP = json.loads(_MAP_FILE.read_text(encoding="utf-8")) if _MAP_FILE.exists() else {}  # URL → docs/… (fetch_docs.py)


def ext_docs(items, prop=None):
    """items: [(title, url)]. Если файл скачан в docs/ (tools/fetch_docs.py) — ссылка на него
    и встроенный просмотр PDF; иначе — внешняя ссылка на старое хранилище."""
    up = "../../" if CUR == "ru" else "../../../"
    view = L("Просмотр", "Preview", "Харах")
    rows = []
    for t, u in items:
        local = DOCS_MAP.get(u)
        if DOCS_MAP and not local and "cloud.mail.ru" in u:
            # ссылка в облаке удалена (404 при переносе) — показываем без ссылки
            gone = L("файл недоступен", "file unavailable", "файл байхгүй")
            rows.append(f'        <li><span class="doc-missing"><span class="ext">—</span>{t} <small>({gone})</small></span></li>')
            continue
        href = up + local if local else u
        ext = Path(local or u).suffix.lower()
        kind = {".pdf": "PDF", ".doc": "DOC", ".docx": "DOC"}.get(ext, "URL")
        a = f'<a href="{href}"{ip(prop)} rel="noopener" target="_blank"><span class="ext">{kind}</span>{t}</a>'
        if local and kind == "PDF":
            a += (f'<details class="doc-preview"><summary>{view}</summary>'
                  f'<iframe src="{href}#view=FitH" loading="lazy" title="{t}"></iframe></details>')
        rows.append(f"        <li>{a}</li>")
    return '<ul class="doc-list">\n' + "\n".join(rows) + "\n      </ul>"


def old_group(section, title):
    return next((g[1] for g in OLD[section] if g[0] == title), [])


def h2(ru, en, mn):
    return f"<h2>{L(ru, en, mn)}</h2>"


# ------------------------------------------------------------------ sveden pages
def page_common():
    S = school()
    return f"""
      {h2("Общая информация", "General information", "Ерөнхий мэдээлэл")}
      {kv([
        (L("Полное наименование", "Full name", "Бүтэн нэр"), S["full"], "fullName"),
        (L("Сокращённое наименование", "Short name", "Товч нэр"), S["short_full"], "shortName"),
        (L("Дата создания", "Date of foundation", "Байгуулагдсан огноо"), S["regdate"], "regDate"),
        (L("Место нахождения (адрес)", "Address", "Хаяг"), S["address"], "address"),
        (L("Режим и график работы", "Working hours", "Ажлын цаг"), S["hours"], "workTime"),
        (L("Контактный телефон", "Phone", "Утас"), S["phone"], "telephone"),
        (L("Адрес электронной почты", "E-mail", "И-мэйл"), f'<a href="mailto:{S["email"]}">{S["email"]}</a>', "email"),
        (L("Места осуществления образовательной деятельности", "Places of educational activity", "Сургалт явуулдаг байршил"), S["address"], "addressPlaceSet"),
        (L("Языки образования", "Languages of instruction", "Сургалтын хэл"), S["languages"], "language"),
        (L("Места проведения ГИА", "State final exam venue", "Улсын төгсөлтийн шалгалт авах газар"), S["address"], None),
        (L("Филиалы", "Branches", "Салбар"), L("Филиалов нет", "None", "Байхгүй"), "filInfo"),
        (L("Представительства", "Representative offices", "Төлөөлөгчийн газар"), L("Представительств нет", "None", "Байхгүй"), "repInfo"),
      ])}
      {h2("Учредитель", "Founder", "Үүсгэн байгуулагч")}
      <div{ip("uchredLaw")}>
      {kv([
        (L("Наименование учредителя", "Founder", "Үүсгэн байгуулагчийн нэр"),
         L("ПГС «Предприятие Эрдэнэт»", "Erdenet Mining Corporation (state-owned)", "«Эрдэнэт үйлдвэр» ТӨҮГ"), "nameUchred"),
        (L("Сайт", "Website", "Вэбсайт"), '<a href="https://www.erdenetmc.mn" rel="noopener">www.erdenetmc.mn</a>', "websiteUchred"),
      ])}
      </div>
      {h2("Лицензия", "License", "Тусгай зөвшөөрөл")}
      {ext_docs([(L("Лицензия на образовательную деятельность", "Educational license", "Боловсролын үйл ажиллагааны тусгай зөвшөөрөл"), u)
                 for t, u in old_group("documents", "Правоустанавливающие документы") if t == "Лицензия"], "licenseDocLink")}
"""


def page_struct():
    S = school()
    up = "../../" if CUR == "ru" else "../../../"
    reg = L("Положение", "Regulations", "Журам")
    unit = {"Директор школы": L("Администрация", "Administration", "Захиргаа"),
            "Ведущий менеджер": L("Администрация", "Administration", "Захиргаа"),
            "Заместитель директора по учебно-воспитательной работе": L("Учебная часть", "Academic office", "Сургалтын алба")}
    pol = next((u for t, u in old_group("documents", "Правоустанавливающие документы") if t.startswith("Положение о деятельности")), "#")
    pol = up + DOCS_MAP[pol] if pol in DOCS_MAP else pol
    rows = [(unit[m["post"]], fio(m["fio"]), tr(POSTS, m["post"]), S["address"],
             f'<a href="mailto:{m["email"]}">{m["email"]}</a>', f'<a href="{pol}" rel="noopener" target="_blank">{reg}</a>')
            for m in OLD["managers"]]
    gov = [
        L("Общее собрание работников", "General Staff Meeting", "Ажилтнуудын нэгдсэн хурал"),
        L("Педагогический совет", "Teachers' Council", "Багш нарын зөвлөл"),
        L("Управляющий совет", "Governing Board", "Удирдах зөвлөл"),
        L("Совет обучающихся", "Student Council", "Сурагчдын зөвлөл"),
    ]
    gov_html = "\n".join(
        f'<li><a href="{up}docs/organ.pdf"{ip("structOrgUprav")}><span class="ext">PDF</span><span{ip("name")}>{n}</span> — {reg.lower()}<span class="sig">✓</span></a></li>'
        for n in gov
    )
    head = [(L("Наименование", "Unit", "Нэгж"), "name"), (L("Руководитель", "Head", "Удирдагч"), "fio"),
            (L("Должность", "Position", "Албан тушаал"), "post"), (L("Адрес", "Address", "Хаяг"), "addressStr"),
            ("E-mail", "email"), (reg, "divisionClauseDocLink")]
    return f"""
      {h2("Структурные подразделения", "Structural units", "Бүтцийн нэгжүүд")}
      {table(head, rows, "structOrgUprav")}
      {h2("Органы управления", "Governing bodies", "Удирдлагын байгууллагууд")}
      <ul class="doc-list">{gov_html}</ul>
"""


def page_document():
    heads = [
        ("Правоустанавливающие документы", L("Правоустанавливающие документы", "Founding documents", "Үүсгэн байгуулах баримт бичиг"), "ustavDocLink"),
        ("Локальные акты", L("Локальные нормативные акты", "Internal regulations", "Дотоод журам"), "localActStud"),
        ("Прием в школу", L("Приём в школу", "Admission", "Элсэлт"), "localActStud"),
        ("Шаблон документов", L("Шаблоны заявлений", "Application templates", "Өргөдлийн загвар"), None),
        ("ФГОС и ГОС", L("Образовательные стандарты", "Educational standards", "Боловсролын стандарт"), None),
    ]
    return "".join(f"""
      <h2>{title}</h2>
      {ext_docs(old_group("documents", key), prop)}""" for key, title, prop in heads)


def page_education():
    lv = [L("Начальное общее образование", "Primary general education", "Бага боловсрол"),
          L("Основное общее образование", "Basic general education", "Суурь боловсрол"),
          L("Среднее общее образование", "Secondary general education", "Бүрэн дунд боловсрол")]
    full_time = L("Очная", "Full-time", "Өдрийн")
    progs = [
        ("—", L("ООП начального общего образования", "Primary education programme", "Бага боловсролын хөтөлбөр"), lv[0], full_time, L("4 года", "4 years", "4 жил"), "—"),
        ("—", L("ООП основного общего образования", "Basic education programme", "Суурь боловсролын хөтөлбөр"), lv[1], full_time, L("5 лет", "5 years", "5 жил"), "—"),
        ("—", L("ООП среднего общего образования", "Secondary education programme", "Бүрэн дунд боловсролын хөтөлбөр"), lv[2], full_time, L("2 года", "2 years", "2 жил"), "—"),
    ]
    groups = [("НАЧАЛЬНОЕ ОБЩЕЕ ОБРАЗОВАНИЕ", lv[0]), ("ОСНОВНОЕ ОБЩЕЕ ОБРАЗОВАНИЕ", lv[1]), ("СРЕДЕЕ ОБЩЕЕ ОБРАЗОВАНИЕ", lv[2])]
    prog_docs = "".join(f"""
      <h3>{name}</h3>
      {ext_docs(old_group("education", key), "educationRpd")}""" for key, name in groups)
    exams = ext_docs([(L(f"Расписание {t} в 2026 году", f"{t} exam schedule, 2026", f"{t} шалгалтын хуваарь, 2026"), u)
                      for t, u in old_group("education", "Расписание экзаменов")])
    numbers = [(lv[0], "320", "0", "320", "0", "0"), (lv[1], "410", "0", "410", "0", "0"), (lv[2], "95", "0", "95", "0", "0")]
    return f"""
      {h2("Реализуемые образовательные программы", "Educational programmes", "Хэрэгжүүлж буй хөтөлбөрүүд")}
      {table([(L("Код", "Code", "Код"), "eduCode"), (L("Программа", "Programme", "Хөтөлбөр"), "eduName"), (L("Уровень", "Level", "Түвшин"), "eduLevel"),
              (L("Форма обучения", "Mode of study", "Сургалтын хэлбэр"), "eduForm"), (L("Нормативный срок", "Duration", "Хугацаа"), "learningTerm"),
              (L("Срок действия аккредитации", "Accreditation valid until", "Магадлан итгэмжлэлийн хугацаа"), "dateEnd")], progs, "eduAccred")}
      {h2("Учебные планы и рабочие программы", "Curricula and syllabi", "Сургалтын төлөвлөгөө, хөтөлбөрүүд")}
{prog_docs}
      {h2("Расписание экзаменов", "Exam schedule", "Шалгалтын хуваарь")}
      {exams}
      {h2("Численность обучающихся", "Number of students", "Суралцагчдын тоо")}
      {table([(L("Уровень", "Level", "Түвшин"), "eduLevel"), (L("Всего", "Total", "Нийт"), "numberAll"),
              (L("Федеральный бюджет", "Federal budget", "Холбооны төсөв"), "numberBF"), (L("Бюджет субъекта", "Regional budget", "Бүсийн төсөв"), "numberBR"),
              (L("Местный бюджет", "Local budget", "Орон нутгийн төсөв"), "numberBM"), (L("По договорам", "Fee-paying", "Гэрээгээр"), "numberP")], numbers, "eduChislen")}
      {h2("Язык образования", "Language of instruction", "Сургалтын хэл")}
      {kv([(L("Язык обучения", "Language", "Хэл"), school()["languages"], "language")])}
"""


def page_eduStandarts():
    items = [
        ("https://fgos.ru/fgos/fgos-noo/", L("ФГОС начального общего образования (Приказ № 286 от 31.05.2021)", "Federal standard for primary education (Order No. 286, 31.05.2021)", "Бага боловсролын холбооны стандарт (2021.05.31-ний № 286 тушаал)")),
        ("https://fgos.ru/fgos/fgos-ooo/", L("ФГОС основного общего образования (Приказ № 287 от 31.05.2021)", "Federal standard for basic education (Order No. 287, 31.05.2021)", "Суурь боловсролын холбооны стандарт (2021.05.31-ний № 287 тушаал)")),
        ("https://fgos.ru/fgos/fgos-soo/", L("ФГОС среднего общего образования (Приказ № 413 от 17.05.2012)", "Federal standard for secondary education (Order No. 413, 17.05.2012)", "Бүрэн дунд боловсролын холбооны стандарт (2012.05.17-ны № 413 тушаал)")),
        ("https://edsoo.ru/", L("Федеральные образовательные программы (ФОП)", "Federal educational programmes", "Холбооны боловсролын хөтөлбөрүүд")),
    ]
    li = "".join(f'<li><a href="{u}"{ip("eduFedDoc")} rel="noopener"><span class="ext">URL</span>{t}</a></li>' for u, t in items)
    return f"""
      {h2("Федеральные государственные образовательные стандарты", "Federal State Educational Standards", "Холбооны улсын боловсролын стандарт")}
      <ul class="doc-list">{li}</ul>
      {h2("Образовательные стандарты", "Own standards", "Өөрийн стандарт")}
      <p{ip("eduStandartDoc")}>{L("Самостоятельно устанавливаемые образовательные стандарты не применяются.", "The school does not use its own educational standards.", "Сургууль өөрийн боловсролын стандарт хэрэглэдэггүй.")}</p>
"""


def person(fio, post, rows, prop):
    dl = "".join(f"<dt>{l}</dt><dd{ip(p)}>{v}</dd>" for l, v, p in rows)
    return f"""      <div class="person"{ip(prop)}>
        <div class="person__photo ph ph-light" role="img" aria-label="{L("Фото", "Photo", "Зураг")}: {fio}"></div>
        <div><h3{ip("fio")}>{fio}</h3><div{ip("post")}>{post}</div><dl>{dl}</dl></div>
      </div>"""


def page_managers():
    out = "\n".join(
        person(fio(m["fio"]), tr(POSTS, m["post"]),
               [(L("Телефон", "Phone", "Утас"), phone_fmt(m["phone"]), "telephone"),
                ("E-mail", f'<a href="mailto:{m["email"]}">{m["email"]}</a>', "email")], "rucovodstvo")
        for m in OLD["managers"]
    )
    return h2("Руководитель и заместители", "Principal and deputies", "Захирал, орлогч нар") + "\n" + out


def pd_html(pd):
    """Курсы повышения квалификации — по одному в строке (разбиваем после «…, 2023 г.»)."""
    if not pd:
        return "—"
    parts = re.split(r"(?<=\d{4} г\.)\s+(?=\S)|(?<=\d{4}г\.)\s+(?=\S)|(?<=\d{4} год\.)\s+(?=\S)|(?<=\d{4} год)\s+(?=[«“\"А-ЯЁ])", pd)
    return "<br>".join(x.strip() for x in parts if x.strip())


def page_employees():
    ru = CUR == "ru"
    rows = []
    for t in OLD["teachers"]:
        r = [fio(t["fio"]), tr(POSTS, t["post"])]
        if ru:
            r.append(t.get("subjects") or "—")
        r += [tr(LEVELS, t.get("level", "")), (t.get("spec") or "—").strip("«»"), tr(CATEGORIES, t.get("category", "")).replace(" квалификационная категория", ""), "—",
              pd_html(t.get("pd")), t.get("exp") or "—"]
        rows.append(tuple(r))
    head = [(L("ФИО", "Name", "Овог нэр"), "fio"), (L("Должность", "Position", "Албан тушаал"), "post")]
    if ru:
        head.append(("Преподаваемые дисциплины", "teachingDiscipline"))
    head += [(L("Образование", "Education", "Боловсрол"), "teachingLevel"), (L("Специальность", "Specialisation", "Мэргэжил"), "teachingQual"),
             (L("Категория", "Category", "Зэрэглэл"), "qualification"), (L("Учёная степень", "Degree", "Эрдмийн зэрэг"), "degree"),
             (L("Повышение квалификации", "Professional development", "Мэргэжил дээшлүүлэлт"), "profDevelopment"),
             (L("Стаж, лет", "Experience, years", "Ажилласан жил"), "specExperience")]
    n = len(OLD["teachers"])
    lead = L(f"Всего педагогических работников: {n}.",
             f"{n} teachers in total. Specialisation and professional development are given as in the original Russian records.",
             f"Нийт {n} багш. Мэргэжил, мэргэжил дээшлүүлэлтийн мэдээллийг эх хувиар нь (орос хэлээр) өгөв.")
    staff = table(head, rows, "teachingStaff").replace('<div class="table-wrap">', '<div class="table-wrap table-wrap--staff">', 1)
    return h2("Педагогические работники", "Teachers", "Багш нар") + f"\n      <p>{lead}</p>\n      " + staff


def page_objects():
    return f"""
      {h2("Материально-техническое обеспечение", "Facilities", "Материаллаг-техникийн хангамж")}
      {kv([
        (L("Учебные кабинеты", "Classrooms", "Анги танхим"), L("32 кабинета, в т.ч. 3 кабинета информатики, лаборатории физики, химии, биологии; центр «Точка роста»",
          "32 classrooms including 3 computer labs and physics, chemistry and biology labs; “Growth Point” centre",
          "32 анги танхим, үүнд 3 мэдээлэл зүйн кабинет, физик, хими, биологийн лаборатори; «Точка роста» төв"), "purposeCab"),
        (L("Библиотека", "Library", "Номын сан"), L("Читальный зал на 30 мест, фонд — 25 000 экз.", "Reading room for 30, collection of 25,000 items", "30 суудалтай уншлагын танхим, 25 000 ширхэг ном"), "purposeLibr"),
        (L("Объекты спорта", "Sports facilities", "Спортын байгууламж"), L("2 спортивных зала, стадион, тренажёрный зал", "2 gyms, stadium, fitness room", "2 спорт заал, цэнгэлдэх, фитнес танхим"), "purposeSport"),
        (L("Средства обучения", "Learning equipment", "Сургалтын хэрэгсэл"), L("Интерактивные панели, ноутбуки, цифровые лаборатории, 3D-принтеры", "Interactive panels, laptops, digital labs, 3D printers", "Интерактив самбар, зөөврийн компьютер, дижитал лаборатори, 3D принтер"), "meansTraining"),
        (L("Доступ к сети Интернет", "Internet access", "Интернэт холболт"), L("100 Мбит/с, контентная фильтрация", "100 Mbit/s with content filtering", "100 Мбит/с, агуулгын шүүлтүүртэй"), "comNet"),
      ])}
      {h2("Доступная среда", "Accessible environment", "Хүртээмжтэй орчин")}
      {kv([
        (L("Специально оборудованные кабинеты", "Specially equipped rooms", "Тусгайлан тоноглосон өрөө"), L("Кабинет психолога и логопеда, сенсорная комната", "Psychologist and speech therapist rooms, sensory room", "Сэтгэл зүйч, хэл заслын өрөө, мэдрэхүйн өрөө"), "purposeCabOvz"),
        (L("Доступ в здание", "Building access", "Байранд нэвтрэх"), L("Пандус, кнопка вызова, тактильная плитка, мнемосхема", "Ramp, call button, tactile paving, tactile map", "Налуу зам, дуудлагын товч, мэдрэхүйн хавтан, мнемосхем"), "ovz"),
        (L("Электронные ресурсы для лиц с ОВЗ", "Accessible e-resources", "Хөгжлийн бэрхшээлтэй хүмүүст зориулсан цахим нөөц"), L("Версия сайта для слабовидящих (ГОСТ Р 52872-2019)", "Low vision version of the website", "Вэбсайтын хараа муу хүмүүст зориулсан хувилбар"), "erListOvz"),
      ])}
"""


def page_paid_edu():
    return h2("Платные образовательные услуги", "Paid services", "Төлбөртэй үйлчилгээ") + "\n      " + docs([
        (L("Положение о порядке оказания платных образовательных услуг", "Regulations on paid educational services", "Төлбөртэй боловсролын үйлчилгээ үзүүлэх журам"), "paid-polozhenie.pdf", "paidEdu"),
        (L("Образец договора", "Sample contract", "Гэрээний загвар"), "paid-dogovor.pdf", "paidDog"),
        (L("Документ об утверждении стоимости обучения", "Approved tuition fees", "Сургалтын төлбөр баталсан баримт"), "paid-stoimost.pdf", "paidSt"),
    ])


def page_budget():
    rub = L(" руб.", " RUB", " рубль")
    return f"""
      {h2("Объём образовательной деятельности", "Funding of educational activities", "Боловсролын үйл ажиллагааны санхүүжилт")}
      {kv([
        (L("Федеральный бюджет", "Federal budget", "Холбооны төсөв"), "0" + rub, "finBFVolume"),
        (L("Бюджет субъекта РФ", "Regional budget", "Бүсийн төсөв"), "85 400 000" + rub, "finBRVolume"),
        (L("Местный бюджет", "Local budget", "Орон нутгийн төсөв"), "12 300 000" + rub, "finBMVolume"),
        (L("По договорам", "Fee-paying contracts", "Гэрээгээр"), "1 200 000" + rub, "finPVolume"),
      ])}
      {h2("Документы", "Documents", "Баримт бичиг")}
      {docs([
        (L("План финансово-хозяйственной деятельности на 2026 год", "2026 financial plan", "2026 оны санхүү, аж ахуйн төлөвлөгөө"), "pfhd-2026.pdf", "finPlanDocLink"),
        (L("Поступление и расходование средств за 2025 год", "2025 income and expenditure report", "2025 оны орлого, зарлагын тайлан"), "finrec-2025.pdf", "finRec"),
      ])}
"""


def page_vacant():
    grade = L("{} класс", "Grade {}", "{}-р анги")
    data = [("1", 0, "4"), ("2", 0, "1"), ("5", 1, "3"), ("7", 1, "0"), ("10", 2, "6")]
    lv = [L("Начальное общее", "Primary", "Бага"), L("Основное общее", "Basic", "Суурь"), L("Среднее общее", "Secondary", "Бүрэн дунд")]
    rows = [(grade.format(g), lv[l], L("Очная", "Full-time", "Өдрийн"), v, "0", "0", "0") for g, l, v in data]
    head = [(L("Класс", "Grade", "Анги"), "eduCode"), (L("Уровень", "Level", "Түвшин"), "eduLevel"), (L("Форма", "Mode", "Хэлбэр"), "eduForm"),
            (L("Бюджет субъекта", "Regional budget", "Бүсийн төсөв"), "numberBRVacant"), (L("Федеральный бюджет", "Federal budget", "Холбооны төсөв"), "numberBFVacant"),
            (L("Местный бюджет", "Local budget", "Орон нутгийн төсөв"), "numberBMVacant"), (L("По договорам", "Fee-paying", "Гэрээгээр"), "numberPVacant")]
    return h2("Количество вакантных мест (на 01.11.2026)", "Vacant places (as of 1 November 2026)", "Сул орон тоо (2026.11.01-ний байдлаар)") + "\n      " + table(head, rows, "vacant")


def page_grants():
    return kv([
        (L("Стипендии", "Scholarships", "Тэтгэлэг"), L("Не предусмотрены", "Not provided", "Олгодоггүй"), "grant"),
        (L("Меры социальной поддержки", "Student support", "Нийгмийн дэмжлэг"),
         L("Бесплатное горячее питание для 1–4 классов и льготных категорий; бесплатный подвоз; бесплатные учебники",
           "Free hot meals for grades 1–4 and eligible students; free school transport; free textbooks",
           "1–4-р анги болон хөнгөлөлттэй ангиллын сурагчдад үнэгүй халуун хоол; үнэгүй тээвэр; үнэгүй сурах бичиг"), "support"),
        (L("Общежитие, интернат", "Dormitory", "Дотуур байр"), L("Не предусмотрено", "Not available", "Байхгүй"), "hostelInfo"),
    ])


def page_inter():
    return kv([
        (L("Договоры с иностранными организациями", "Agreements with foreign organisations", "Гадаадын байгууллагатай байгуулсан гэрээ"), L("Договоров нет", "None", "Байхгүй"), "internationalDog"),
        (L("Международная аккредитация", "International accreditation", "Олон улсын магадлан итгэмжлэл"), L("Нет", "None", "Байхгүй"), "intAccreditation"),
    ])


def page_catering():
    return f"""
      {h2("Условия питания", "Catering", "Хоол хүнсний нөхцөл")}
      {kv([
        (L("Столовая", "Canteen", "Цайны газар"), L("Обеденный зал на 220 мест, полный цикл приготовления", "Dining hall for 220 with full-cycle kitchen", "220 суудалтай хоолны танхим, бүрэн циклийн гал тогоо"), "meals"),
        (L("Охрана здоровья", "Health care", "Эрүүл мэнд"), L("Медицинский кабинет", "On-site medical room", "Эмнэлгийн өрөө"), "health"),
        (L("Телефон по вопросам питания", "Meals enquiries", "Хоолны асуудлаарх утас"), school()["phone"], None),
      ])}
      {h2("Документы по питанию", "Documents", "Баримт бичиг")}
      {docs([
        (L("Примерное цикличное меню", "Cyclic menu", "Мөчлөгт цэс"), "menu-cikl.pdf", None),
        (L("Положение об организации питания", "Catering regulations", "Хоол хүнсний журам"), "pitanie-polozhenie.pdf", None),
      ])}
      <p>{L("Ежедневные меню размещаются в каталоге <code>/food/</code> в формате XLSX (МР 2.4.0179-20).",
            "Daily menus are published in the <code>/food/</code> folder (XLSX).",
            "Өдөр тутмын цэсийг <code>/food/</code> хавтсанд XLSX хэлбэрээр байршуулдаг.")}</p>
"""


PAGES = [page_common, page_struct, page_document, page_education, page_eduStandarts, page_managers,
         page_employees, page_objects, page_paid_edu, page_budget, page_vacant, page_grants, page_inter, page_catering]


# ------------------------------------------------------------------ home, index, contacts
def photo(name, top):
    """Если в assets/img/ лежит файл (напр. tile-1.jpg) — подставляем его как фон."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        if (ROOT / "assets" / "img" / f"{name}.{ext}").exists():
            return f' style="--img:url(\'{top}assets/img/{name}.{ext}\')"'
    return ""


def home():
    S, names = school(), sveden_names()
    top = "" if CUR == "ru" else "../"
    tiles = [
        ("sveden/index.html", L("Сведения об образовательной организации", "About the School", "Сургуулийн тухай мэдээлэл"), L("14 подразделов", "14 subsections", "14 дэд хэсэг")),
        ("index.html#news", L("Новости и события", "News and events", "Мэдээ, үйл явдал"), L("Жизнь школы", "School life", "Сургуулийн амьдрал")),
        ("index.html#parents", L("Родителям и ученикам", "For parents and students", "Эцэг эх, сурагчдад"), L("Полезное", "Useful", "Хэрэгтэй")),
        ("sveden/catering/index.html", L("Питание", "School meals", "Хоол хүнс"), L("Меню", "Menu", "Цэс")),
    ]
    tiles_html = "\n".join(
        f'        <a class="tile ph ph-{i + 1}" href="{h}"{photo(f"tile-{i + 1}", top)}><h3>{t}</h3><span class="tile__chip">{c}</span></a>'
        for i, (h, t, c) in enumerate(tiles)
    )
    sv_cards = "\n".join(
        f'        <a class="card" href="sveden/{s}/index.html"><span class="card__icon" aria-hidden="true">{ICONS[i]}</span><h3>{names[i]}</h3><p>/sveden/{s}</p></a>'
        for i, s in enumerate(SVEDEN_SLUGS[:8])
    )
    news_tr = {
        "Результаты соревнований": ("Pioneerball tournament results for grade 6", "6-р ангийн «Пионербол»-ын тэмцээний дүн"),
        "Участие в III Международных": ("Taking part in the 3rd International Engineering Competition", "III Олон улсын инженерийн тэмцээнд оролцлоо"),
        "Онлайн-зачет": ("Online financial literacy test", "Санхүүгийн боловсролын онлайн шалгалт"),
        "Интеллектуальная игра": ("“BioMatius” quiz game for grade 11", "11-р ангийн «БиоМатиус» оюуны тоглоом"),
        "День открытых дверей": ("School Open Day", "Сургуулийн нээлттэй хаалганы өдөр"),
        "Участие в международном турнире": ("“Power of Mind” international tournament", "«Оюуны хүч» олон улсын тэмцээнд оролцлоо"),
        "День самоуправления": ("Student Self-Government Day", "Сурагчдын өөрөө удирдах өдөр"),
        "Выборы президента": ("School No. 19 elects its student president", "19-р сургуулийн сурагчдын ерөнхийлөгчийн сонгууль боллоо"),
    }
    news = []
    for n in OLD["news"][:6]:
        en, mn = next((v for k, v in news_tr.items() if n["title"].startswith(k)), (n["title"], n["title"]))
        text = n["text"][len(n["title"]):].strip() if n["text"].startswith(n["title"]) else n["text"]
        text = (text[:160].rsplit(" ", 1)[0] + "…") if len(text) > 160 else text
        y, m, d = n["date"].split("-")
        news.append((f"{d}.{m}.{y}", L(n["title"].rstrip("."), en, mn), L(text, "", "")))
    news_html = "\n".join(
        f'        <article class="card news-card"><h3>{t}</h3>' + (f'<p>{x}</p>' if x else '') + f'<div class="card__date">{d}</div></article>'
        for d, t, x in news
    )
    body = f"""
  <section class="hero">
    <div class="container hero__top">
      <div>
        <h1>{S["short"]}</h1>
        <p class="lead">{L("Современная школа, где каждый ученик раскрывает свои способности",
                            "A modern school where every student discovers their talents",
                            "Сурагч бүр авьяас чадвараа нээх орчин үеийн сургууль")}</p>
      </div>
      <div class="hero-pill">
        <p>{L("Чемпионат по баскетболу",
              "Basketball championship",
              "Сагсан бөмбөгийн аварга шалгаруулах тэмцээн")} <span class="ico" aria-hidden="true">🏀</span></p>
        <a class="btn btn--primary btn--sm" href="https://e-mongolia.mn/news/n/8642" rel="noopener">{L("Участвовать", "Participate", "Оролцох")}</a>
      </div>
    </div>
    <div class="container" style="margin-top:2.2rem">
      <div class="tiles">
{tiles_html}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="promo">
        <div class="promo__img ph ph-light"{photo("promo", top)} role="img" aria-label="{L("Фото школы", "School photo", "Сургуулийн зураг")}"></div>
        <div class="promo__body">
          <h2>{L("Сведения об образовательной организации", "About the School", "Сургуулийн тухай мэдээлэл")}</h2>
          <p>{L("Вся официальная информация о школе в соответствии с Приказом Рособрнадзора № 1493: документы, образовательные программы, педагогический состав, питание, вакантные места и многое другое.",
                "All official information about the school under Rosobrnadzor Order No. 1493: documents, programmes, teaching staff, meals, vacancies and more.",
                "Рособрнадзорын № 1493 тушаалын дагуу сургуулийн албан ёсны бүх мэдээлэл: баримт бичиг, хөтөлбөр, багшийн бүрэлдэхүүн, хоол хүнс, сул орон тоо гэх мэт.")}</p>
          <a class="btn btn--primary" href="sveden/index.html">{L("Перейти в раздел", "Open section", "Хэсэг рүү орох")}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="grid grid--4">
{sv_cards}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="promo promo--reverse">
        <div class="promo__img ph ph-light"{photo("about", top)} role="img" aria-label="{L("Фото педагогов", "Teachers photo", "Багш нарын зураг")}"></div>
        <div class="promo__body">
          <h2>{L("Наша школа", "Our school", "Манай сургууль")}</h2>
          <p>{L("Школа – это особый мир, мир изумительный и необычный. С 1974 года мы даём начальное, основное и среднее общее образование на русском и монгольском языках.",
                "School is a special world, wonderful and unusual. Since 1974 we have provided primary, basic and secondary education in Russian and Mongolian.",
                "Сургууль бол гайхамшигтай, онцгой ертөнц. 1974 оноос хойш бага, суурь, бүрэн дунд боловсролыг орос, монгол хэлээр олгож байна.")}</p>
          <div class="stats">
            <div><b>{len(OLD["teachers"])}</b><span>{L("педагогов", "teachers", "багш")}</span></div>
            <div><b>{len(OLD["managers"])}</b><span>{L("в администрации", "administrators", "удирдлага")}</span></div>
            <div><b>2</b><span>{L("языка обучения", "languages of instruction", "сургалтын хэл")}</span></div>
            <div><b>1974</b><span>{L("год основания", "founded", "байгуулагдсан")}</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="news">
    <div class="container">
      <div class="section__head"><h2>{L("Новости", "News", "Мэдээ")}</h2><a class="btn btn--ghost" href="index.html#news">{L("Все новости", "All news", "Бүх мэдээ")}</a></div>
      <div class="grid grid--3">
{news_html}
      </div>
    </div>
  </section>

  <section class="section" id="parents">
    <div class="container">
      <div class="section__head"><h2>{L("Родителям и ученикам", "For parents and students", "Эцэг эх, сурагчдад")}</h2></div>
      <div class="grid grid--4">
        <a class="card" href="https://e-mongolia.mn/news/n/8642" rel="noopener"><span class="card__icon" aria-hidden="true">📝</span><h3>{L("Запись в 1-й класс", "Grade 1 enrolment", "1-р ангид бүртгүүлэх")}</h3><p>{L("Заявление через E-Mongolia", "Apply via E-Mongolia", "E-Mongolia-гаар өргөдөл гаргах")}</p></a>
        <a class="card" href="https://myschool.edu.ru/" rel="noopener"><span class="card__icon" aria-hidden="true">📚</span><h3>{L("Электронный дневник", "Electronic diary", "Цахим өдрийн тэмдэглэл")}</h3><p>{L("ФГИС «Моя школа»", "“My School” platform", "«Моя школа» платформ")}</p></a>
        <a class="card" href="sveden/catering/index.html"><span class="card__icon" aria-hidden="true">🍎</span><h3>{L("Меню питания", "Menu", "Хоолны цэс")}</h3><p>{L("Ежедневное меню столовой", "Daily canteen menu", "Өдөр тутмын цэс")}</p></a>
        <a class="card" href="sveden/vacant/index.html"><span class="card__icon" aria-hidden="true">🪑</span><h3>{L("Свободные места", "Vacant places", "Сул орон тоо")}</h3><p>{L("Вакантные места для приёма", "Places available for admission", "Элсэлтийн сул орон тоо")}</p></a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <!-- Замените этот блок на виджет ПОС Госуслуг (код — в кабинете pos.gosuslugi.ru) -->
      <div class="pos-banner" id="pos-widget">
        <div>
          <h2>{L("Есть вопрос или предложение?", "Have a question or suggestion?", "Асуулт, санал байна уу?")}</h2>
          <p>{L("Напишите нам через платформу обратной связи Госуслуг — мы ответим в установленный срок.",
                "Write to us via the Gosuslugi feedback platform and we will reply within the official deadline.",
                "Госуслуги-ийн санал хүсэлтийн платформоор бидэнд бичээрэй, тогтоосон хугацаанд хариу өгнө.")}</p>
        </div>
        <div>
          <a class="btn btn--primary" href="https://pos.gosuslugi.ru/" rel="noopener">{L("Написать обращение", "Send a request", "Өргөдөл илгээх")}</a>
          <small>{L("Для отправки потребуется подтверждённая учётная запись Госуслуг", "A verified Gosuslugi account is required", "Баталгаажсан Госуслуги бүртгэл шаардлагатай")}</small>
        </div>
      </div>
    </div>
  </section>
"""
    return layout(L("Главная", "Home", "Нүүр"), body, "index.html", current="home")


def sveden_index():
    names = sveden_names()
    cards = "\n".join(
        f'        <a class="card" href="{s}/index.html"><span class="card__icon" aria-hidden="true">{ICONS[i]}</span><h3>{i + 1}. {names[i]}</h3><p>/sveden/{s}</p></a>'
        for i, s in enumerate(SVEDEN_SLUGS)
    )
    intro = L(
        "Раздел сформирован в соответствии с Приказом Рособрнадзора от 04.08.2023 № 1493 «Об утверждении Требований к структуре официального сайта образовательной организации в информационно-телекоммуникационной сети «Интернет» и формату представления информации».",
        'This section follows Rosobrnadzor Order No. 1493 of 4 August 2023. The official version is in <a href="../../sveden/index.html">Russian</a>.',
        'Энэ хэсгийг Рособрнадзорын 2023.08.04-ний № 1493 тушаалын дагуу бүрдүүлсэн. Албан ёсны хувилбар нь <a href="../../sveden/index.html">орос хэл дээр</a>.',
    )
    title = L("Сведения об образовательной организации", "About the School", "Сургуулийн тухай мэдээлэл")
    body = f"""
  <section class="section">
    <div class="container">
      <p class="note">{intro}</p>
      <div class="grid grid--3">
{cards}
      </div>
    </div>
  </section>"""
    return layout(title, body, "sveden/index.html", current="sveden",
                  crumbs=[(L("Главная", "Home", "Нүүр"), "index.html"), (title, None)])


# ------------------------------------------------------------------ образовательные материалы (ЭИОС)
EBOOKS = [
    ("Школа фей", "Барбара Розу", "docs/ebooks/shkola-fey.pdf"),
    ("Сказки для самых маленьких", "С. Маршак", "docs/ebooks/skazki-dlya-samykh-malenkikh.pdf"),
    ("Школьники-детективы", "Александр Калинина", "docs/ebooks/shkolniki-detektivy.pdf"),
]

EIOS_RESOURCES = [
    ("https://resh.edu.ru/", L("Российская электронная школа", "Russian Electronic School", "Оросын цахим сургууль"),
     L("Интерактивные уроки по всему школьному курсу с 1 по 11 класс от лучших учителей страны. Уроки соответствуют ФГОС; задания даны по типу экзаменационных тестов и подходят для подготовки к ОГЭ и ЕГЭ.",
       "Interactive lessons covering the whole school curriculum for grades 1–11, aligned with the federal standards; exercises follow the OGE/EGE exam format.",
       "1–11-р ангийн бүх хичээлийн интерактив хичээлүүд. Холбооны стандартад нийцсэн, ОГЭ, ЕГЭ шалгалтад бэлтгэх даалгавартай.")),
    ("http://school-collection.edu.ru/", L("Единая коллекция цифровых образовательных ресурсов", "Unified Collection of Digital Educational Resources", "Цахим боловсролын нөөцийн нэгдсэн сан"),
     L("Цифровые образовательные ресурсы, методические материалы, тематические коллекции и инструменты для поддержки учебной деятельности.",
       "Digital learning resources, teaching materials, thematic collections and tools to support learning.",
       "Цахим сургалтын нөөц, арга зүйн материал, сэдэвчилсэн цуглуулга, сургалтыг дэмжих хэрэгслүүд.")),
    ("https://sbooks.gnpbu.ru/", L("Электронная библиотека учебников", "Electronic textbook library", "Сурах бичгийн цахим номын сан"),
     L("Российское образование: электронные версии учебников.", "Russian education: electronic versions of textbooks.", "Сурах бичгүүдийн цахим хувилбар.")),
    ("https://uchi.ru/", "Учи.ру", L("Онлайн-платформа, где ученики изучают школьные предметы в интерактивной форме; здесь же проводятся предметные олимпиады.",
                                      "An online platform for learning school subjects interactively, with subject olympiads.",
                                      "Хичээлүүдийг интерактив хэлбэрээр судлах онлайн платформ, хичээлийн олимпиадтай.")),
    ("https://www.yaklass.ru/", "ЯКласс", L("Тестирование знаний и домашние задания в электронном виде; для ученика — электронные рабочие тетради и тренажёр по школьной программе.",
                                              "Online tests and homework; electronic workbooks and practice for students.",
                                              "Цахим шалгалт, гэрийн даалгавар; сурагчдад зориулсан цахим дасгалын дэвтэр.")),
    ("https://educont.ru/", L("Цифровой образовательный контент", "Digital Educational Content", "Цахим боловсролын контент"),
     L("Бесплатный доступ к образовательным онлайн-платформам для школьников и учителей.", "Free access to online learning platforms for students and teachers.",
       "Сурагч, багш нарт онлайн сургалтын платформыг үнэгүй ашиглах боломж.")),
]

EIOS_LINKS = [
    (L("Онлайн-обучение", "Online learning", "Онлайн сургалт"), [
        ("http://math-ege.sdamgia.ru/", "math-ege.sdamgia.ru", L("подготовка к ЕГЭ и ОГЭ", "OGE/EGE exam practice", "ОГЭ, ЕГЭ-д бэлтгэх")),
        ("http://childrenscience.ru/", "childrenscience.ru", L("курсы по школьной программе", "school curriculum courses", "сургуулийн хөтөлбөрийн сургалт")),
    ]),
    (L("Лингвистика", "Languages and literature", "Хэл, уран зохиол"), [
        ("http://vsrussian.com/", "vsrussian.com", L("весёлый и увлекательный способ изучать русский язык", "a fun way to learn Russian", "орос хэлийг сонирхолтой сурах")),
        ("http://briefly.ru/", "briefly.ru", L("2000 произведений школьной программы в кратком изложении", "2,000 school-curriculum works in summary", "сургуулийн хөтөлбөрийн 2000 зохиолын товчлол")),
        ("http://lingualeo.com/", "lingualeo.com", L("интерактивный сервис для изучения английского языка", "interactive English learning", "англи хэлийг интерактив сурах")),
        ("http://gostei.ru/", "gostei.ru", L("детская библиотека: программные произведения по литературе для 1–11 классов", "children's library of curriculum literature, grades 1–11", "1–11-р ангийн уран зохиолын хүүхдийн номын сан")),
        ("http://gramota.ru/", "gramota.ru", L("справочный портал по правилам русского языка", "Russian language reference portal", "орос хэлний дүрмийн лавлах")),
        ("http://itra.ru/", "itra.ru", L("биографии писателей, краткие содержания и тексты произведений", "author biographies, summaries and full texts", "зохиолчдын намтар, товчлол, бүрэн эх")),
        ("http://bibliotekar.ru/", "bibliotekar.ru", L("электронная библиотека нехудожественной литературы", "non-fiction e-library", "уран бус зохиолын цахим номын сан")),
    ]),
]


def materials():
    top = "../" if CUR == "ru" else "../../"
    view = L("Просмотр", "Preview", "Харах")
    title = L("Образовательные материалы", "Learning Materials", "Сургалтын материал")
    intro = L(
        "Электронная информационно-образовательная среда школы (ЭИОС) — совокупность электронных информационных и образовательных ресурсов, технологий и средств, обеспечивающих освоение обучающимися образовательных программ начального общего, основного общего и среднего общего образования.",
        "The school's electronic learning environment brings together digital information and learning resources, technologies and tools that support students in primary, basic and secondary education.",
        "Сургуулийн цахим сургалтын орчин нь бага, суурь, бүрэн дунд боловсролын хөтөлбөрийг эзэмшихэд туслах цахим мэдээлэл, сургалтын нөөц, технологи, хэрэгслийн цогц юм.")
    provides = [
        L("доступ к учебным планам, рабочим программам, изданиям электронных библиотек и электронным образовательным ресурсам;",
          "access to curricula, syllabi, e-libraries and digital learning resources;",
          "сургалтын төлөвлөгөө, хөтөлбөр, цахим номын сан, цахим сургалтын нөөцөд хандах;"),
        L("фиксацию хода образовательного процесса, результатов текущей и промежуточной аттестации;",
          "recording of learning progress and assessment results;",
          "сургалтын явц, явцын болон завсрын үнэлгээний үр дүнг бүртгэх;"),
        L("формирование электронного портфолио обучающегося;", "electronic student portfolios;", "сурагчийн цахим портфолио бүрдүүлэх;"),
        L("взаимодействие участников образовательного процесса, в том числе через сеть «Интернет»;",
          "communication between students, parents and teachers, including online;",
          "сургалтын оролцогчдын хооронд, тэр дундаа интернэтээр харилцах;"),
        L("проведение занятий с применением электронного обучения и дистанционных образовательных технологий.",
          "e-learning and distance learning.", "цахим болон зайн сургалт явуулах."),
    ]
    res = "\n".join(
        f'        <a class="card" href="{u}" rel="noopener" target="_blank"><h3>{n}</h3><p>{d}</p></a>'
        for u, n, d in EIOS_RESOURCES
    )
    groups = "".join(
        f'\n      <h3>{g}</h3>\n      <ul class="link-list">'
        + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{n}</a> — {d}</li>' for u, n, d in items)
        + "</ul>"
        for g, items in EIOS_LINKS
    )
    books = "\n".join(
        f'        <li><a href="{top}{f}" target="_blank"><span class="ext">PDF</span>«{t}» — {a}</a>'
        f'<details class="doc-preview"><summary>{view}</summary><iframe src="{top}{f}#view=FitH" loading="lazy" title="{t}"></iframe></details></li>'
        for t, a, f in EBOOKS
    )
    body = f"""
  <div class="container" style="padding:2.5rem 0 4rem">
    <p class="lead">{intro}</p>
    {h2("ЭИОС школы обеспечивает", "What the environment provides", "Цахим орчин юу олгодог вэ")}
    <ul>{"".join(f"<li>{x}</li>" for x in provides)}</ul>

    {h2("Электронные образовательные ресурсы", "Digital learning resources", "Цахим сургалтын нөөц")}
    <div class="grid grid--3">
{res}
    </div>
    {groups}

    {h2("Электронные книги", "E-books", "Цахим ном")}
    <p>{L("Детям и родителям", "For children and parents", "Хүүхэд, эцэг эхчүүдэд")}</p>
    <ul class="doc-list">
{books}
    </ul>

    {h2("Учебные планы и рабочие программы", "Curricula and syllabi", "Сургалтын төлөвлөгөө, хөтөлбөр")}
    <p>{L("Учебные планы и рабочие программы по предметам размещены в разделе",
          "Curricula and subject syllabi are published in the section",
          "Сургалтын төлөвлөгөө, хичээлийн хөтөлбөрүүдийг дараах хэсэгт байршуулсан:")}
       <a href="../sveden/education/index.html">{L("«Сведения об образовательной организации» → «Образование»", "About the School → Education", "Сургуулийн тухай → Боловсрол")}</a>.</p>
  </div>"""
    return layout(title, body, "materials/index.html", current="materials",
                  crumbs=[(L("Главная", "Home", "Нүүр"), "index.html"), (title, None)])


def contacts():
    S = school()
    title = L("Контакты", "Contacts", "Холбоо барих")
    body = f"""
  <div class="container" style="padding:2.5rem 0 4rem">
    {kv([
      (L("Адрес", "Address", "Хаяг"), S["address"], "address"),
      (L("Телефон приёмной", "Reception", "Хүлээн авах утас"), S["phone"], "telephone"),
      ("E-mail", f'<a href="mailto:{S["email"]}">{S["email"]}</a>', "email"),
      (L("Режим работы", "Working hours", "Ажлын цаг"), S["hours"], "workTime"),
      (L("Директор", "Principal", "Захирал"), S["director"], None),
    ])}
  </div>"""
    return layout(title, body, "contacts.html", current="contacts",
                  crumbs=[(L("Главная", "Home", "Нүүр"), "index.html"), (title, None)])


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    count = 0
    for code, _, _ in LANGS:
        CUR = code
        base = ROOT if code == "ru" else ROOT / code
        write(base / "index.html", home())
        write(base / "contacts.html", contacts())
        write(base / "materials" / "index.html", materials())
        write(base / "sveden" / "index.html", sveden_index())
        for i, fn in enumerate(PAGES):
            write(base / "sveden" / SVEDEN_SLUGS[i] / "index.html", sveden_page(i, fn()))
        count += 4 + len(PAGES)
        print(f"  ✓ {code}: {4 + len(PAGES)} страниц")
    print(f"Готово: {count} страниц.")
