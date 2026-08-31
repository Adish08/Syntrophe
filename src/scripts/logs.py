# ---------------------------------------------------------
# Copyright (C) 2026 krvstek
# 
# DO NOT REMOVE OR ALTER THIS COPYRIGHT HEADER.
# This file is part of uni-apks.
# Canonical source: https://github.com/krvstek/uni-apks
#
# Licensed under the GNU GPLv3. You may modify this file,
# but you MUST keep this original copyright notice intact
# and prominently state any changes made.
# See the AUTHORS file in the root directory for details.
# ---------------------------------------------------------

import sys
from pathlib import Path

from src.core.logger import IS_GITHUB, abort


def _require_ci(script: str) -> None:
    if not IS_GITHUB:
        abort(f"'{script}' is only available in GitHub Actions")

def _parse_log_file(log: Path, green_lines: list[str], collected: list[str]) -> str:
    microg_line = ""
    lines = [s for ln in log.read_text(encoding="utf-8").splitlines() if (s := ln.strip())]
    for i, line in enumerate(lines):
        if line.startswith("- 🟢"):
            green_lines.append(f"{line}  ")
        elif not microg_line and line.startswith("▶️") and "MicroG" in line:
            microg_line = line
        elif line.startswith("> ⚙️ » CLI:"):
            collected.append(f"{line}  ")
        elif line.startswith("> ⚙️ » Patches:"):
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            collected.append(f"{line}  \n{next_line}  ")
    return microg_line

def combine_logs(logs_dir: Path | str, existing_notes_path: Path | str | None = None) -> None:
    logs = sorted(Path(logs_dir).rglob("build*.md"))
    if not logs and not existing_notes_path:
        return

    apps_map: dict[str, str] = {}
    collected: list[str] = []
    microg_line = ""

    if existing_notes_path and Path(existing_notes_path).is_file():
        try:
            existing_text = Path(existing_notes_path).read_text(encoding="utf-8")
            for line in existing_text.splitlines():
                line_str = line.strip()
                if line_str.startswith("- 🟢 »"):
                    parts = line_str.split(":", 1)
                    app_key = parts[0].replace("- 🟢 »", "").strip()
                    apps_map[app_key] = line_str
                elif not microg_line and line_str.startswith("▶️") and "MicroG" in line_str:
                    microg_line = line_str
        except Exception:
            pass

    new_green: list[str] = []
    for log in logs:
        m_line = _parse_log_file(log, new_green, collected)
        if not microg_line:
            microg_line = m_line

    for line in new_green:
        line_str = line.strip()
        if line_str.startswith("- 🟢 »"):
            parts = line_str.split(":", 1)
            app_key = parts[0].replace("- 🟢 »", "").strip()
            apps_map[app_key] = line_str

    if apps_map:
        sorted_apps = [apps_map[k] for k in sorted(apps_map.keys(), key=lambda s: s.lower())]
        print("\n".join(f"{line}  " for line in sorted_apps), end="\n\n")

    if not microg_line:
        microg_line = "▶️ » Install [MicroG-RE](https://github.com/MorpheApp/MicroG-RE/releases) to enable Google account sign-in for supported apps"
    print(microg_line, end="\n\n")

    if unique := list(dict.fromkeys(collected)):
        print("\n\n".join(unique))

def main() -> None:
    _require_ci("logs.py")
    match sys.argv[1:]:
        case ["combine-logs", logs_dir, existing_notes]:
            combine_logs(logs_dir=Path(logs_dir), existing_notes_path=Path(existing_notes))
        case ["combine-logs", logs_dir]:
            combine_logs(logs_dir=Path(logs_dir))
        case ["combine-logs"]:
            combine_logs(logs_dir=Path("logs"))
        case _:
            abort("Usage: logs.py combine-logs [dir] [existing_notes_file]")

if __name__ == "__main__":
    main()