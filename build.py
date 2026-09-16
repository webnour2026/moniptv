import requests

SOURCES = [
    "https://iptv-org.github.io/iptv/countries/ma.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u",
    "https://iptv-org.github.io/iptv/countries/fr.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",
]

def fetch(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text.splitlines()

def merge(sources):
    seen = set()
    output = ["#EXTM3U"]
    for src in sources:
        lines = fetch(src)
        i = 0
        while i < len(lines):
            if lines[i].startswith("#EXTINF"):
                info, url = lines[i], lines[i+1]
                if url not in seen:
                    seen.add(url)
                    output.append(info)
                    output.append(url)
                i += 2
            else:
                i += 1
    return "\n".join(output)

if __name__ == "__main__":
    result = merge(SOURCES)
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(result)
