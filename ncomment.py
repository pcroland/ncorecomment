#!/usr/bin/env python3
import argparse
import http.cookiejar
import json
import math
import os
import re
import signal
import sys
from datetime import datetime

import requests
import toml
from bs4 import BeautifulSoup as soup
from rich import print as rprint

signal.signal(signal.SIGINT, signal.SIG_DFL)

def opentoml(fl):
    fl = open(fl, 'r')
    t = toml.load(fl)
    fl.close()
    return t


def erase_line():
    print(f'\r{" " * (os.get_terminal_size().columns - 1)}', end='\r')


def truncate():
    return os.get_terminal_size().columns


def pages(param):
    try:
        r = session.get(param).json()
    except json.decoder.JSONDecodeError:
        rprint('[red]ERROR: no result was found.[/red]')
        sys.exit(1)
    perpage = int(r['perpage'])
    results = int(r['total_results'])
    return math.ceil(results / perpage)


def date_check(id_):
    erase_line()
    length = len(id_) + len(str(counter)) + 27
    rprint(f'{counter} | https://ncore.pro/t/[bold]{id_}[/bold] | [not italic bold yellow]{name[:truncate() - length]}[/not italic bold yellow]', end='')
    url = f'https://ncore.pro/ajax.php?action=comments&id={id_}'
    r = session.get(url).text
    if '<div class="hsz_jobb_felso_txt">' in r:
        page = soup(r, 'html.parser')
        c = page.select('.hsz_jobb_felso_date')[-1]
        date = re.search(r'\d+-\d+-\d+ \d+:\d+:\d+', soup.get_text(c))[0].replace('-', '.').replace(' ', '. ')
        comment_date = re.sub("[^0-9]", "", date).ljust(14, '0')
        if comment_date > compare_date:
            erase_line()
            length = len(id_) + len(date) + 27
            rprint(f'https://ncore.pro/t/[bold]{id_}[/bold] | [not bold]{date}[/not bold] | [not italic bold yellow]{name[:truncate() - length]}[/not italic bold yellow]')


def hidden_check(id_):
    erase_line()
    length = len(id_) + len(str(counter)) + 27
    rprint(f'{counter} | https://ncore.pro/t/[bold]{id_}[/bold] | [not italic bold yellow]{name[:truncate() - length]}[/not italic bold yellow]', end='')
    url = f'https://ncore.pro/t/{id_}'
    r = session.get(url).text
    if 'Nem található az adatbázisunkban' in r:
        erase_line()
        length = len(id_) + 27
        rprint(f'https://ncore.pro/t/{id_} | [not italic bold yellow]{name[:truncate() - length]}[/not italic bold yellow]')


def login(username, password):
    rprint(f'logging in as [bold cyan]{username}[/bold cyan]', end='', flush=True)
    if args.twofactor != '':
        rprint(f' with 2FA: [bold cyan]{args.twofactor}[/bold cyan][white]...[/white] ', end='', flush=True)
    else:
        print('... ', end='', flush=True)
    form_data = {
        'submitted': 1,
        'nev': username,
        'pass': password,
        '2factor': args.twofactor,
        'ne_leptessen_ki': 1
    }
    session.post('https://ncore.pro/login.php?2fa', form_data, allow_redirects=False)
    if session.head('https://ncore.pro/').status_code == 200:
        session.cookies.save()
        rprint('[bold green]Successful login.[/bold green]')
    else:
        rprint('[red]ERROR: Login failed, wrong password/2FA or maybe a captcha appeared.[/red]')
        sys.exit(1)


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help',
                    action='help',
                    default=argparse.SUPPRESS,
                    help='Show this help message.')
parser.add_argument('-v', '--version',
                    action='version',
                    version='ncomment 1.4.2',
                    help='Shows version.')
parser.add_argument('-2fa', '--twofactor',
                    default='',
                    help='2FA code for login.')
parser.add_argument('-s', '--search',
                    help='Search word.')
parser.add_argument('-d', '--date',
                    help='Date for comment comparing.')
parser.add_argument('-e', '--exact',
                    action='store_true',
                    help='Only search in torrents that actually contains the search string in the torrent name.')
parser.add_argument('-a', '--all',
                    action='store_true',
                    help='Search in every category, not just your own.')
parser.add_argument('-c', '--category',
                    nargs='*',
                    help='Add search category(ies).')
parser.add_argument('-m', '--mode',
                    default='title',
                    help='Search mode. (title / description / imdb / uploader)')
parser.add_argument('-r', '--hidden',
                    action='store_true',
                    help='List hidden torrents from your uploads. If you use this switch other switches will be ignored.')
args = parser.parse_args()

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        SCRIPT_PATH = os.path.dirname(sys.executable)
    else:
        SCRIPT_PATH = os.path.dirname(__file__)

    userpass_fl = os.path.join(SCRIPT_PATH, 'login.toml')
    if not os.path.exists(userpass_fl):
        print(f'[bold red]ERROR: login.toml is missing.[/bold red]')
        sys.exit(1)
    else:
        userpass = opentoml(userpass_fl)['login']

    username = userpass.split(':')[0]
    password = userpass.split(':')[1]
    twofactor = args.twofactor

    COOKIES_PATH = os.path.join(SCRIPT_PATH, 'cookies.txt')
    session = requests.Session()
    session.cookies = http.cookiejar.MozillaCookieJar(COOKIES_PATH)

    if not os.path.isfile(COOKIES_PATH):
        rprint('🍪.txt is missing, ', end='')
        login(username, password)
    else:
        session.cookies.load()
        response = session.get('https://ncore.pro/')
        if 'login.php' in response.url:
            rprint('🍪.txt expired, ', end='')
            login(username, password)

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
            id_ = torrent['href'].split('=')[-1]
            name = torrent['title']
            counter += 1
            hidden_check(id_)
        erase_line()
        rprint(f'[bold cyan]{counter}[/bold cyan] torrent checked.')
        sys.exit(1)

    if not args.search:
        rprint('[red]ERROR: You have to use -r or -s.[/red]')
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
        rprint('[red]ERROR: invalid mode.[/red]')
        sys.exit(1)

    if args.date:
        compare_date = re.sub('[^0-9]', '', args.date).ljust(14, '0')
        with open(LOG_PATH, 'r') as file:
            log = json.load(file)
        new_date = str(int(datetime.now().strftime('%Y%m%d%H%M%S')) - 5)
        log[args.search] = new_date
    else:
        with open(LOG_PATH, 'r') as file:
            log = json.load(file)
        try:
            compare_date = log[args.search]
        except:
            rprint('[red]ERROR: no date was found in log, you have to specify one with -d.[/red]')
            sys.exit(1)
        new_date = datetime.now().strftime('%Y%m%d%H%M%S')
        log[args.search] = new_date
    cd = str(compare_date)
    readable_date = f'{cd[0:4]}.{cd[4:6]}.{cd[6:8]}. {cd[8:10]}:{cd[10:12]}:{cd[12:14]}'
    rprint(f'Searching comments newer than [bold cyan]{readable_date}[/bold cyan].')

    type_and_mode = ''
    if args.all: type_and_mode = '&tipus=all'

    valid_categories = ['xvid_hun', 'xvid', 'dvd_hun', 'dvd', 'dvd9_hun', 'dvd9', 'hd_hun', 'hd',
                        'xvidser_hun', 'xvidser', 'dvdser_hun', 'dvdser', 'hdser_hun', 'hdser',
                        'mp3_hun', 'mp3', 'lossless_hun', 'lossless', 'clip',
                        'xxx_xvid', 'xxx_dvd', 'xxx_imageset', 'xxx_hd',
                        'game_iso', 'game_rip', 'console',
                        'iso', 'misc', 'mobil',
                        'ebook_hun', 'ebook']
    if args.category:
        for c in args.category:
            if c not in valid_categories:
                rprint(f'[red]ERROR:[/red] [bold cyan]{c}[/bold cyan] [red]is not a valid category.[/red]\nValid categories are: [bold green]{"[/bold green],[bold green] ".join(valid_categories)}[/bold green]')
                sys.exit(1)
        type_and_mode = f'&kivalasztott_tipus={",".join(args.category)}&tipus=kivalasztottak_kozott'

    url = f'https://ncore.pro/torrents.php?&mire={args.search}&miben={mode}{type_and_mode}&jsons=true'
    page_number = pages(url)

    for i in range(1, page_number + 1):
        url = f'https://ncore.pro/torrents.php?oldal={str(i)}&mire={args.search}&miben={mode}{type_and_mode}&jsons=true'
        r = session.get(url).text
        r = json.loads(r)
        for torrent in r['results']:
            id_ = torrent['torrent_id']
            name = torrent['release_name']
            if args.exact:
                if args.search in name:
                    counter += 1
                    date_check(id_)
            else:
                counter += 1
                date_check(id_)

    with open(LOG_PATH, 'w', encoding='utf-8') as output:
        json.dump(log, output, indent=4, ensure_ascii=False)

    erase_line()
    rprint(f'[bold cyan]{counter}[/bold cyan] torrent checked.')
