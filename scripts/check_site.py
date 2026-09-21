from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.rglob("*.html"))
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[tuple[str, str, dict[str, str]]] = []
        self.images: list[dict[str, str]] = []
        self.has_main = False
        self.h1_count = 0
        self.has_description = False
        self.has_viewport = False
        self.has_canonical = False

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k: (v or "") for k, v in attrs_list}
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "main":
            self.has_main = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and attrs.get("name") == "description" and attrs.get("content"):
            self.has_description = True
        if tag == "meta" and attrs.get("name") == "viewport":
            self.has_viewport = True
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.has_canonical = True
        if tag == "img":
            self.images.append(attrs)
        for attr_name in ("href", "src"):
            value = attrs.get(attr_name)
            if value:
                self.links.append((tag, value, attrs))


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def resolve_local(source: Path, raw_url: str) -> tuple[Path | None, str]:
    split = urlsplit(raw_url)
    if split.scheme in IGNORED_SCHEMES or raw_url.startswith("//"):
        return None, ""
    path_part = unquote(split.path)
    if not path_part:
        return source, split.fragment
    if path_part.startswith("/"):
        resolved = ROOT / path_part.lstrip("/")
    else:
        resolved = (source.parent / path_part).resolve()
    return resolved, split.fragment


def main() -> int:
    errors: list[str] = []
    parsed = {path.resolve(): parse_page(path) for path in HTML_FILES}

    for page, parser in parsed.items():
        rel = page.relative_to(ROOT)
        if not parser.has_main:
            errors.append(f"{rel}: missing <main>")
        if parser.h1_count != 1:
            errors.append(f"{rel}: expected exactly one <h1>, found {parser.h1_count}")
        if not parser.has_description:
            errors.append(f"{rel}: missing meta description")
        if not parser.has_viewport:
            errors.append(f"{rel}: missing viewport meta")
        if page.name != "404.html" and not parser.has_canonical:
            errors.append(f"{rel}: missing canonical link")

        duplicate_ids = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
        for duplicate in duplicate_ids:
            errors.append(f"{rel}: duplicate id '{duplicate}'")

        for img in parser.images:
            if "alt" not in img:
                errors.append(f"{rel}: image missing alt text ({img.get('src', 'unknown source')})")

        for tag, url, attrs in parser.links:
            if attrs.get("target") == "_blank":
                rel_values = set(attrs.get("rel", "").split())
                if not ({"noreferrer", "noopener"} & rel_values):
                    errors.append(f"{rel}: target=_blank link missing rel protection ({url})")

            target, fragment = resolve_local(page, url)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"{rel}: local reference escapes repository ({url})")
                continue

            if not target.exists():
                errors.append(f"{rel}: broken local {tag} reference ({url})")
                continue

            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target.resolve())
                if target_parser and fragment not in target_parser.ids:
                    errors.append(f"{rel}: missing fragment '#{fragment}' in {target.relative_to(ROOT)}")

    if errors:
        print("Static site checks failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Static site checks passed for {len(HTML_FILES)} HTML pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
