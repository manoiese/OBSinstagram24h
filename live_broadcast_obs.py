import argparse
import subprocess
import json
import os
import psutil
import signal
from ItsAGramLive import ItsAGramLive


def kills(pid):
    '''Kills all process'''
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", "--username", type=str, help="username", required=True)
parser.add_argument("-p", "--password", type=str, help="password", required=True)
parser.add_argument("-f", "--file", type=str, help="File", required=True)
args = parser.parse_args()

live = ItsAGramLive(username=args.username, password=args.password)

if live.login():
    print("You'r logged in")

    if live.create_broadcast():

        if live.start_broadcast():
            obs_cmd = "cd obs; cd bin; cd 64bit; dir "
            dictionary ={ "settings" :{ "bwtest" : False , "key" : live.stream_key , "server" : live.stream_server , "use_auth" : False }, "type" : "rtmp_custom" }
            json_object = json.dumps(dictionary, indent = 4)
            with open("./obs/config/obs-studio/basic/profiles/Sem nome/service.json", "w") as outfile:
                outfile.write(json_object)
            print('CTRL+C to quit.')
            try:
                os.chdir('obs')
                os.chdir('bin')
                os.chdir('64bit')
                obs_cmd = "obs64.exe --startstreaming --minimize-to-tray"
                list_files = subprocess.Popen(obs_cmd, shell=True)
                p = psutil.Process(list_files.pid)
                try:
                    p.wait(timeout=60*60*1)
                except psutil.TimeoutExpired:
                    kills(p.pid)
                    raise
            except KeyboardInterrupt:
                pass
            except Exception as error:
                print(error)
                live.end_broadcast()

            live.end_broadcast()
