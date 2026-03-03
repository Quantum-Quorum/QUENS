import os
import urllib.request
from astroquery.heasarc import Heasarc
from astropy.time import Time

DATA_DIR = 'data/'
def download_pulsar():
    hsrc = Heasarc()

    try:
        print("Downloading pulsar data...")
        print(hsrc.name)
        table = hsrc.query_object("PSR J0030+0451", mission="nicermastr") # NICER observation
        ta = table['name']
        print(ta)
        print(table)
        if table is not None and len(table) > 0:
            dwn_sts = False
            for idx in range(min(5, len(table))):
                obid = table['obsid'][idx]
                if isinstance(obid, bytes):
                    obid = obid.decode("utf-8")
                elif not isinstance(obid, str):
                    obid = str(obid)
                print(f'observation id found {obid}')
                time_mjd = float(table['time'][idx])
                t = Time(time_mjd, format='mjd')
                y_mon = t.to_datetime()
                y_mon_str = y_mon.strftime('%Y_%m')
                f_name = f"ni{obid}_0mpu7_cl.evt.gz"
                url = f"https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/{y_mon_str}/{obid}/xti/event_cl/{f_name}"
                #bruteforce attack or knock knock till we get the correct door!
                try:
                    req = urllib.request.Request(url, method='HEAD')
                    urllib.request.urlopen(req)
                except Exception as check_e:
                    print(f"Observation {obid} event file not found (F0F). Contacting huston to trying next <><><><>")
                    continue
                fpath = os.path.join(DATA_DIR, 'pulsar', f_name)
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                if not os.path.exists(fpath):
                    urllib.request.urlretrieve(url, fpath)
                    print(f"Observation {obid} event file {fpath} downloaded")
                else:
                    print(f"Observation {obid} event file {fpath} already downloaded")
                dwn_sts = True
                break
            if not dwn_sts:
                print(f"Observation {obid} event file {fpath} not downloaded")
            else:
                print(f"UFFOOOO obstacle!")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    download_pulsar()