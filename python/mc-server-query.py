#!/usr/bin/env python3

# WARNING: This program is only made compatible for GNU/Linux,
# because is is using the standard bash shell color formatting

# import modules
from mcipc.query import Client
import os.system
import time
import sys

# define "replace_all" function
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

# define sleep time
if len(sys.argv)<2:
    seconds, stop_cmd = 1, False
elif sys.argv[1]=="0":
    stop_cmd = True
else:
    seconds, stop_cmd = int(sys.argv[1]), False

# first cleanup if sleep timer given
if not(stop_cmd):
    os.system("clear")

while True:
    # get query
    with Client('127.0.0.1', 25565) as client:
        stats = client.full_stats

    # print motd
    minecraft_to_terminal_colors = { "§0": "\\e[30m", "§1": "\\e[34m", "§2":"\\e[32m", "§2":"\\e[36m", "§4":"\\e[31m", "§5":"\\e[35m", "§6":"\\e[33m", "§7":"\\e[37m", "§8":"\\e[90m","§9":"\\e[94m", "§a":"\\e[92m", "§b":"\\e[96m", "§c":"\\e[91m", "§d":"\\e[95m", "§e":"\\e[93m", "§f":"\\e[97m", "§r":""} # WARNING: "§r" gets removed
    motd="echo -e \""+replace_all(stats[2], minecraft_to_terminal_colors)+"\\e[39m\""
    os.system(motd)

    # print server type
    cache_text = str(stats[6])[str(stats[6]).find('\'')+1:]
    os.system("echo -e \"\n\\e[97mServer:   \\e[39m"+stats[4]+" "+cache_text[:cache_text.find('\'')]+"\"")

    # list all players
    player_list = ""
    for i in stats[12]:
        player_list += i+", "
    player_list = player_list[:-2]
    os.system("echo -e \"\\e[97mPlayers ["+str(stats[8])+"/"+str(stats[9])+"]:   \\e[39m"+player_list+"\"")

    # reload after timer or stop completely
    if stop_cmd:
        break
    else:
        time.sleep(seconds)
        os.system("clear")
