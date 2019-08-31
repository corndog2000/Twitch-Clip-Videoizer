#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Joseph Schroedl
# joe.schroedl@outlook.com
# https://github.com/corndog2000

import argparse
import os
import re

from datetime import datetime
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Twitch chat downloader: https://pypi.org/project/tcd/
import tcd

def parse_arguments():

    # Parse command line arguments
    parser = argparse.ArgumentParser(prog="mian.py")

    parser.add_argument(
        "vod_id", 
        help="ID number of the Twitch VOD. Example: Given the url https://www.twitch.tv/videos/461450418 the ID is 461450418", 
        type=str
    )

    parser.add_argument(
        "client_id",
        help="Your Twitch client ID. This is different from the vod_id. You can get one here https://dev.twitch.tv/console/apps",
        type=str
    )

    parser.add_argument(
        "source_video",
        help="Path to the twitch VOD video file",
        type=str
    )

    return parser.parse_args()

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def make_output_dir(p = "./resources"):
    if os.path.exists(p):
        return
    else:
        os.mkdir(p)

def run_tcd(v, c, p = "./resources"):
    os.system("tcd --video "+ v +" --format irc --output " + p + " --client-id " + c)

def parse_timestamps(a, b, sv, idx, vdcp):
    a_timestamp = a[:a.find("]")]
    if a_timestamp[0] == "[":
        a_timestamp = a_timestamp.replace("[","")

    # change the number below to set how many seconds before the detection to start the clip
    a_timestamp = get_sec(a_timestamp)
    a_timestamp = a_timestamp - 20

    b_timestamp = b[:b.find("]")]
    if b_timestamp[0] == "[":
        b_timestamp = b_timestamp.replace("[","")
    
    # change the number below to set how many seconds after the detection to continue the clip
    b_timestamp = get_sec(b_timestamp)
    b_timestamp = b_timestamp + 10

    print("Generating clip")
    ffmpeg_extract_subclip(sv, a_timestamp, b_timestamp, targetname=(vdcp + "/" + str(idx) + ".mkv"))

def search_vod_log(p, sv, vdcp):
    start_line = None
    end_line = None
    
    triggered = False
    found_on = 0
    word_count = 0

    word = "LUL"
    
    with open(p, "r", newline="", encoding="utf8") as vodfile:
        for idx, row in enumerate(vodfile):
            #print(idx, row)
            
            row = row.upper()

            # Start searching for the word
            if (word in row) and (triggered == False):
                #print("start")
                
                start_line = row
                found_on = idx
                triggered = True

                word_count = 1

            elif (word in row) and triggered:
                #print("bump")

                found_on = idx
                word_count += 1

            # If it's been 6 messages since the last occurance of word so we will stop the selection
            elif ((idx - found_on) >= 6) and triggered:
                #print("end")
                
                if word_count >= 10:
                    end_line = row
                    parse_timestamps(start_line, end_line, sv, idx, vdcp)
                triggered = False
          

def main(vod_id, client_id, source_video):
    print(f"Video ID: {vod_id}")

    vod_clip_path = "./clips/" + vod_id
    vod_log_path = "./resources/" + vod_id + ".log"

    # Create folder that are needed later
    make_output_dir()
    make_output_dir(vod_clip_path)

    if not os.path.exists(vod_log_path):
        run_tcd(v=vod_id, c=client_id)

    print("Starting the search for moments")
    search_vod_log(("./resources/" + vod_id + ".log"), source_video, vod_clip_path)
    print("Done searching")


if __name__ == "__main__":
    args = parse_arguments()
    vod_id = args.vod_id
    client_id = args.client_id
    source_video = args.source_video
    
    main(vod_id, client_id, source_video)