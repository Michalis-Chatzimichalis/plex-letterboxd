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
    parser.add_argument('-s', '--sections', default=['Films', 'Films Michalis', 'TV Shows', 'TV Shows (Michalis)'], nargs='+',
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


def write_csv(sections, output):
    #Generate Letterboxd import CSV.#
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Year', 'Rating10', 'WatchedDate'])

        count = 0
        for section in sections:
            for movie in section.search(sort='lastViewedAt', unwatched=False):
                date = None
                if movie.lastViewedAt is not None:
                    date = movie.lastViewedAt.strftime('%Y-%m-%d')
                rating = movie.userRating
                if rating is not None:
                    rating = f'{movie.userRating:.0f}'
                writer.writerow([movie.title, movie.year, rating, date])
                count += 1
    print(f'Exported {count} movies to {output}.')


def main():
    args = parse_args()
    auth = parse_config(args.ini)
    #Needs 
    plex = PlexServer(auth['baseurl'], auth['token'])
    if args.managed_user:
        myplex = plex.myPlexAccount()
        user = myplex.user(args.managed_user)
        # Get the token for your machine.
        token = user.get_token(plex.machineIdentifier)
        # Login to your server using your friends credentials.
        plex = PlexServer(auth['baseurl'], token)

    sections = [plex.library.section(s) for s in args.sections]
    write_csv(sections, args.output)