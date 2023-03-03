import ast
import csv
import os
import random
import re
import time
from collections import defaultdict, deque
from functools import partial
import subprocess
from ansi.colour.rgb import rgb256
from ansi.colour import fx
import kthread
import psutil
import sys
from threading import Lock
lock=Lock()
from kthread_sleep import sleep

nested_dict = lambda: defaultdict(nested_dict)
proxies = sys.modules[__name__]
proxies.overview = nested_dict()

basedir = os.path.dirname(os.path.abspath(__file__))
minisockspath = os.path.normpath(os.path.join(basedir, "microsocks.exe"))


def print_full_col(text, colour):
    print(
        "".join(
            list(
                map(
                    str,
                    (
                        fx.bold,
                        rgb256(colour[0], colour[1], colour[2]),
                        text,
                        fx.bold,
                        fx.reset,
                    ),
                )
            )
        )
    )


def killprocess(p):
    try:
        if psutil.pid_exists(p):
            try:
                p2 = psutil.Process(p)
                p2.kill()
            except Exception:
                pass
    except Exception as fe:
        pass


def get_right_process(wholecommandline):
    while True:
        for p in psutil.process_iter():
            try:
                if "microsocks.exe" in p.name().lower():
                    c1, c2 = "".join(p.cmdline()), wholecommandline
                    sa = re.sub(r"\W+", "", c1) == re.sub(r"\W+", "", c2)
                    if sa:
                        return p

            except Exception:
                continue


def get_log(color, silent, listenip, port, auth_once, user, password, popen):
    try:
        for stdout_line in iter(popen.stderr.readline, b""):
            try:
                outl = stdout_line.decode("utf-8", "ignore").strip()
                if not silent:
                    te = f"listen:{listenip}█port:{port}█auth:{auth_once}█user:{user}█pass:{password}█{outl}"
                    if not color:
                        print(te)
                    else:
                        print_full_col(te, color)
                yield outl
            except Exception as Fehler:
                continue
        try:
            popen.stdout.close()
            return_code = popen.wait()
        except Exception as fax:
            return ""
    except Exception as vx:
        return ""


def get_all_proxy_pids():
    if proxies.overview:
        return [x[1]["pid"] for x in proxies.overview.items()]


def kill_all():
    if proxies.overview:

        return [x[1]["p_kill"]() for x in proxies.overview.items()]


def get_debug():
    if proxies.overview:

        return [x[1]["p_debug"] for x in proxies.overview.items()]


def get_logs():
    if proxies.overview:

        return [x[1]["p_log"] for x in proxies.overview.items()]


def get_processes():
    if proxies.overview:

        return [x[1]["p"] for x in proxies.overview.items()]


def create_proxies(
    x,
    auth_once=-1,
    listenip="0.0.0.0",
    port=1080,
    user=None,
    password=None,
    bindaddr=None,
    silent=False,
    loglimit=10,
    colored=True,

pidfile=None
):

    wholecommandline = f'"{minisockspath}" {auth_once} -i {listenip} -p {port}'

    if user:
        wholecommandline += f" -u {user}"
    if password:
        wholecommandline += f" -P {password}"
    if bindaddr:
        wholecommandline += f" -b {bindaddr}"

    proxies.overview[x]["auth_once"] = auth_once
    proxies.overview[x]["listenip"] = listenip
    proxies.overview[x]["port"] = port
    proxies.overview[x]["user"] = user
    proxies.overview[x]["password"] = password
    proxies.overview[x]["bindaddr"] = bindaddr
    DEVNULL = open(os.devnull, "wb")

    proxies.overview[x]["process"] = subprocess.Popen(
        wholecommandline,
        stdin=subprocess.PIPE,
        stdout=DEVNULL,
        universal_newlines=False,
        stderr=subprocess.PIPE,
        shell=False,
    )
    proxies.overview[x]["p"] = get_right_process(wholecommandline)
    proxies.overview[x]["pid"] = proxies.overview[x]["p"].pid

    proxies.overview[x]["p_connections"] = partial(proxies.overview[x]["p"].connections)
    proxies.overview[x]["p_debug"] = partial(proxies.overview[x]["p"].as_dict)
    proxies.overview[x]["p_kill"] = partial(proxies.overview[x]["p"].kill)
    if colored:
        co = (
            random.randrange(50, 255),
            random.randrange(50, 255),
            random.randrange(50, 255),
        )

        proxies.overview[x]["color"] = co
    else:
        co = None
        proxies.overview[x]["color"] = None

    if pidfile:
        try:
            lock.acquire()
            with open(pidfile,mode='a',encoding='utf-8') as f:
                f.write(f'{auth_once},{listenip},{port},{user},{password},{bindaddr},{silent},{loglimit},{colored},')
                f.write(str(proxies.overview[x]["pid"]))
                f.write('\n')
        finally:
            lock.release()

    proxies.overview[x]["p_log"] = deque(
        (
            x
            for x in get_log(
                co,
                silent,
                listenip,
                port,
                auth_once,
                user,
                password,
                proxies.overview[x]["process"],
            )
        ),
        loglimit,
    )


def start_proxies(allproxies,pidfile=None):
    for pro in allproxies:
        try:
            maxdi = max(list(proxies.overview.keys()))
        except Exception:
            maxdi = -1
        x = maxdi + 1

        proxies.overview[x]["thread"] = kthread.KThread(
            target=create_proxies,
            name=str(time.perf_counter()) + str(random.randrange(1, 100000000000)),
            args=(x, *pro,pidfile),
        )

        proxies.overview[x]["thread"].start()
        sleep(0.5)


def start_proxies_from_csv(path):
    def convi(x):
        try:
            return ast.literal_eval(x)
        except Exception:
            return x

    allfi = []
    with open(path, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            allfi.append([convi(q.strip()) for q in row])
    pidfile = '\\'.join(path.split('\\')[:-1]) + '\\_withpid_' + path.split('\\')[-1]
    print(pidfile)
    start_proxies(allproxies=allfi[1:],pidfile=pidfile)


if __name__ == "__main__":
    try:
        start_proxies_from_csv(sys.argv[1].strip().strip("'\"").strip())
    except Exception as fe:
        print(
            """
CSV file not found! 
Example:
auth_once,listenip,port,user,password,bindaddr,silent,loglimit,colored
-1,       0.0.0.0, 1080,baba,bubu,    None,     False, 10,     True
-1,       0.0.0.0, 1081,babi,bubu,    None,     True,  10,     False

#or import it
start_proxies(
    allproxies=[
        (-1, "0.0.0.0", 1080, "baba", "bubu", None, False, 10, True),
        (-1, "0.0.0.0", 1081, "baba", "bubu", None, False, 10, True),
        (-1, "0.0.0.0", 1082, "baba", "bubu", None, False, 10, True),
    ]
)


"""
        )

