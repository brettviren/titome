#!/usr/bin/env python3
'''
'''
import os
import pytz
import arrow
import click

from datetime import datetime
import parsedatetime as pdt
from itertools import product as outer

from configparser import ConfigParser

from rich.table import Table
from rich.console import Console
console = Console()

def date_test():
    cal = pdt.Calendar()
    now = datetime.now()
    console.print(cal.parseDT("today 10 pm", now))
    arw = arrow.get(cal.parseDT("today 10 pm", now)[0])
    console.print(arw.humanize())

def table_test():

    from rich.console import Console
    from rich.table import Table

    table = Table(title="Star Wars Movies")

    table.add_column("Released", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    console.print(table)

def get_config(filename):
    if filename is None:
        ch = os.environ.get('XDG_CONFIG_HOME')
        if ch:
            filename = os.path.join(cg, "titome", "titome.cfg")
        else:
            filename = os.path.join(os.environ['HOME'], ".titome.cfg")
    cfg = ConfigParser()
    if os.path.exists(filename):
        cfg.read(filename)
        return cfg

    # make default, save and return

    # The time zones to care about.  'local' is implied
    cfg["zones"] = {}
    cfg["zones"]["BNL"] = "US/Eastern"
    cfg["zones"]["FNAL"] = "US/Central"
    cfg["zones"]["LBNL"] = "US/Pacific"
    cfg["zones"]["RAL"] = "Europe/London"
    cfg["zones"]["CERN"] = "Europe/Zurich"
    cfg["zones"]["KEK"] = "Japan"
    
    with open(filename, 'w') as fp:
        cfg.write(fp)

    return cfg

def parse_date(text):
    cal = pdt.Calendar()
    tt, rc = cal.parse(text, arrow.utcnow().timetuple())
    assert(rc)
    arw = arrow.get(tt)
    return arw.to("local")

    # console.print()
    # arw = arrow.get(cal.parseDT("today 10 pm", now)[0])
    # console.print(arw.humanize())

@click.command()
@click.option("-c", "--config", default=None,
              type=click.Path(dir_okay=False, file_okay=True),
              help="Configuration file")
@click.option("-t", "--times", 
              default="9,10,11,12,13,14,15,16,17,18",
              help="Specific times to display")
@click.argument("when", nargs=-1)
def main(config, times, when):
    cfg = get_config(config)

    if when:
        when = ' '.join(when)
    else:
        when = "today"
    
    arw = parse_date(when)
    #print(arw)
    hours = [int(h) for h in times.split(",")]
    zones = [z.split(":",1) for z in cfg["zones"].values()]


    first = arw.replace(hour=hours[0])
    fmtstr = first.strftime('%A %m/%d %H:%M')
    human = first.humanize()
    table = Table(title=f'{when}: {fmtstr} ({human})')
    table.add_column("zone")
    for h in hours:
        table.add_column(str(h), justify="right")

    lines = list()
    for zz in zones:
        if len(zz) == 1:
            zz.append(zz[0])
        zone,label = zz
        hh = [str(arw.replace(hour=h).to(zone).hour) for h in hours]
        table.add_row(label, *hh)

    console.print(table)
    # console.rule(f'[bold red]{when}')


if __name__ == '__main__':
    main()
