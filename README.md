# ncomment
### nCore komment kereső
![image1](https://widevine.is-a.fail/WrBB4g.gif)

## Leírás
* A scriptnek meg lehet adni, hogy mire keressen, milyen keresési módban és milyen dátumtól.
* Kilistázza azokat a torrenteket, amiknél talál egy adott dátumnál frissebb komment(ek)et.
* A futtatáskor elmenti az aktuális időt az adott kereséshez,\
így következő futtatásnál már nem kell dátumot megadni és onnan fog keresni.
* A dátumot akármilyen formában meg lehet adni (`2020`, `2020-10-29`, `20201029`, `2020-10-29-22-20-50`)

## Használat
```
usage: ncomment.py [-h] [-s SEARCH] [-d DATE] [-e] [-m MODE] [-r]

optional arguments:
  -h, --help            Show this help message.
  -s SEARCH, --search SEARCH
                        Search word.
  -d DATE, --date DATE  Date for comment comparing.
  -e, --exact           Only search in torrents that actually contains
                        the search string in the torrent name.
  -m MODE, --mode MODE  Search mode. (title / description / imdb / uploader)
                        Default: title
  -r, --hidden          List hidden torrents from your uploads.
                        If you use this switch other switches will be ignored.
```

## Példák
`./ncomment.py -s pcroland -d 20201029`\
Keresés címre.\
\
`./ncomment.py -e -s=-boOk -d 20201029`\
A `-boOk` keresésre kiadott találatokat tovább szűri azokra a torrentekre,\
amiknek ténylegesen szerepel a címében a keresés.\
\
`./ncomment.py -m uploader -s trinitygrp -d 20201029`\
Keresés a feltöltő nevére.

## Telepítés
* `git clone https://github.com/pcroland/ncorecomment`
* `cd ncorecomment`
* `pip install -r requirements.txt`\
Vagy exeként is letöltheted innen: [https://github.com/pcroland/ncorecomment/releases](https://github.com/pcroland/ncorecomment/releases)\
(nem igényel semmit a futtatáshoz.)