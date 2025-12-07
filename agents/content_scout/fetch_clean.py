import requests


def fetch_and_clean(url: str, timeout: int = 10) -> dict:
    """
    Download the webpage and extract the main readable text.

    Returns:
        {
            "ok": bool,
            "title": str,
            "text": str,
            "language": str | None,
            "error": str | None
        }
    """
    try:
        # Imported lazily to avoid hard failures when optional deps are missing.
        from readability import Document
        from bs4 import BeautifulSoup
        from langdetect import detect
    except ImportError as exc:
        raise ImportError(
            "readability-lxml, beautifulsoup4, and langdetect are required for fetch_and_clean."
        ) from exc

    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        return {
            "ok": False,
            "title": "",
            "text": "",
            "language": None,
            "error": str(e),
        }

    # Requests may include control chars; strip null bytes to avoid lxml errors.
    html = resp.text.replace("\x00", "")

    try:
        # Use readability to pull out the main article
        doc = Document(html)
        title = doc.title() or ""

        simplified_html = doc.summary()
        soup = BeautifulSoup(simplified_html, "html.parser")
        text = soup.get_text(separator="\n")

        # basic cleanup
        lines = [line.strip() for line in text.splitlines()]
        text = "\n".join(line for line in lines if line)

        # detect language on a chunk (avoid super-long strings)
        lang = None
        sample = text[:2000]
        if sample:
            try:
                lang = detect(sample)
            except Exception:
                lang = None
    except Exception as e:
        return {
            "ok": False,
            "title": "",
            "text": "",
            "language": None,
            "error": f"parse_error: {e}",
        }

    return {
        "ok": True,
        "title": title,
        "text": text,
        "language": lang,
        "error": None,
    }
