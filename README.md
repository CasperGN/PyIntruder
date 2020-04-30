# PyIntruder
Simple Command Line URL Fuzzer


```
python3 PyIntruder.py 
usage: PyIntruder [-h] [-r] [-s] [-o OUT] url payload

positional arguments:
  url                Url with $ to replace
  payload            payload to replace $ with

optional arguments:
  -h, --help         show this help message and exit
  -r, --redir        Allow HTTP redirects
  -s, --save         Save HTTP response content to files
  -o OUT, --out OUT  Directory to save HTTP responses
 ```
 
 
# Description
This script allows a user to quickly test many similar URLs and analyze responses.  This can act as a simplified alternative to Burp Suite's "Intruder" tool (which heavily rate-limits requests in the free version......).

# Use Case

As an example, say you observe the following URL:
```
http://www.example.com/file/74
```
When accessing the URL, your browser redirects you to a page which automatically downloads a file (this could be any type of file - pdf, doc, exe, mp3, etc.).  This is a common method of allowing users of a website to download content.  In this particular example, the URL above seems to beg the question: "I wonder what I might find at 'http://www.example.com/file/75'? ...or at 'http://www.example.com/file/73'?"

This program automates the process of attempting to browse to each of these potentially-interesting URLs by automatically cycling through a list of custom "payloads". A user can create a list of payloads (say, for example, a list of numbers from 1 through 100) and try each payload in a particular position within the URL (use the dollar-sign character to tell the program where to swap out your payloads within the URL).

```
pyintruder http://www.example.com/file/$ payloads.txt
```
In the above command, where "payloads.txt" is a text file containing a list of numbers 1 - 100 (one number per line), a user can quickly determine which URLs lead somewhere interesting by comparing HTTP status code, Content-Length, or response time:

sample output:
```
root@kali:~# pyintruder http://www.example.com/file/$ payloads.txt
Status    Length    Time      Host
----------------------------------------
200       0         110.536   http://www.example.com/file/01
200       0         112.312   http://www.example.com/file/02
302       0         104.266   http://www.example.com/file/03

...

200       0         137.111   http://www.example.com/file/73
302       0         120.607   http://www.example.com/file/74
302       0         108.553   http://www.example.com/file/75

...
```
In this case, it looks like the interesting URLs are the ones that return a 302 HTTP status code (redirect).  If all URLs are redirecting and you cant find any other distinguishing factors, try using the "-r" option to enable redirection.  The redirected results will often contain more interesting/varying content-lengths.  The program defaults to disabling the following of redirects.  The reason for this is that it is usually much faster and a little less noisy/intrusive, which is good when running an initial scan.


In order to download whatever files might be available at each of these links, you can run a command like this:
```
pyintruder -rs -o /path/to/save/files http://www.example.com/file/$ payloads-refined.txt
```

- The "r" option tells the program to follow redirects
- The "s" option tells the program to save HTTP responses
- The "o" option tells the program where you want to save the responses on your local machine (this option is optional; by default, if "s" is used without "o", it will save files to the current directory)
- "payloads-refined.txt" is your refined list of payloads. This can be useful in a case like this if you want to weed out a bunch of URLs that you found out don't go anywhere interesting.


# Installation
PyIntruder is available as an installable python module. Try running:
```
pip install pyintruder
```
Or you can download and run PyIntruder.py from this repo (swap out `pyintruder` in these examples for `./PyIntruder.py`).

# Dependencies
If it's not already installed, make sure to [install Requests](http://docs.python-requests.org/en/master/user/install/) (try running "pip install requests").
