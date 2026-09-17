from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str]] = []
        self.images_missing_alt: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value for key, value in attrs if value is not None}
        if tag == "img":
            if not values.get("alt", "").strip():
                self.images_missing_alt.append(values.get("src", "<unknown>"))
            if "src" in values:
                self.references.append(("src", values["src"]))
        elif tag in {"script", "source"} and "src" in values:
            self.references.append(("src", values["src"]))
        elif tag == "link" and "href" in values:
            self.references.append(("href", values["href"]))
        elif tag == "a" and "href" in values:
            self.references.append(("href", values["href"]))


def resolve_reference(html_file: Path, reference: str) -> Path | None:
    parts = urlsplit(reference)
    if parts.scheme in IGNORED_SCHEMES or parts.netloc or reference.startswith("//"):
        return None
    if not parts.path:
        return None

    if parts.path.startswith("/"):
        target = ROOT / parts.path.lstrip("/")
    else:
        target = html_file.parent / parts.path

    if parts.path.endswith("/"):
        target = target / "index.html"

    return target.resolve()


def main() -> int:
    problems: list[str] = []
    html_files = sorted(ROOT.rglob("*.html"))

    for html_file in html_files:
        parser = ReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))

        for image in parser.images_missing_alt:
            problems.append(f"{html_file.relative_to(ROOT)}: image missing alt text: {image}")

        for attribute, reference in parser.references:
            target = resolve_reference(html_file, reference)
            if target is None:
                continue
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                problems.append(
                    f"{html_file.relative_to(ROOT)}: {attribute} escapes repository: {reference}"
                )
                continue

            if not target.exists():
                problems.append(
                    f"{html_file.relative_to(ROOT)}: missing local target for {attribute}: {reference}"
                )

    if problems:
        print("Portfolio validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"Portfolio validation passed for {len(html_files)} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
