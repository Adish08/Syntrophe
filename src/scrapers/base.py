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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

from src.core.network import NetworkManager


def _parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

class ScraperError(Exception):
    """Raised for scraper-layer failures: DOM parsing, regex mismatches, missing assets"""

@dataclass(slots=True, frozen=True)
class AppMetadata:
    pkg_name: str
    versions: list[str]

@dataclass(slots=True, frozen=True)
class DownloadResult:
    path: Path
    is_bundle: bool = False

class BaseScraper(ABC):
    def __init__(self, net: NetworkManager) -> None:
        self.net = net
        self._cache: dict[str, AppMetadata] = {}

    def cached_metadata(self, url: str) -> AppMetadata:
        if url not in self._cache:
            self._cache[url] = self.fetch_metadata(url)
        return self._cache[url]

    @abstractmethod
    def fetch_metadata(self, url: str) -> AppMetadata:
        pass

    @abstractmethod
    def download(self, url: str, version: str, dest: Path, arch: str, dpi: str, version_code: str | None = None) -> DownloadResult:
        pass


class UptodownError(ScraperError):
    pass

class UptodownScraper(BaseScraper):
    def __init__(self, net: NetworkManager) -> None:
        super().__init__(net)
        self._versions_cache: dict[str, str] = {}

    def fetch_metadata(self, url: str) -> AppMetadata:
        import re
        clean_url = url.rstrip("/").removesuffix("/download").rstrip("/")
        versions_html = self.net.get(f"{clean_url}/versions")
        self._versions_cache[clean_url] = versions_html
        
        soup_ver = _parse_html(versions_html)
        pkg_name = ""
        
        try:
            dl_page = self.net.get(f"{clean_url}/download")
            soup_dl = _parse_html(dl_page)
            th = soup_dl.find("th", string=re.compile(r"Package\s*Name", re.I))
            if th and (td := th.find_next_sibling("td")):
                pkg_name = td.get_text(strip=True)
        except Exception:
            pass

        if not pkg_name:
            try:
                main_html = self.net.get(clean_url)
                soup_main = _parse_html(main_html)
                th = soup_main.find("th", string=re.compile(r"Package\s*Name", re.I))
                if th and (td := th.find_next_sibling("td")):
                    pkg_name = td.get_text(strip=True)
            except Exception:
                pass

        if not pkg_name:
            slug = clean_url.split("//", 1)[-1].split(".", 1)[0]
            if "ibispaint" in slug:
                pkg_name = "jp.ne.ibis.ibispaintx.app"
            else:
                pkg_name = slug

        versions = [text for el in soup_ver.select(".version") if (text := el.get_text(strip=True))]
        return AppMetadata(pkg_name=pkg_name, versions=versions or ["latest"])

    def download(self, url: str, version: str, dest: Path, arch: str, dpi: str, version_code: str | None = None) -> DownloadResult:
        clean_url = url.rstrip("/").removesuffix("/download").rstrip("/")
        dl_page = self.net.get(f"{clean_url}/download")
        soup_dl = _parse_html(dl_page)
        
        btn = soup_dl.select_one("#detail-download-button, a.button.download")
        if btn and btn.get("data-url"):
            data_url = btn["data-url"]
            final_dl_url = f"https://dw.uptodown.com/dwn/{data_url}"
        elif btn and btn.get("href"):
            final_dl_url = btn["href"]
        else:
            raise UptodownError(f"Could not find download URL on '{clean_url}/download'")

        self.net.download(final_dl_url, dest)
        return DownloadResult(path=dest, is_bundle=False)