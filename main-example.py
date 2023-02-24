#Export Plex watchlist to the Letterboxd import format.
import argparse
import configparser
import csv
import sys

#Install plexapi module with pip install plexapi
from plexapi.myplex import MyPlexAccount


def parse_args():
    parser = argparse.ArgumentParser(
        description='Export Plex watchlist to the Letterboxd import format',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--ini', default='config.ini',
                        help='config file')
    parser.add_argument('-o', '--output', default='letterboxd-watchlist.csv',
                        help='file to output to')
    parser.add_argument('-w', '--watchlist', nargs='+',
                        help='sections to grab from')
    parser.add_argument('-m', '--managed-user',
                        help='name of managed user to export')
    return parser.parse_args()


def parse_config(ini):
    #Read and validate config file.
    config = configparser.ConfigParser()
    config.read(ini)
    auth = config['auth']
    missing = {'account', 'plex'} - set(auth.keys())
    if missing:
        print(f'Missing the following config values: {missing}')
        sys.exit(1)
    return auth


def write_csv(watchlist, output):
    #Generate Letterboxd import CSV.#
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Year', 'tmdbID'])

        count = 0
        for watchlist in watchlist:
            for item in watchlist():
                date = None
                writer.writerow([item.title, item.year, item.tmdbID])
                count += 1
    print(f'Exported {count} items to {output}.')


def main():
    args = parse_args()
    auth = parse_config(args.ini)
    #Needs 
    plex = parse_config(config.ini)
    #MyPlxAccount(auth['username'], auth['token'])
    if args.managed_user:
        myplex = plex.myPlexAccount()
        user = myplex.user(args.managed_user)
        # Get the token for your machine.
        token = user.get_token(plex.machineIdentifier)
        # Login to your server using your friends credentials.
        plex = MyPlexAccount(auth['username'], token)

    watchlist = [plex.library.watchlist(w) for w in args.watchlist]
    write_csv(watchlist, args.output)