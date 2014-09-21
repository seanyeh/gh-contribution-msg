#!/usr/bin/env python

import argparse
import datetime
import os
import re
import subprocess

# 4 x 5 letters
LETTERS = {
        " ": 20*[0],
        "a": [
            1,1,1,1,
            1,0,0,1,
            1,1,1,1,
            1,0,0,1,
            1,0,0,1
            ],
        "b": [
            1,1,1,0,
            1,0,0,1,
            1,1,1,1,
            1,0,0,1,
            1,1,1,0
            ],
        "c": [
            1,1,1,1,
            1,0,0,0,
            1,0,0,0,
            1,0,0,0,
            1,1,1,1
            ],
        "d": [
            1,1,1,0,
            1,0,0,1,
            1,0,0,1,
            1,0,0,1,
            1,1,1,0
            ],
        "e": [
            1,1,1,1,
            1,0,0,0,
            1,1,1,0,
            1,0,0,0,
            1,1,1,1
            ],
        "f": [
            1,1,1,1,
            1,0,0,0,
            1,1,1,1,
            1,0,0,0,
            1,0,0,0
            ],
        "g": [
            0,1,1,1,
            1,0,0,0,
            1,0,1,1,
            1,0,0,1,
            0,1,1,0
            ],
        "h": [
            1,0,0,1,
            1,0,0,1,
            1,1,1,1,
            1,0,0,1,
            1,0,0,1
            ],
        "i": [
            1,1,1,1,
            0,1,1,0,
            0,1,1,0,
            0,1,1,0,
            1,1,1,1
            ],
        "j": [
            1,1,1,1,
            0,0,1,0,
            0,0,1,0,
            1,0,1,0,
            0,1,1,0
            ],
        "k": [
            1,0,0,1,
            1,0,1,0,
            1,1,0,0,
            1,0,1,0,
            1,0,0,1
            ],
        "l": [
            1,0,0,0,
            1,0,0,0,
            1,0,0,0,
            1,0,0,0,
            1,1,1,1
            ],
        "m": [
            1,0,0,1,
            1,1,1,1,
            1,0,0,1,
            1,0,0,1,
            1,0,0,1
            ],
        "n": [
            1,0,0,1,
            1,1,0,1,
            1,0,1,1,
            1,0,1,1,
            1,0,0,1
            ],
        "o": [
            0,1,1,0,
            1,0,0,1,
            1,0,0,1,
            1,0,0,1,
            0,1,1,0
            ],
        "p": [
            0,1,1,0,
            1,0,0,1,
            1,1,1,0,
            1,0,0,0,
            1,0,0,0
            ],
        "q": [
            0,1,1,0,
            1,0,0,1,
            1,0,0,1,
            0,1,1,0,
            0,0,0,1
            ],
        "r": [
            1,1,1,0,
            1,0,0,1,
            1,1,1,0,
            1,0,1,0,
            1,0,0,1
            ],
        "s": [
            0,1,1,1,
            1,0,0,0,
            0,1,1,0,
            0,0,0,1,
            1,1,1,0
            ],
        "t": [
            1,1,1,1,
            0,1,1,0,
            0,1,1,0,
            0,1,1,0,
            0,1,1,0
            ],
        "u": [
            1,0,0,1,
            1,0,0,1,
            1,0,0,1,
            1,0,0,1,
            0,1,1,0
            ],
        "v": [
            1,0,0,1,
            1,0,0,1,
            1,0,0,1,
            1,1,1,1,
            0,1,1,0
            ],
        "w": [
            1,0,0,1,
            1,0,0,1,
            1,0,0,1,
            1,1,1,1,
            1,0,0,1
            ],
        "x": [
            1,0,0,1,
            1,0,0,1,
            0,1,1,0,
            1,0,0,1,
            1,0,0,1
            ],
        "y": [
            1,0,0,1,
            1,0,0,1,
            0,1,1,0,
            0,1,1,0,
            0,1,1,0
            ],
        "z": [
            1,1,1,1,
            0,0,1,0,
            0,1,1,0,
            0,1,0,0,
            1,1,1,1
            ]
        }


def create_commit(date, filename="README.md"):
    cur_perm = oct(os.stat(filename).st_mode)[5:]

    if cur_perm == "644":
        new_perm = 484 # 744
    else:
        new_perm = 420 # 644

    os.chmod(filename, new_perm)

    git_add = "git add %s" % filename
    git_cm = "git commit -m \"YO\" --date=\"%s\"" % date

    git_cmd = "%s;%s" % (git_add, git_cm)

    subprocess.call(git_cmd, shell=True)


def get_first_sunday():
    first_day = datetime.datetime.now() - datetime.timedelta(days=365)

    # find nearest sunday
    days_offset = 6 - first_day.weekday()
    first_day += datetime.timedelta(days=days_offset)

    return first_day


def char_to_pixels(c):
    m = LETTERS[c.lower()]

    arr = []
    for i in range(4):
        arr.append(0)
        for j in range(5):
            index = 4*j + i
            arr.append(m[index])

        arr.append(0)

    # Add a column of vertical space
    arr += [0] * 7
    return arr


def pixels_to_dates(pixel_arr):
    offset_tuples = filter(lambda x: x[1], enumerate(pixel_arr))
    offsets = map(lambda x: x[0], offset_tuples)

    first_sunday = get_first_sunday()

    return map(lambda x: first_sunday + datetime.timedelta(days=x), offsets)


def msg_to_pixels(msg):
    pixel_arr = []
    for c in msg:
        pixel_arr += char_to_pixels(c)

    return pixel_arr


def create_msg(msg, num_commits):
    pixel_arr = msg_to_pixels(msg)
    for date in pixels_to_dates(pixel_arr):
        for i in range(num_commits):
            create_commit(date)


def git_init(reponame):
    subprocess.call(["git", "init", reponame])
    os.chdir(reponame)
    subprocess.call("echo \"Hello\" > README.md", shell=True)


def git_push(username, reponame):
    subprocess.call(["git", "remote", "add", "origin",
                     "git@github.com:%s/%s.git" % (username, reponame)])
    subprocess.call("git push -u origin master", shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", metavar="USERNAME", type=str,
            help="Your github username")
    parser.add_argument("reponame", metavar="REPO_NAME", type=str,
            help="Name of new repository")
    parser.add_argument("message", metavar="MESSAGE", type=str,
            help="Message to draw.")
    parser.add_argument("--num_commits", metavar="NUM", type=int, default=20,
            help="Number of commits for each day. Default: 20")
    args = parser.parse_args()

    if os.path.exists(args.reponame):
        print("'%s' already exists in filesystem!" % args.reponame)
    elif (not re.match("^[a-zA-Z ]+$", args.message)) or len(args.message) > 10:
        print("Message must only contain letters or spaces and have length <= 10")
    else:
        print("First, create a new repository on Github with the name:",
              args.reponame)
        input("Press Enter to continue")
        git_init(args.reponame)
        create_msg(args.message, args.num_commits)
        git_push(args.username, args.reponame)


if __name__ == "__main__":
    main()
