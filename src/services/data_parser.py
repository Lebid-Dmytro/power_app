import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any


class WikipediaParser:
    WIKI_URL = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"

    async def get_raw_data(self) -> List[Dict[str, Any]]:
        print(f"-> Завантаження: {self.WIKI_URL}")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            )
        }

        async with httpx.AsyncClient(timeout=30.0, headers=headers, follow_redirects=True) as client:
            r = await client.get(self.WIKI_URL)
            r.raise_for_status()
            html = r.text

        soup = BeautifulSoup(html, "lxml")

        table = soup.find("table", class_="wikitable")
        if not table:
            print("Таблиця не знайдена.")
            return []

        rows = table.find_all("tr")[1:]
        results = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            texts = [c.get_text(strip=True) for c in cols]

            def has_letters(s: str) -> bool:
                return any(ch.isalpha() for ch in s)

            def is_number_like(s: str) -> bool:
                s_clean = s.replace(",", "").replace("\u00a0", "")
                return s_clean.isdigit()

            country_idx = None
            for i, txt in enumerate(texts):
                if has_letters(txt) and "%" not in txt:
                    country_idx = i
                    break

            if country_idx is None:
                continue

            pop_idx = None
            for j in range(country_idx + 1, len(texts)):
                if is_number_like(texts[j]):
                    pop_idx = j
                    break

            if pop_idx is None:
                continue

            region_idx = None
            for k in range(pop_idx + 1, len(texts)):
                if has_letters(texts[k]) and "%" not in texts[k]:
                    region_idx = k
                    break

            if region_idx is None:
                continue

            country = texts[country_idx].split("\n")[0]
            pop_text = texts[pop_idx].replace(",", "").replace("\u00a0", "")
            region = texts[region_idx]

            try:
                population = int(pop_text)
            except Exception:
                continue

            if not country or "Total" in country:
                continue

            results.append({
                "country_name": country,
                "region_name": region,
                "population": population,
                "source_url": self.WIKI_URL,
            })

        print(f"-> Спаршено {len(results)} записів.")
        return results
