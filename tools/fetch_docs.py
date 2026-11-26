"""Скачивает документы со старого сайта (облако Mail.ru и wp-content) в docs/.

Запуск: python tools/fetch_docs.py
Результат: файлы в docs/… и карта tools/docs_map.json {исходный URL: локальный путь от корня сайта}.
Уже скачанные файлы повторно не загружаются.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = json.loads((ROOT / "tools" / "oldsite.json").read_text(encoding="utf-8"))
MAP_FILE = ROOT / "tools" / "docs_map.json"
UA = {"User-Agent": "Mozilla/5.0 (school-site-migration)"}

TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
              ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t",
               "u", "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya"]))


def slug(title, limit=60):
    s = "".join(TR.get(c, c) for c in title.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:limit].rstrip("-") or "doc"


def get(url, timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read(), r.headers.get_content_type()


def cloud_download(url):
    """Публичная ссылка cloud.mail.ru/public/XXX/YYY → (bytes, имя файла)."""
    page = get(url, 60)[0].decode("utf-8", "replace")
    base = re.search(r'"weblink_get":\{"count":"\d+","url":"([^"]+)"', page).group(1)
    name = re.search(r'"name":"([^"]+\.[A-Za-z0-9]{2,5})"', page)
    key = url.split("/public/", 1)[1].strip("/")
    data, _ = get(f"{base}/{key}")
    return data, name.group(1) if name else ""


GROUP_DIR = {
    "НАЧАЛЬНОЕ ОБЩЕЕ ОБРАЗОВАНИЕ": "education/noo",
    "ОСНОВНОЕ ОБЩЕЕ ОБРАЗОВАНИЕ": "education/ooo",
    "СРЕДЕЕ ОБЩЕЕ ОБРАЗОВАНИЕ": "education/soo",
    "Расписание экзаменов": "education/exams",
}


def jobs():
    for g, items in OLD["documents"]:
        for t, u in items:
            yield "documents", t, u
    for g, items in OLD["education"]:
        for t, u in items:
            yield GROUP_DIR.get(g, "education"), t, u
    for t, u in OLD["eios"]:
        yield "documents", t, u


def main():
    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8")) if MAP_FILE.exists() else {}
    used = set(mapping.values())
    total, failed = 0, []
    for folder, title, url in jobs():
        if url in mapping and (ROOT / mapping[url]).exists():
            total += (ROOT / mapping[url]).stat().st_size
            continue
        if "cloud.mail.ru" not in url and "wp-content/uploads" not in url:
            continue
        try:
            if "cloud.mail.ru" in url:
                data, name = cloud_download(url)
            else:
                data, _ = get(urllib.parse.quote(url, safe=":/?=&%"))
                name = urllib.parse.unquote(url.rsplit("/", 1)[1])
            ext = Path(name).suffix.lower() or ".pdf"
            base = f"docs/{folder}/{slug(title)}"
            rel, n = base + ext, 2
            while rel in used:
                rel, n = f"{base}-{n}{ext}", n + 1
            path = ROOT / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            mapping[url] = rel
            used.add(rel)
            total += len(data)
            print(f"  ✓ {rel}  ({len(data) / 1e6:.1f} MB)", flush=True)
            MAP_FILE.write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
            time.sleep(0.5)
        except Exception as e:  # noqa: BLE001 — продолжаем остальные файлы
            failed.append((title, url, repr(e)))
            print(f"  ✗ {title}: {e!r}", flush=True)
    print(f"Готово: {len(mapping)} файлов, {total / 1e6:.1f} MB; ошибок: {len(failed)}")
    for f in failed:
        print("   ", *f)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
