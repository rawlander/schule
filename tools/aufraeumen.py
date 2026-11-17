#!/usr/bin/env python3
"""Ablauf-System für GitHub Pages (Repository rawlander/schule).

Jede Schülerseite liegt in seiten/<name>/index.html und trägt im <head>:
    <meta name="ablauf" content="JJJJ-MM-TT">   letzter Tag, an dem sie online ist
    <meta name="kurs"   content="EF Informatik"> optional, für die Übersicht

Das Skript
  1. löscht mit --loeschen alle Seiten, deren Ablaufdatum vor heute (Europe/Berlin) liegt,
  2. schreibt seiten.json (Liste der aktiven Seiten für uebersicht.html),
  3. baut mit --site <ordner> die Website nur aus aktiven Seiten zusammen.
Seiten ohne gültiges Ablaufdatum werden nie veröffentlicht (Warnung), aber auch nicht gelöscht.

Aufruf:  python3 tools/aufraeumen.py [--loeschen] [--site _site] [--heute JJJJ-MM-TT]
"""
import argparse, datetime, html, json, re, shutil, sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SEITEN = ROOT / "seiten"
# Dateien/Ordner im Hauptverzeichnis, die immer veröffentlicht werden
OEFFENTLICH = ["index.html", "uebersicht.html", "robots.txt", ".nojekyll", "assets"]


def meta(text, name):
    for tag in re.findall(r"<meta\b[^>]*>", text, re.I):
        if re.search(r'name\s*=\s*["\']%s["\']' % name, tag, re.I):
            m = re.search(r'content\s*=\s*["\']([^"\']*)["\']', tag, re.I)
            if m:
                return html.unescape(m.group(1)).strip()
    return None


def titel(text, fallback):
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    return html.unescape(m.group(1)).strip() if m else fallback


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loeschen", action="store_true", help="abgelaufene Seiten löschen")
    ap.add_argument("--site", help="Zielordner für die Veröffentlichung")
    ap.add_argument("--heute", help="Datum überschreiben (zum Testen)")
    a = ap.parse_args()

    heute = (datetime.date.fromisoformat(a.heute) if a.heute
             else datetime.datetime.now(ZoneInfo("Europe/Berlin")).date())
    aktiv, abgelaufen, ohne = [], [], []

    for ordner in sorted(p for p in SEITEN.iterdir() if p.is_dir()) if SEITEN.exists() else []:
        datei = ordner / "index.html"
        if not datei.exists():
            continue
        text = datei.read_text(encoding="utf-8", errors="replace")
        roh = meta(text, "ablauf")
        try:
            ablauf = datetime.date.fromisoformat(roh or "")
        except ValueError:
            ohne.append(ordner.name)
            continue
        eintrag = {"ordner": ordner.name, "titel": titel(text, ordner.name),
                   "kurs": meta(text, "kurs") or "", "ablauf": ablauf.isoformat(),
                   "pfad": f"seiten/{ordner.name}/"}
        (abgelaufen if ablauf < heute else aktiv).append(eintrag)

    for e in abgelaufen:
        print(f"abgelaufen: {e['ordner']} (bis {e['ablauf']})")
        if a.loeschen:
            shutil.rmtree(SEITEN / e["ordner"])
    for n in ohne:
        print(f"WARNUNG: seiten/{n}/index.html hat kein gültiges <meta name=\"ablauf\"> – wird nicht veröffentlicht",
              file=sys.stderr)

    aktiv.sort(key=lambda e: (e["ablauf"], e["titel"].lower()))
    daten = {"stand": heute.isoformat(), "seiten": aktiv}
    (ROOT / "seiten.json").write_text(json.dumps(daten, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"aktiv: {len(aktiv)}, abgelaufen: {len(abgelaufen)}, ohne Ablaufdatum: {len(ohne)}")

    if a.site:
        ziel = Path(a.site).resolve()
        if ziel == ROOT or ziel in ROOT.parents or ziel == SEITEN or SEITEN in ziel.parents:
            sys.exit("--site muss ein eigener, neuer Ordner sein (z. B. _site)")
        shutil.rmtree(ziel, ignore_errors=True)
        ziel.mkdir(parents=True)
        for name in OEFFENTLICH:
            q = ROOT / name
            if q.is_dir():
                shutil.copytree(q, ziel / name)
            elif q.exists():
                shutil.copy2(q, ziel / name)
        shutil.copy2(ROOT / "seiten.json", ziel / "seiten.json")
        for e in aktiv:
            shutil.copytree(SEITEN / e["ordner"], ziel / "seiten" / e["ordner"])


if __name__ == "__main__":
    main()
