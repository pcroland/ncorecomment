# ncomment
### nCore komment kereső
![image1](https://widevine.is-a.fail/WrBB4g.gif)

## Leírás
* A scriptnek meg lehet adni, hogy mire keressen, milyen keresési módban, milyen dátumtól és milyen kategóriában.
* Kilistázza azokat a torrenteket, amiknél talál egy adott dátumnál frissebb komment(ek)et.
* A futtatáskor elmenti az aktuális időt az adott kereséshez,\
így következő futtatásnál már nem kell dátumot megadni és onnan fog keresni.
* A dátumot akármilyen formában meg lehet adni (`2020`, `2020-10-29`, `20201029`, `2020-10-29-22-20-50`)

## Használat
```
usage: ncomment.py [-h] [-s SEARCH] [-d DATE] [-e] [-a] [-c [CATEGORY ...]] [-m MODE] [-r] [-v]

optional arguments:
  -h, --help            Show this help message.
  -s SEARCH, --search SEARCH
                        Search word.
  -d DATE, --date DATE  Date for comment comparing.
  -e, --exact           Only search in torrents that actually contains the search string in the torrent name.
  -a, --all             Search in every category, not just your own.
  -c [CATEGORY ...], --category [CATEGORY ...]
                        Add search category(ies).
  -m MODE, --mode MODE  Search mode. (title / description / imdb / uploader)
  -r, --hidden          List hidden torrents from your uploads. If you use this switch other switches will be ignored.
  -v, --version         Shows version.
```

## Példák
`./ncomment.py -s pcroland -d 20201029`\
Keresés címre.\
\
`./ncomment.py -s pcroland -d 20201029 -c xvid_hun hdser_hun`\
Keresés címre, xvid_hun (magyar SD filmek) és hdser_hun (magyar HD sorozatok) kategóriában.\
\
`./ncomment.py -e -s=-boOk -d 20201029`\
A `-boOk` keresésre kiadott találatokat tovább szűri azokra a torrentekre,\
amiknek ténylegesen szerepel a címében a keresés.\
\
`./ncomment.py -m uploader -s trinitygrp -d 20201029`\
Keresés a feltöltő nevére.

## Kategóriák
Az oldalon megtalálható összes kategória támoagatott.
<details>
    <summary>Kategóriák használata</summary>

| Film    |          | Sorozat    |             | Zene        |              | XXX      |              |
|---------|----------|------------|-------------|-------------|--------------|----------|--------------|
| SD/HU   | xvid_hun | SD/HU      | xvidser_hun | MP3/HU      | mp3_hun      | SD       | xxx_xvid     |
| SD/EN   | xvid     | SD/EN      | xvidser     | MP3/EN      | mp3          | DVDR     | xxx_dvd      |
| DVDR/HU | dvd_hun  | DVDR/HU    | dvdser_hun  | Lossless/HU | lossless_hun | Imageset | xxx_imageset |
| DVDR/EN | dvd      | DVDR/EN    | dvdser      | Lossless/EN | lossless     | HD       | xxx_hd       |
| DVD9/HU | dvd9_hun | HD/HU      | hdser_hun   | Klip        | clip         |          |              |
| DVD9/EN | dvd9     | HD/EN      | hdser       |             |              |          |              |
| HD/HU   | hd_hun   |            |             |             |              |          |              |
| HD/EN   | hd       |            |             |             |              |          |              |


| Játék   |          | Program    |             | Könyv       |              |
|---------|----------|------------|-------------|-------------|--------------|
| PC/ISO  | game_iso | Prog/ISO   | iso         | eBook/HU    | ebook_hun    |
| PC/RIP  | game_rip | Prog/RIP   | misc        | eBook/EN    | ebook        |
| Konzol  | console  | Prog/Mobil | mobil       |             |              |
</details>

## Telepítés
* `git clone https://github.com/pcroland/ncorecomment`
* `cd ncorecomment`
* `pip install -r requirements.txt`\
Vagy exeként is letöltheted innen: [https://github.com/pcroland/ncorecomment/releases](https://github.com/pcroland/ncorecomment/releases)\
(nem igényel semmit a futtatáshoz.)