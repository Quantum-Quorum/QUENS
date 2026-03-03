import os
import urllib.request
from astroquery.heasarc import Heasarc


def download_pulsar():
    hsrc = Heasarc()

    try:
        table = hsrc.query_object("PSR J0030+0451", mission="nicermastr") # NICER observation
        if table is not None and len(table) > 0:
            obid = table[0]['OBSID']
            print(f'observation id found {obid}')
    except Exception as e:
        print(e)
