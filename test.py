#!/usr/bin/env python3
from rich import print as rprint
import time
import os


def erase_line():
    print(f'\r{" " * (os.get_terminal_size().columns - 1)}', end='\r')

def truncate():
    return os.get_terminal_size().columns


rprint('[cyan]27[/cyan] | https://ncore.pro/t/3173871 | [green]A.vektor.2004.REMASTERED.Hybrid.1080p.BluRay.AAC2.0.x264-pcroland[/green]', end='', flush=True)
time.sleep(1)
erase_line()
rprint('[cyan]28[/cyan] | https://ncore.pro/t/3173872 | [green]fdghgjghjghjghfjghjjghjfgjgfjghfjgjghghjA.vektor.2004.720[/green]', flush=True)
time.sleep(1)
print()
