# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/myayun/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/myayun/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sum up Sunday 22 November 2026's world news in one image: a newspaper front page with 31 stories. The three hero stories are the COP31 climate summit collapsing in Antalya with no deal, Mexico capturing cartel boss 'El Chapo Isidro' with 11 killed, and a Russian drone hitting a Kyiv apartment block with 14 missing, plus the S&P 500 falling into correction, BepiColombo entering orbit around Mercury, and Iran striking Bahrain as the US blockade hits 130 days.

## Run it

```sh
python3 main.py
```

The program copies `assets/entry.png` to `/output/entry.png` and prints its
size and sha256. It is deterministic: every run writes the same bytes.

## How the image is built

The front page is drawn with Pillow by `build_image_v5.py` (kept in the
project history): one dominant hero (COP31), two stacked heroes (El Chapo,
Kyiv), six medium stories, a world map with pins, 22 briefs, a statistics
card strip with a globe motif, and a DATE CHECK box listing the 19 November
stories that are not on this page as news. Every story was verified against
a primary outlet (BBC, Reuters, AP, The Guardian, Al Jazeera) before it
went in.

---

<sub>Entered on [make.fun](https://make.fun/?ref=xcd24b0d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
