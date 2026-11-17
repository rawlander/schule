# Kapu – Unterrichtsseiten mit Ablaufdatum

Einfache HTML-Seiten für Schüler:innen, veröffentlicht über GitHub Pages:
`https://rawlander.github.io/schule/`

## So funktioniert es

- Jede Seite liegt in einem eigenen Ordner: `seiten/<name>/index.html`
  → Link: `https://rawlander.github.io/schule/seiten/<name>/`
- Im `<head>` steht das Ablaufdatum (letzter Tag, an dem die Seite online ist):
  `<meta name="ablauf" content="2026-12-20">` und optional `<meta name="kurs" content="EF Informatik">`.
- Der Job `.github/workflows/seiten.yml` läuft bei jeder Änderung und jede Nacht kurz nach Mitternacht.
  Er löscht abgelaufene Seiten (`tools/aufraeumen.py`) und veröffentlicht nur die aktiven.
- Seiten ohne gültiges Ablaufdatum werden nicht veröffentlicht.
- Zusätzlich prüft jede Seite selbst das Datum und zeigt danach nur „Diese Seite ist abgelaufen“.
- `uebersicht.html` zeigt alle aktiven Seiten mit Ablaufdatum und „Link kopieren“.
- Vorlage für neue Seiten: `vorlage/seite.html` (Kapu-Design, Ablauf-Prüfung, PDF-Export für GoodNotes).

## Einmalige Einrichtung

1. Settings → Pages → Source: **GitHub Actions**.
2. Logos aus dem Design System „Kapu Bocholt“ nach `assets/` hochladen:
   `kapu-bildmarke.png` (und optional `kapu-logo.png`). Ohne Logo bleibt der Kopf ohne Bild.

## Wichtig

- Das Repository ist öffentlich: keine Schülernamen, Noten oder Lösungen zu laufenden Klausuren hochladen.
  Gelöschte Seiten bleiben im Änderungsverlauf des Repositorys einsehbar.
- Eingaben der Schüler:innen bleiben im Browser bzw. im exportierten PDF; nichts wird an GitHub gesendet.
- Seite früher entfernen: Ordner löschen oder Ablaufdatum auf gestern setzen.
- Seite verlängern: Ablaufdatum ändern.
- Testen: `python3 tools/aufraeumen.py --heute 2026-12-01 --site /tmp/test` (löscht ohne `--loeschen` nichts).
