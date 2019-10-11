#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Joseph Schroedl
# joe.schroedl@outlook.com
# https://github.com/corndog2000

import argparse
import os

import main as mn

def parse_arguments():
    # Parse command line arguments
    parser = argparse.ArgumentParser(prog="mian.py")

    parser.add_argument(
        "vod_ids", 
        help="Text file with ID numbers of the Twitch VODs. Example: Given the url https://www.twitch.tv/videos/461450418 the ID is 461450418", 
        type=str
    )

    parser.add_argument(
        "client_id",
        help="Your Twitch client ID. This is different from the vod_id. You can get one here https://dev.twitch.tv/console/apps",
        type=str
    )

    parser.add_argument(
        "source_videos",
        nargs='?',
        help="Path to the twitch VOD video file directory",
        type=str
    )

    return parser.parse_args()

def main(vod_ids, client_id, source_videos):
    id_list = []

    with open(vod_ids, "r", newline="") as txtfile:
        for row in txtfile:
            row = row.replace("\n","")
            row = row.replace("\r","")
            id_list.append(row)

    print(id_list)

    file_paths = []

    if source_videos != None:
        for folder, subs, files in os.walk(source_videos):
            for filename in files:
                file_paths.append(os.path.abspath(os.path.join(folder, filename)))
    
    print(file_paths)

    if source_videos != None:
        for vod, fp in zip(id_list, file_paths):
            mn.main(vod, client_id, fp)
    else:
        for vod in id_list:
            print(vod)

            sv = None

            mn.main(vod, client_id, sv)

if __name__ == "__main__":
    args = parse_arguments()
    vod_ids = args.vod_ids
    client_id = args.client_id
    source_videos = args.source_videos
    
    main(vod_ids, client_id, source_videos)