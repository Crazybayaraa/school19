# -*- coding: utf-8 -*-
"""
Генератор статических страниц сайта школы.
Запуск:  python tools/build.py
Создаёт index.html, contacts.html и раздел /sveden/ (14 подразделов)
по Приказу Рособрнадзора № 1493 от 04.08.2023.

Данные школы меняйте в словаре SCHOOL ниже, содержимое подразделов —
в функциях page_*(). После правки снова запустите скрипт.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCHOOL = {
    "full": "Муниципальное бюджетное общеобразовательное учреждение «Средняя общеобразовательная школа № 1»",
    "short": "МБОУ «СОШ № 1»",
    "abbr": "1",
    "city": "г. Примерск",
    "address": "123456, Российская Федерация, Примерская область, г. Примерск, ул. Школьная, д. 1",
    "phone": "+7 (000) 000-00-00",
    "email": "school1@example.ru",
    "hours": "Пн–Пт: 08:00–18:00, Сб: 08:00–14:00, Вс: выходной",
    "regdate": "01.09.1975",
    "director": "Иванова Мария Петровна",
}

# (slug, название подраздела) — порядок и адреса строго по Приказу № 1493
SVEDEN = [
    ("common", "Основные сведения"),
    ("struct", "Структура и органы управления образовательной организацией"),
    ("document", "Документы"),
    ("education", "Образование"),
    ("eduStandarts", "Образовательные стандарты и требования"),
    ("managers", "Руководство"),
    ("employees", "Педагогический состав"),
    ("objects", "Материально-техническое обеспечение и оснащённость образовательного процесса. Доступная среда"),
    ("paid_edu", "Платные образовательные услуги"),
    ("budget", "Финансово-хозяйственная деятельность"),
    ("vacant", "Вакантные места для приёма (перевода) обучающихся"),
    ("grants", "Стипендии и меры поддержки обучающихся"),
    ("inter", "Международное сотрудничество"),
    ("catering", "Организация питания в образовательной организации"),
]

ICONS = ["🏫", "🗂️", "📄", "🎓", "📘", "👤", "👩‍🏫", "🧪", "💳", "📊", "🪑", "🎖️", "🌍", "🍎"]


# ------------------------------------------------------------------ layout
def layout(title, body, depth=0, current="", crumbs=None):
    p = "../" * depth
    nav_items = [
        ("index.html", "Главная", "home"),
        ("sveden/index.html", "Сведения об ОО", "sveden"),
        ("index.html#news", "Новости", "news"),
        ("index.html#parents", "Родителям", "parents"),
        ("contacts.html", "Контакты", "contacts"),
    ]
    nav = "\n".join(
        f'        <li><a href="{p}{href}"{" aria-current=\"page\"" if key == current else ""}>{label}</a></li>'
        for href, label, key in nav_items
    )
    crumbs_html = ""
    if crumbs:
        items = "".join(
            f'<li><a href="{p}{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>'
            for t, h in crumbs
        )
        crumbs_html = f'<nav class="breadcrumbs" aria-label="Хлебные крошки"><ol>{items}</ol></nav>'

    head_block = ""
    if crumbs is not None:
        head_block = f"""
  <section class="page-head">
    <div class="container">
      {crumbs_html}
      <h1>{title}</h1>
    </div>
  </section>"""

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {SCHOOL["short"]}</title>
  <meta name="description" content="Официальный сайт {SCHOOL["short"]}, {SCHOOL["city"]}">
  <link rel="stylesheet" href="{p}assets/css/style.css">
  <script>try{{var s=JSON.parse(localStorage.getItem('a11y-settings'));if(s&&s.on)document.documentElement.classList.add('a11y')}}catch(e){{}}</script>
</head>
<body>
<a class="skip-link" href="#main">Перейти к содержимому</a>

<div class="a11y-panel" role="region" aria-label="Настройки версии для слабовидящих">
  <div class="container">
    <fieldset><legend>Размер шрифта:</legend>
      <button type="button" data-a11y-set="fs:1">А</button>
      <button type="button" data-a11y-set="fs:2" style="font-size:1.2em">А</button>
      <button type="button" data-a11y-set="fs:3" style="font-size:1.4em">А</button>
    </fieldset>
    <fieldset><legend>Цвет:</legend>
      <button type="button" data-a11y-set="scheme:wb" aria-label="Чёрным по белому">Ц</button>
      <button type="button" class="scheme-bw" data-a11y-set="scheme:bw" aria-label="Белым по чёрному">Ц</button>
      <button type="button" class="scheme-blue" data-a11y-set="scheme:blue" aria-label="Тёмно-синим по голубому">Ц</button>
      <button type="button" class="scheme-beige" data-a11y-set="scheme:beige" aria-label="Коричневым по бежевому">Ц</button>
    </fieldset>
    <fieldset><legend>Изображения:</legend>
      <button type="button" data-a11y-set="noimg:false">Вкл</button>
      <button type="button" data-a11y-set="noimg:true">Выкл</button>
    </fieldset>
    <fieldset><legend>Интервал:</legend>
      <button type="button" data-a11y-set="ls:false">Обычный</button>
      <button type="button" data-a11y-set="ls:true">Большой</button>
    </fieldset>
  </div>
</div>

<div class="topbar">
  <div class="container">
    <div class="topbar__info">
      <span>📞 <a href="tel:{SCHOOL["phone"].replace(" ", "").replace("(", "").replace(")", "").replace("-", "")}">{SCHOOL["phone"]}</a></span>
      <span>✉ <a href="mailto:{SCHOOL["email"]}">{SCHOOL["email"]}</a></span>
      <span>🕘 {SCHOOL["hours"]}</span>
    </div>
    <button type="button" class="btn-a11y" aria-pressed="false"><span aria-hidden="true">👁</span><span> Версия для слабовидящих</span></button>
  </div>
</div>

<header class="header">
  <div class="container">
    <a class="brand" href="{p}index.html">
      <span class="brand__logo" aria-hidden="true">№{SCHOOL["abbr"]}</span>
      <span class="brand__name">{SCHOOL["short"]}<small>{SCHOOL["city"]}</small></span>
    </a>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false">☰ Меню</button>
    <nav class="nav" id="main-nav" aria-label="Основное меню">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>

<main id="main">{head_block}
{body}
</main>

<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <h3>{SCHOOL["short"]}</h3>
        <p>{SCHOOL["full"]}</p>
        <p>{SCHOOL["address"]}<br>Тел.: {SCHOOL["phone"]} · E-mail: <a href="mailto:{SCHOOL["email"]}">{SCHOOL["email"]}</a></p>
      </div>
      <div>
        <h3>Разделы</h3>
        <ul>
          <li><a href="{p}sveden/index.html">Сведения об образовательной организации</a></li>
          <li><a href="{p}sveden/document/index.html">Документы</a></li>
          <li><a href="{p}sveden/vacant/index.html">Вакантные места</a></li>
          <li><a href="{p}sveden/catering/index.html">Питание</a></li>
          <li><a href="{p}contacts.html">Контакты</a></li>
        </ul>
      </div>
      <div>
        <h3>Полезные ссылки</h3>
        <ul>
          <li><a href="https://edu.gov.ru/" rel="noopener">Минпросвещения России</a></li>
          <li><a href="https://obrnadzor.gov.ru/" rel="noopener">Рособрнадзор</a></li>
          <li><a href="https://www.gosuslugi.ru/" rel="noopener">Госуслуги</a></li>
          <li><a href="https://fgis.gosuslugi.ru/" rel="noopener">ФГИС «Моя школа»</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {SCHOOL["short"]}, 2026. Все права защищены.</span>
      <span><a href="{p}docs/privacy-policy.pdf">Политика обработки персональных данных</a></span>
    </div>
  </div>
</footer>
<script src="{p}assets/js/main.js"></script>
</body>
</html>
"""


def sveden_page(idx, body):
    slug, name = SVEDEN[idx]
    side = "\n".join(
        f'        <li><a href="../{s}/index.html"{" aria-current=\"page\"" if s == slug else ""}>{n}</a></li>'
        for s, n in SVEDEN
    )
    inner = f"""
  <div class="container layout">
    <aside>
      <nav class="sidenav" aria-label="Подразделы">
        <div class="sidenav__title">Сведения об ОО</div>
        <ol>
{side}
        </ol>
      </nav>
    </aside>
    <article class="content">
{body}
    </article>
  </div>"""
    return layout(
        name, inner, depth=2, current="sveden",
        crumbs=[("Главная", "index.html"), ("Сведения об образовательной организации", "sveden/index.html"), (name, None)],
    )


def kv(rows):
    """rows: [(label, value, itemprop|None)]"""
    tr = "\n".join(
        f'        <tr><th scope="row">{l}</th><td{f" itemprop=\"{ip}\"" if ip else ""}>{v}</td></tr>'
        for l, v, ip in rows
    )
    return f'<div class="table-wrap"><table class="kv"><tbody>\n{tr}\n      </tbody></table></div>'


def table(head, rows, row_prop=None):
    th = "".join(f"<th>{h[0]}</th>" for h in head)
    body = []
    for r in rows:
        tds = "".join(
            f'<td{f" itemprop=\"{h[1]}\"" if h[1] else ""}>{v}</td>' for h, v in zip(head, r)
        )
        body.append(f'<tr{f" itemprop=\"{row_prop}\"" if row_prop else ""}>{tds}</tr>')
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def docs(items):
    """items: [(title, file, itemprop|None)] — документы с ЭП"""
    li = "\n".join(
        f'        <li><a href="../../docs/{f}"{f" itemprop=\"{ip}\"" if ip else ""}><span class="ext">PDF</span>{t}<span class="sig">✓ подписан ЭП</span></a></li>'
        for t, f, ip in items
    )
    return f'<ul class="doc-list">\n{li}\n      </ul>'


NOTE = '<p class="note">Шаблон: замените примерные данные на сведения вашей организации. Атрибуты <code>itemprop</code> не удаляйте — по ним Рособрнадзор проводит автоматический мониторинг сайта.</p>'


# ------------------------------------------------------------------ sveden pages
def page_common():
    return NOTE + f"""
      <h2>Общая информация</h2>
      {kv([
        ("Полное наименование", SCHOOL["full"], "fullName"),
        ("Сокращённое наименование", SCHOOL["short"], "shortName"),
        ("Дата создания", SCHOOL["regdate"], "regDate"),
        ("Место нахождения (адрес)", SCHOOL["address"], "address"),
        ("Режим и график работы", SCHOOL["hours"], "workTime"),
        ("Контактный телефон", SCHOOL["phone"], "telephone"),
        ("Адрес электронной почты", f'<a href="mailto:{SCHOOL["email"]}">{SCHOOL["email"]}</a>', "email"),
        ("Места осуществления образовательной деятельности", SCHOOL["address"], "addressPlaceSet"),
        ("Филиалы", "Филиалов нет", "filInfo"),
        ("Представительства", "Представительств нет", "repInfo"),
      ])}
      <h2>Учредитель</h2>
      <div itemprop="uchredLaw">
      {kv([
        ("Наименование учредителя", "Администрация городского округа «Город Примерск»", "nameUchred"),
        ("Адрес", "123456, г. Примерск, пл. Ленина, д. 1", "addressUchred"),
        ("Телефон", "+7 (000) 000-00-01", "telUchred"),
        ("E-mail", "adm@example.ru", "mailUchred"),
        ("Сайт", '<a href="https://example.ru">example.ru</a>', "websiteUchred"),
      ])}
      </div>
      <h2>Лицензия и аккредитация</h2>
      {kv([
        ("Лицензия на образовательную деятельность", "№ Л035-00000-00/00000000 от 01.01.2016 (выписка из реестра лицензий)", "licenseDocLink"),
        ("Государственная аккредитация", "№ А007-00000-00/00000000 от 01.01.2019", "accreditationDocLink"),
      ])}
"""


def page_struct():
    rows = [
        ("Администрация", "Иванова Мария Петровна", "Директор", SCHOOL["address"], SCHOOL["email"], "Положение"),
        ("Учебная часть", "Петрова Анна Сергеевна", "Заместитель директора по УВР", SCHOOL["address"], "uvr@example.ru", "Положение"),
        ("Библиотека", "Сидорова Ольга Ивановна", "Заведующий библиотекой", SCHOOL["address"], "lib@example.ru", "Положение"),
    ]
    rows = [r[:5] + (f'<a href="../../docs/polozhenie.pdf">{r[5]}</a>',) for r in rows]
    gov = [
        ("Общее собрание работников", "Положение об общем собрании"),
        ("Педагогический совет", "Положение о педагогическом совете"),
        ("Управляющий совет", "Положение об управляющем совете"),
        ("Совет обучающихся", "Положение о совете обучающихся"),
    ]
    gov_html = "\n".join(
        f'<li><a href="../../docs/organ.pdf" itemprop="structOrgUprav"><span class="ext">PDF</span><span itemprop="name">{n}</span> — {d}<span class="sig">✓ ЭП</span></a></li>'
        for n, d in gov
    )
    return NOTE + f"""
      <h2>Структурные подразделения</h2>
      {table([("Наименование", "name"), ("Руководитель", "fio"), ("Должность", "post"), ("Адрес", "addressStr"), ("E-mail", "email"), ("Положение", "divisionClauseDocLink")], rows, "structOrgUprav")}
      <h2>Органы управления</h2>
      <ul class="doc-list">{gov_html}</ul>
"""


def page_document():
    return NOTE + "\n      <h2>Основные документы</h2>\n      " + docs([
        ("Устав образовательной организации", "ustav.pdf", "ustavDocLink"),
        ("Правила внутреннего распорядка обучающихся", "pravila-obuch.pdf", "localActStud"),
        ("Правила внутреннего трудового распорядка", "pravila-trud.pdf", "localActOrder"),
        ("Коллективный договор", "koldogovor.pdf", "localActCollec"),
        ("Отчёт о результатах самообследования", "samoobsl.pdf", "reportEduDocLink"),
        ("Предписания органов госконтроля и отчёты об их исполнении", "predpisaniya.pdf", "prescriptionDocLink"),
    ]) + "\n      <h2>Локальные нормативные акты</h2>\n      " + docs([
        ("Правила приёма обучающихся", "priem.pdf", "localActStud"),
        ("Режим занятий обучающихся", "rezhim.pdf", "localActStud"),
        ("Положение о формах, периодичности и порядке текущего контроля и промежуточной аттестации", "attestaciya.pdf", "localActStud"),
        ("Порядок и основания перевода, отчисления и восстановления обучающихся", "perevod.pdf", "localActStud"),
        ("Порядок оформления возникновения, приостановления и прекращения отношений", "otnosheniya.pdf", "localActStud"),
    ])


def page_education():
    progs = [
        ("—", "Основная образовательная программа начального общего образования", "Начальное общее образование", "Очная", "4 года", "01.06.2027"),
        ("—", "Основная образовательная программа основного общего образования", "Основное общее образование", "Очная", "5 лет", "01.06.2027"),
        ("—", "Основная образовательная программа среднего общего образования", "Среднее общее образование", "Очная", "2 года", "01.06.2027"),
    ]
    numbers = [
        ("Начальное общее образование", "320", "320", "0", "0", "0"),
        ("Основное общее образование", "410", "410", "0", "0", "0"),
        ("Среднее общее образование", "95", "95", "0", "0", "0"),
    ]
    return NOTE + f"""
      <h2>Реализуемые образовательные программы</h2>
      {table([("Код", "eduCode"), ("Наименование программы", "eduName"), ("Уровень образования", "eduLevel"), ("Форма обучения", "eduForm"), ("Нормативный срок", "learningTerm"), ("Срок действия аккредитации", "dateEnd")], progs, "eduAccred")}
      <h2>Документы образовательных программ</h2>
      {docs([
        ("ООП НОО (с учебным планом, календарным графиком, рабочими программами)", "oop-noo.pdf", "educationPlan"),
        ("ООП ООО (с учебным планом, календарным графиком, рабочими программами)", "oop-ooo.pdf", "educationPlan"),
        ("ООП СОО (с учебным планом, календарным графиком, рабочими программами)", "oop-soo.pdf", "educationPlan"),
        ("Рабочая программа воспитания и календарный план воспитательной работы", "vospitanie.pdf", "educationRpd"),
      ])}
      <h2>Численность обучающихся</h2>
      {table([("Уровень образования", "eduLevel"), ("Всего", "numberAll"), ("За счёт бюджета РФ", "numberBF"), ("За счёт бюджета субъекта", "numberBR"), ("За счёт местного бюджета", "numberBM"), ("По договорам", "numberP")], numbers, "eduChislen")}
      <h2>Языки образования</h2>
      {kv([("Язык обучения", "Русский", "language")])}
      <h2>Использование ЭО и ДОТ</h2>
      <p>Обучение с применением электронного обучения и дистанционных образовательных технологий осуществляется с использованием ФГИС «Моя школа» и ИКОП «Сферум».</p>
"""


def page_eduStandarts():
    return NOTE + "\n      <h2>Федеральные государственные образовательные стандарты</h2>\n      " + (
        '<ul class="doc-list">'
        '<li><a href="https://fgos.ru/fgos/fgos-noo/" itemprop="eduFedDoc" rel="noopener"><span class="ext">URL</span>ФГОС начального общего образования (Приказ Минпросвещения № 286 от 31.05.2021)</a></li>'
        '<li><a href="https://fgos.ru/fgos/fgos-ooo/" itemprop="eduFedDoc" rel="noopener"><span class="ext">URL</span>ФГОС основного общего образования (Приказ Минпросвещения № 287 от 31.05.2021)</a></li>'
        '<li><a href="https://fgos.ru/fgos/fgos-soo/" itemprop="eduFedDoc" rel="noopener"><span class="ext">URL</span>ФГОС среднего общего образования (Приказ Минобрнауки № 413 от 17.05.2012)</a></li>'
        '<li><a href="https://edsoo.ru/" itemprop="eduFedDoc" rel="noopener"><span class="ext">URL</span>Федеральные образовательные программы (ФОП НОО, ООО, СОО)</a></li>'
        '</ul>'
        '<h2>Образовательные стандарты</h2><p itemprop="eduStandartDoc">Самостоятельно устанавливаемые образовательные стандарты не применяются.</p>'
    )


def person(fio, post, rows):
    dl = "".join(f'<dt>{l}</dt><dd itemprop="{ip}">{v}</dd>' for l, v, ip in rows)
    return f"""      <div class="person" itemprop="{{prop}}">
        <div class="person__photo" role="img" aria-label="Фото: {fio}"></div>
        <div><h3 itemprop="fio">{fio}</h3><div itemprop="post">{post}</div><dl>{dl}</dl></div>
      </div>"""


def page_managers():
    ppl = [
        ("Иванова Мария Петровна", "Директор", "+7 (000) 000-00-00", "director@example.ru"),
        ("Петрова Анна Сергеевна", "Заместитель директора по учебно-воспитательной работе", "+7 (000) 000-00-02", "uvr@example.ru"),
        ("Кузнецов Игорь Владимирович", "Заместитель директора по воспитательной работе", "+7 (000) 000-00-03", "vr@example.ru"),
    ]
    out = "\n".join(
        person(f, p, [("Телефон", t, "telephone"), ("E-mail", e, "email")]).replace("{prop}", "rucovodstvo")
        for f, p, t, e in ppl
    )
    return NOTE + "\n      <h2>Руководитель и заместители</h2>\n" + out


def page_employees():
    rows = [
        ("Смирнова Елена Александровна", "Учитель начальных классов", "Высшее", "Педагог-психолог / учитель начальных классов", "Высшая", "—", "2025 г., «Реализация ФОП НОО», 72 ч.", "18 лет", "ООП НОО"),
        ("Орлов Дмитрий Николаевич", "Учитель математики", "Высшее", "Математика", "Первая", "—", "2024 г., «Методика подготовки к ЕГЭ», 36 ч.", "11 лет", "ООП ООО, ООП СОО"),
        ("Волкова Наталья Сергеевна", "Учитель русского языка и литературы", "Высшее", "Филология", "Высшая", "к.ф.н.", "2025 г., «Обновлённые ФГОС ООО», 72 ч.", "22 года", "ООП ООО, ООП СОО"),
    ]
    head = [("ФИО", "fio"), ("Должность / преподаваемые дисциплины", "post"), ("Образование", "teachingLevel"), ("Направление подготовки / квалификация", "teachingQual"), ("Категория", "qualification"), ("Учёная степень", "degree"), ("Повышение квалификации", "profDevelopment"), ("Стаж", "specExperience"), ("Программы", "teachingOp")]
    return NOTE + "\n      <h2>Педагогические работники</h2>\n      " + table(head, rows, "teachingStaff")


def page_objects():
    return NOTE + f"""
      <h2>Материально-техническое обеспечение</h2>
      {kv([
        ("Учебные кабинеты", "32 кабинета, в т.ч. 3 кабинета информатики, лаборатории физики, химии, биологии; центр «Точка роста»", "purposeCab"),
        ("Библиотека", "Библиотека с читальным залом на 30 мест, фонд — 25 000 экз.", "purposeLibr"),
        ("Объекты спорта", "2 спортивных зала, стадион, тренажёрный зал", "purposeSport"),
        ("Средства обучения и воспитания", "Интерактивные панели, ноутбуки, цифровые лаборатории, 3D-принтеры", "meansTraining"),
        ("Доступ к информационным системам и сетям", "Подключение к ЕСПД, скорость 100 Мбит/с, контентная фильтрация", "comNet"),
        ("Электронные образовательные ресурсы", "ФГИС «Моя школа», «Сферум», Российская электронная школа", "erList"),
      ])}
      <h2>Доступная среда</h2>
      {kv([
        ("Специально оборудованные кабинеты", "Кабинет педагога-психолога и логопеда, сенсорная комната", "purposeCabOvz"),
        ("Обеспечение беспрепятственного доступа в здание", "Пандус, кнопка вызова, тактильная плитка, мнемосхема, расширенные дверные проёмы", "ovz"),
        ("Специальные средства обучения", "Портативные индукционные системы, ПО экранного доступа", "meansTrainingOvz"),
        ("Условия питания и охраны здоровья для лиц с ОВЗ", "Диетическое меню по показаниям, медицинский кабинет", "meansMealsOvz"),
        ("Электронные ресурсы, адаптированные для лиц с ОВЗ", "Сайт имеет версию для слабовидящих (ГОСТ Р 52872-2019)", "erListOvz"),
      ])}
"""


def page_paid_edu():
    return NOTE + "\n      <h2>Документы о платных образовательных услугах</h2>\n      " + docs([
        ("Положение о порядке оказания платных образовательных услуг", "paid-polozhenie.pdf", "paidEdu"),
        ("Образец договора об оказании платных образовательных услуг", "paid-dogovor.pdf", "paidDog"),
        ("Документ об утверждении стоимости обучения", "paid-stoimost.pdf", "paidSt"),
    ])


def page_budget():
    return NOTE + f"""
      <h2>Объём образовательной деятельности</h2>
      {kv([
        ("За счёт бюджета РФ", "0 руб.", "finBFVolume"),
        ("За счёт бюджета субъекта РФ", "85 400 000 руб.", "finBRVolume"),
        ("За счёт местного бюджета", "12 300 000 руб.", "finBMVolume"),
        ("По договорам об оказании платных услуг", "1 200 000 руб.", "finPVolume"),
      ])}
      <h2>Документы</h2>
      {docs([
        ("План финансово-хозяйственной деятельности на 2026 год", "pfhd-2026.pdf", "finPlanDocLink"),
        ("Информация о поступлении и расходовании финансовых и материальных средств за 2025 год", "finrec-2025.pdf", "finRec"),
      ])}
"""


def page_vacant():
    rows = [(f"{c} класс", lvl, "Очная", v, "0", "0", "0") for c, lvl, v in [
        ("1", "Начальное общее", "4"), ("2", "Начальное общее", "1"), ("5", "Основное общее", "3"),
        ("7", "Основное общее", "0"), ("10", "Среднее общее", "6"),
    ]]
    head = [("Класс", "eduCode"), ("Уровень", "eduLevel"), ("Форма", "eduForm"), ("Мест за счёт бюджета субъекта", "numberBRVacant"), ("Федеральный бюджет", "numberBFVacant"), ("Местный бюджет", "numberBMVacant"), ("По договорам", "numberPVacant")]
    return NOTE + '\n      <h2>Количество вакантных мест (на 01.11.2026)</h2>\n      ' + table(head, rows, "vacant")


def page_grants():
    return NOTE + f"""
      {kv([
        ("Условия предоставления стипендий", "Стипендии не предусмотрены", "grant"),
        ("Меры социальной поддержки", "Бесплатное горячее питание для 1–4 классов и льготных категорий; бесплатный подвоз; бесплатные учебники", "support"),
        ("Общежитие, интернат", "Не предусмотрено", "hostelInfo"),
        ("Трудоустройство выпускников", "Информация о поступлении выпускников 9 и 11 классов публикуется ежегодно", "graduateJob"),
      ])}
"""


def page_inter():
    return NOTE + f"""
      {kv([
        ("Заключённые договоры с иностранными организациями", "Договоров нет", "internationalDog"),
        ("Международная аккредитация", "Нет", "intAccreditation"),
      ])}
"""


def page_catering():
    return NOTE + f"""
      <h2>Условия питания</h2>
      {kv([
        ("Столовая", "Обеденный зал на 220 посадочных мест, полный цикл приготовления", "meals"),
        ("Охрана здоровья обучающихся", "Медицинский кабинет, лицензированный медицинский работник по договору с ГБУЗ", "health"),
        ("Горячая линия по питанию", "+7 (000) 000-00-05, министерство просвещения региона", None),
      ])}
      <h2>Документы по питанию</h2>
      {docs([
        ("Примерное цикличное меню", "menu-cikl.pdf", None),
        ("Ежедневное меню (папка food/)", "food-index.pdf", None),
        ("Положение об организации питания обучающихся", "pitanie-polozhenie.pdf", None),
        ("Перечень юридических лиц и ИП, оказывающих услуги по питанию", "postavshiki.pdf", None),
      ])}
      <p>Ежедневные меню размещаются в каталоге <code>/food/</code> в формате XLSX по методическим рекомендациям МР 2.4.0179-20.</p>
"""


PAGES = [page_common, page_struct, page_document, page_education, page_eduStandarts, page_managers,
         page_employees, page_objects, page_paid_edu, page_budget, page_vacant, page_grants, page_inter, page_catering]


# ------------------------------------------------------------------ home & index
def home():
    sv_cards = "\n".join(
        f'        <a class="card" href="sveden/{s}/index.html"><span class="card__icon" aria-hidden="true">{ICONS[i]}</span><h3>{n}</h3></a>'
        for i, (s, n) in enumerate(SVEDEN[:8])
    )
    news = [
        ("20 ноября 2026", "Школьный этап всероссийской олимпиады завершён", "Подведены итоги: 46 учащихся вышли в муниципальный этап."),
        ("14 ноября 2026", "День открытых дверей для будущих первоклассников", "Приглашаем родителей познакомиться с учителями и программами."),
        ("05 ноября 2026", "Новая лаборатория «Точка роста»", "Открыт кабинет робототехники и цифровых лабораторий."),
    ]
    news_html = "\n".join(
        f'        <article class="card"><div class="news-img" role="img" aria-label="Иллюстрация к новости"></div><div class="card__date">{d}</div><h3>{t}</h3><p>{x}</p></article>'
        for d, t, x in news
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <div>
        <span class="hero__eyebrow">Приём в 1-й класс на 2027/2028 учебный год — с 1 апреля</span>
        <h1>{SCHOOL["short"]}</h1>
        <p class="lead">Современная школа, где каждый ученик раскрывает свои способности. Начальное, основное и среднее общее образование в {SCHOOL["city"].replace("г. ", "городе ")}.</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="sveden/index.html">Сведения об образовательной организации</a>
          <a class="btn btn--ghost" href="contacts.html">Контакты</a>
        </div>
      </div>
      <div class="hero__card">
        <div class="hero__stats">
          <div class="stat"><b>825</b><span>обучающихся</span></div>
          <div class="stat"><b>64</b><span>педагога</span></div>
          <div class="stat"><b>50+</b><span>кружков и секций</span></div>
          <div class="stat"><b>1975</b><span>год основания</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head">
        <div><h2>Сведения об образовательной организации</h2><p>Обязательный раздел по Приказу Рособрнадзора № 1493</p></div>
        <a class="btn btn--ghost" href="sveden/index.html">Все 14 подразделов →</a>
      </div>
      <div class="grid grid--4">
{sv_cards}
      </div>
    </div>
  </section>

  <section class="section section--soft" id="news">
    <div class="container">
      <div class="section__head"><h2>Новости</h2></div>
      <div class="grid grid--3">
{news_html}
      </div>
    </div>
  </section>

  <section class="section" id="parents">
    <div class="container">
      <div class="section__head"><h2>Родителям и ученикам</h2></div>
      <div class="grid grid--4">
        <a class="card" href="https://www.gosuslugi.ru/" rel="noopener"><span class="card__icon" aria-hidden="true">📝</span><h3>Запись в 1-й класс</h3><p>Подача заявления через Госуслуги</p></a>
        <a class="card" href="https://myschool.edu.ru/" rel="noopener"><span class="card__icon" aria-hidden="true">📚</span><h3>Электронный дневник</h3><p>ФГИС «Моя школа»</p></a>
        <a class="card" href="sveden/catering/index.html"><span class="card__icon" aria-hidden="true">🍎</span><h3>Меню питания</h3><p>Ежедневное меню столовой</p></a>
        <a class="card" href="sveden/vacant/index.html"><span class="card__icon" aria-hidden="true">🪑</span><h3>Свободные места</h3><p>Вакантные места для приёма</p></a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <!-- Замените этот блок на виджет Платформы обратной связи (ПОС) Госуслуг:
           код выдаётся в личном кабинете организации на pos.gosuslugi.ru -->
      <div class="pos-banner" id="pos-widget">
        <div><h2>Не убедились в ответе? Напишите нам через Госуслуги</h2><p>Платформа обратной связи — обращения, жалобы и предложения</p></div>
        <a class="btn" href="https://pos.gosuslugi.ru/" rel="noopener">Написать обращение</a>
      </div>
    </div>
  </section>
"""
    return layout("Главная", body, depth=0, current="home")


def sveden_index():
    cards = "\n".join(
        f'        <a class="card" href="{s}/index.html"><span class="card__icon" aria-hidden="true">{ICONS[i]}</span><h3>{i + 1}. {n}</h3><p>/sveden/{s}</p></a>'
        for i, (s, n) in enumerate(SVEDEN)
    )
    body = f"""
  <section class="section">
    <div class="container">
      <p class="note">Раздел сформирован в соответствии с Приказом Рособрнадзора от 04.08.2023 № 1493 «Об утверждении Требований к структуре официального сайта образовательной организации в информационно-телекоммуникационной сети «Интернет» и формату представления информации».</p>
      <div class="grid grid--3">
{cards}
      </div>
    </div>
  </section>"""
    return layout("Сведения об образовательной организации", body, depth=1, current="sveden",
                  crumbs=[("Главная", "index.html"), ("Сведения об образовательной организации", None)])


def contacts():
    body = f"""
  <div class="container" style="padding:2.5rem 0 4rem">
    {kv([
      ("Адрес", SCHOOL["address"], "address"),
      ("Телефон приёмной", SCHOOL["phone"], "telephone"),
      ("E-mail", f'<a href="mailto:{SCHOOL["email"]}">{SCHOOL["email"]}</a>', "email"),
      ("Режим работы", SCHOOL["hours"], "workTime"),
      ("Директор", SCHOOL["director"], None),
    ])}
    <p class="note">Сюда можно встроить карту (рекомендуется Яндекс Карты — российский сервис).</p>
  </div>"""
    return layout("Контакты", body, depth=0, current="contacts",
                  crumbs=[("Главная", "index.html"), ("Контакты", None)])


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("  ✓", path.relative_to(ROOT))


if __name__ == "__main__":
    write(ROOT / "index.html", home())
    write(ROOT / "contacts.html", contacts())
    write(ROOT / "sveden" / "index.html", sveden_index())
    for i, fn in enumerate(PAGES):
        write(ROOT / "sveden" / SVEDEN[i][0] / "index.html", sveden_page(i, fn()))
    print("Готово.")
