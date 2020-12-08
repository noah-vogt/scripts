#!/usr/bin/env python3

# WARNING: THIS PROGRAM ISN'T FUNCTIONAL AS OF RIGHT NOW

# WARNING: Only on GNU/Linux you see the colors of this script,
# because it is using the standard bash shell color formatting

# import modules
from mcipc.query import Client
from os import name as os_name, system
from time import sleep
from sys import argv

# define "replace_all" function
def replace_all(text, dic):
    for i, j in dic.items():
        text=text.replace(i, j)
    return text

# setting default values
ip='127.0.0.1'
port=25565
seconds=1
stop_cmd=False

# get values from argv
if len(argv)>1:
    if "-ip" in argv:
        ip=argv[argv.index("-ip")+1]
        if ":" in ip:
            initial_ip = ip
            ip=ip[:ip.find(":")]
            port=int(initial_ip[initial_ip.find(":")+1:])
    if "-p" in argv:
        port=int(argv[argv.index("-p")+1])
    if "-port" in argv:
        port=int(argv[argv.index("-port")+1])
    if "-stop" in argv:
        stop_cmd=True
    if "-sec" in argv:
        seconds=int(argv[argv.index("-sec")+1])
    if ("-help" in argv) or ( "--help" in argv):
        print("Here comes the help (soon).")
        exit()

# define colors for bash shell, WARNING: "§r" gets removed and font styles are not integrated
minecraft_to_terminal_colors={ "§0": "\\e[30m", "§1": "\\e[34m", "§2":"\\e[32m", "§2":"\\e[36m", "§4":"\\e[31m",
    "§5":"\\e[35m", "§6":"\\e[33m", "§7":"\\e[37m", "§8":"\\e[90m","§9":"\\e[94m", "§a":"\\e[92m", "§b":"\\e[96m",
    "§c":"\\e[91m", "§d":"\\e[95m", "§e":"\\e[93m", "§f":"\\e[97m", "§r":""}

while True:
    # clear everything
    system("clear")

    # try to get query
    try:
        with Client(ip,port) as client:
            stats=client.full_stats
    # catch Connection Error and reloop after sleep timer
    except ConnectionRefusedError:
        system("echo -e \"\\e[31mWarning:   \\e[97m'ConnectionRefusedError' [Errno 111] detected\\e[39m\"")
        sleep(seconds)
        if stop_cmd:
            break
        else:
            continue

    # print motd
    motd="echo -e \""+replace_all(stats[2], minecraft_to_terminal_colors)+"\\e[39m\""
    system(motd)

    # print server type
    cache_text=str(stats[6])[str(stats[6]).find('\'')+1:]
    system("echo -e \"\n\\e[97mServer:   \\e[92m"+stats[4]+" "+cache_text[:cache_text.find('\'')]+"\\e[39m\"")

    # list all players
    player_list=""
    for i in stats[12]:
        player_list+=i+", "
    player_list=player_list[:-2]
    system("echo -e \"\\e[97mPlayers ["+str(stats[8])+"/"+str(stats[9])+"]:   \\e[92m"+player_list+"\\e[39m\"")

    # reload after timer or stop completely
    if stop_cmd:
        break
    else:
        sleep(seconds)
