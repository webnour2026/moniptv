import requests

SOURCES_FULL = [
    "https://iptv-org.github.io/iptv/countries/ma.m3u",
    "https://iptv-org.github.io/iptv/countries/fr.m3u",
    "https://iptv-org.github.io/iptv/languages/ara.m3u",
]

NEWS_SOURCE = "https://iptv-org.github.io/iptv/categories/news.m3u"
NEWS_LANGUAGES = ["French", "English", "Arabic"]

MOVIES_SOURCE = "https://iptv-org.github.io/iptv/categories/movies.m3u"
MOVIES_LANGUAGES = ["French", "Arabic"]

def fetch(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text.splitlines()

def merge(sources, filter_languages=None):
    seen = set()
    output = []
    for src in sources:
        lines = fetch(src)
        i = 0
        while i < len(lines):
            if lines[i].startswith("#EXTINF"):
                info = lines[i]
                j = i + 1
                extra = []
                while j < len(lines) and lines[j].startswith("#EXTVLCOPT"):
                    extra.append(lines[j])
                    j += 1
                if j >= len(lines):
                    break
                url = lines[j]
                keep = True
                if filter_languages is not None:
                    keep = any(lang in info for lang in filter_languages)
                if keep and url not in seen:
                    seen.add(url)
                    output.append(info)
                    output.extend(extra)
                    output.append(url)
                i = j + 1
            else:
                i += 1
    return output

if __name__ == "__main__":
    all_lines = ["#EXTM3U"]
    all_lines += merge(SOURCES_FULL)
    all_lines += merge([NEWS_SOURCE], filter_languages=NEWS_LANGUAGES)
    all_lines += merge([MOVIES_SOURCE], filter_languages=MOVIES_LANGUAGES)
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))
