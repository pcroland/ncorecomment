#!/usr/bin/env python3
import argparse, http.cookiejar, json, math, os, re, signal, sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup as soup

def erase_line():
    print('\r{}'.format(' ' * (os.get_terminal_size().columns - 1)), end='')

def truncate():
    return os.get_terminal_size().columns

def pages(param):
    try:
        r = session.get(param).json()
    except json.decoder.JSONDecodeError:
        print('ERROR: no result was found.')
        sys.exit(1)
    perpage = int(r['perpage'])
    results = int(r['total_results'])
    return math.ceil(results / perpage)

def date_check(param):
    erase_line()
    print('\r{} | https://ncore.pro/t/{} | {}'.format(counter, id, name)[:truncate()], end="")
    url = 'https://ncore.pro/ajax.php?action=comments&id=' + param
    r = session.get(url).text
    if '<div class="hsz_jobb_felso_txt">' in r:
        page = soup(r, 'html.parser')
        c = page.select('.hsz_jobb_felso_date')[-1]
        date = re.search(r'\d+-\d+-\d+ \d+:\d+:\d+', soup.get_text(c))[0]
        comment_date = re.sub("[^0-9]", "", date).ljust(14, '0')
        if comment_date > compare_date:
            erase_line()
            print('\rhttps://ncore.pro/t/{} | {} | {}'.format(id, date, name)[:truncate()])

def hidden_check(param):
    erase_line()
    print('\r{} | https://ncore.pro/t/{} | {}'.format(counter, id, name)[:truncate()], end="")
    url = 'https://ncore.pro/t/' + param
    r = session.get(url).text
    if 'Nem található az adatbázisunkban' in r:
        erase_line()
        print('\rhttps://ncore.pro/t/{} | {}'.format(id, name)[:truncate()])

def login():
    print('You need to login to use this script.')
    form_data = {
        "submitted": 1,
        "nev": input('Username: '),
        "pass": input('Password: '),
        "2factor": input('Two Factor (empty if none): '),
        "ne_leptessen_ki": 1
    }
    session.post('https://ncore.pro/login.php?2fa', form_data, allow_redirects=False)
    if session.head('https://ncore.pro/').status_code == 200:
        session.cookies.save()
        print('Successful login.')
    else:
        print('ERROR: Login failed, wrong password/2FA or maybe a captcha appeared.')
        sys.exit(1)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help',
                    action='help',
                    default=argparse.SUPPRESS,
                    help='Show this help message.')
parser.add_argument('-s', '--search',
                    help='Search word.')
parser.add_argument('-d', '--date',
                    help='Date for comment comparing.')
parser.add_argument('-e', '--exact',
                    action='store_true',
                    help='Only search in torrents that actually contains the search string in the torrent name.')
parser.add_argument('-m', '--mode',
                    default='title',
                    help='Search mode. (title / description / imdb / uploader)')
parser.add_argument('-r', '--hidden',
                    action='store_true',
                    help='List hidden torrents from your uploads. If you use this switch other switches will be ignored.')
parser.add_argument('-v', '--version',
                    action='version',
                    version='ncomment 1.2',
                    help='Shows version.')
args = parser.parse_args()

if getattr(sys, 'frozen', False):
    SCRIPT_PATH = os.path.dirname(sys.executable)
else:
    SCRIPT_PATH = os.path.dirname(__file__)

COOKIES_PATH = os.path.join(SCRIPT_PATH, 'cookies.txt')
session = requests.Session()
session.cookies = http.cookiejar.MozillaCookieJar(COOKIES_PATH)
if not os.path.isfile(COOKIES_PATH):
    print('ERROR: cookies.txt is missing.')
    login()
else:
    session.cookies.load()
    response = session.get('https://ncore.pro/')
    if 'login.php' in response.url:
        print('ERROR: expired cookies.txt')
        login()

signal.signal(signal.SIGINT, signal.SIG_DFL)

LOG_PATH = os.path.join(SCRIPT_PATH, 'log.json')
if not os.path.isfile(LOG_PATH):
    empty = {}
    with open(LOG_PATH, 'w', encoding='utf-8') as output:
        json.dump(empty, output, indent=4, ensure_ascii=False)

counter = 0

if args.hidden:
    r = session.get('https://ncore.pro/profile.php?action=torrents').text
    page = soup(r, 'html.parser')
    for torrent in soup.select(page, '.torrent_txt_mini2 a'):
        id = torrent['href'].split('=')[-1]
        name = torrent['title']
        counter += 1
        hidden_check(id)
    erase_line()
    print('\r{} torrent checked.'.format(counter))
    sys.exit(1)

if not args.search:
    print('ERROR: You have to use -r or -s.')
    sys.exit(1)

if args.mode == 'title':
    mode = 'name'
elif args.mode == 'description':
    mode = 'leiras'
elif args.mode == 'imdb':
    mode = 'imdb'
elif args.mode == 'uploader':
    mode = 'uploaded_by_nev'
else:
    print('ERROR: invalid mode.')
    sys.exit(1)

if args.date:
    compare_date = re.sub('[^0-9]', '', args.date).ljust(14, '0')
    with open(LOG_PATH, 'r') as file:
        log = json.load(file)
    new_date = str(int(datetime.now().strftime('%Y%m%d%H%M%S')) - 5)
    log[args.search] = new_date
    with open(LOG_PATH, 'w', encoding='utf-8') as output:
        json.dump(log, output, indent=4, ensure_ascii=False)

if not args.date:
    with open(LOG_PATH, 'r') as file:
        log = json.load(file)
    try:
        compare_date = log[args.search]
    except:
        print('ERROR: no date was found in log, you have to specify one with -d.')
        sys.exit(1)
    print('Searching comments newer than {}.'.format(compare_date))
    new_date = datetime.now().strftime('%Y%m%d%H%M%S')
    log[args.search] = new_date
    with open(LOG_PATH, 'w', encoding='utf-8') as output:
        json.dump(log, output, indent=4, ensure_ascii=False)

url = 'https://ncore.pro/torrents.php?mire=' + args.search + '&miben=' + mode + '&jsons=true'
page_number = pages(url)

for i in range(1, page_number + 1):
    url = 'https://ncore.pro/torrents.php?oldal=' + str(i) + '&mire=' + args.search + '&miben=' + mode + '&jsons=true'
    r = session.get(url).text
    r = json.loads(r)
    for torrent in r['results']:
        id = torrent['torrent_id']
        name = torrent['release_name']
        if args.exact:
            if args.search in name:
                counter += 1
                date_check(id)
        else:
            counter += 1
            date_check(id)

erase_line()
print('\r{} torrent checked.'.format(counter))
