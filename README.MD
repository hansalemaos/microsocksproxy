# Wrapper for microsocks - multithreaded, small, efficient SOCKS5 server - Windows only

## pip install microsocksproxy

### This is a Windows only version. 
On the original page, there is no compiled binary for Windows. I was able to compile it 
using Cygwin. 
microsocks.exe and cygwin1.dll are included. 
The Linux cli version can be downloaded here:
https://github.com/rofl0r/microsocks/releases

#### You can launch several proxies using the cli (adapt the command line)

```
python C:\Users\Gamer\anaconda3\envs\dfdir\Lib\site-packages\microsocksproxy\__init__.py  "C:\Users\Gamer\Documents\Downloads\csvfiles\proxyredirect.txt"
```


This is how the csv file should like:
```python

auth_once,listenip,port,user,password,bindaddr,silent,loglimit,colored
-1,0.0.0.0,1080,baba,bubu,None,False,10,True
-1,0.0.0.0,1081,baba,bubu,None,False,10,True
-1,0.0.0.0,1082,baba,bubu,None,False,10,True
-1,0.0.0.0,1083,baba,bubu,None,False,10,True
```

#### Or you import it
```python

from microsocksproxy import start_proxies

start_proxies(
    allproxies=[
        (-1, "0.0.0.0", 1080, "baba", "bubu", None, False, 10, True),
        (-1, "0.0.0.0", 1081, "baba", "bubu", None, False, 10, True),
        (-1, "0.0.0.0", 1082, "baba", "bubu", None, False, 10, True),
    ]
)
```

#### Each connection is printed in a different color

![Example](https://github.com/hansalemaos/screenshots/raw/main/2023-03-03%2002_52_58-dfdir%20%E2%80%93%20multiproxy.py%20Administrator.png "Example")

