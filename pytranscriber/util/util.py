'''
   (C) 2019 Raryel C. Souza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import platform
import os
import subprocess
import requests
import re
from pathlib import PureWindowsPath
from urllib.parse import urlparse
from pytranscriber.gui.message_util import MessageUtil

import requests
from requests.adapters import HTTPAdapter, Retry
import time


class MyUtil(object):
    @staticmethod
    def open_file(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    @staticmethod
    def is_internet_connected(proxies=None):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            print("Proxy", proxies)
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}

            # res = requests.get('http://www.google.com', verify=False,timeout=30, proxies=proxies, headers=headers)
            #print("status",res.status_code)
            # if res.status_code != 200:
            res = MyUtil.send_request('http://www.google.com',proxies=proxies, headers=headers )
            if res != 200:
                return False

            else:
                print("status", res.status_code)
                return True
        except Exception as e:
            print("Error Name: ", e.__class__.__name__)
            print("Error Message: ", e)
            pass

        return False

    @staticmethod
    def send_request(url,
                     n_retries=4,
                     backoff_factor=0.9,
                     status_codes=[504, 503, 502, 500, 429], proxies=None, headers=None):
        sess = requests.Session()
        retries = Retry(connect=n_retries, backoff_factor=backoff_factor,
                        status_forcelist=status_codes)
        sess.mount("https://", HTTPAdapter(max_retries=retries))
        sess.mount("http://", HTTPAdapter(max_retries=retries))
        response = sess.get(url, proxies=proxies, headers=headers)
        return response

    @staticmethod
    def percentage(currentval, maxval):
        return 100 * currentval / float(maxval)