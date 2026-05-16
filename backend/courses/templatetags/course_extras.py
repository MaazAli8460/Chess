import re
from urllib.parse import parse_qs, urlparse

from django import template

register = template.Library()

_YT_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?.*v=|youtu\.be/)([A-Za-z0-9_-]{11})"),
]
_VIMEO_PATTERN = re.compile(r"vimeo\.com/(?:video/)?(\d+)")


@register.filter
def video_embed_url(url: str) -> str:
    """Return an embeddable iframe src for YouTube or Vimeo URLs, or '' if not recognised."""
    if not url:
        return ""
    for pat in _YT_PATTERNS:
        m = pat.search(url)
        if m:
            return f"https://www.youtube.com/embed/{m.group(1)}"
    m = _VIMEO_PATTERN.search(url)
    if m:
        return f"https://player.vimeo.com/video/{m.group(1)}"
    return ""
