"""
VMware vRealize Session implementation and supporting objects.

Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import re
import os
import yaml

from requests.auth import HTTPBasicAuth
from requests.packages import urllib3

from .config import VRO_TCP_PORT
from .utils import format_url,safeget



class Session:
    @property
    def basic_auth(self):
        return HTTPBasicAuth(self.username, self.password)

    @property
    def disable_warnings(self):
        return self._disable_warnings

    @property
    def password(self):
        return self._password

    @property
    def url(self):
        return self._url

    @property
    def username(self):
        return self._username

    @property
    def verify_ssl(self):
        return self._verify_ssl

    def __init__(self, url, username, password, verify_ssl=False, disable_warnings=True, proxies=None, alias=None, tags=[]):
        """
        Returns a new Session object.

        :param url:
         Url of the vRO appliance (i.e. https://vro.mydomain.com:8281).

        :param username:
         Username to authenticate with the vRO appliance.

        :param password:
         Password to authenticate with the vRO appliance.

        :param verify_ssl:
         Verify SSL certification during connections, by default False.

        :param disable_warnings:
         Disable connection warnings, by default True.
        """
        self.log = logging.getLogger(self.__class__.__name__)

        self._url = url
        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl
        self._disable_warnings = disable_warnings
        self.proxies = proxies
        self.alias = alias
        self.tags = tags

        if re.match(r"^http[s]://", url) is None:
            self._url = "https://" + url
            self.log.info("Added HTTPS protocol to URL: %s" % self.url)

        if re.match(r".*(?:\:\d+)$", url) is None:
            self._url += ":{}".format(VRO_TCP_PORT)
            self.log.info("Added default vRO TCP Port to URL: %s" % self.url)

        if disable_warnings:
            self.log.info("Disabling HTTP warnings in urllib3")
            urllib3.disable_warnings()

        self.log.debug("Base URL = %s" % self.url)



class SessionList:

    def __init__(self):
        self.list = dict()
        self.alias = dict()
        self.load()

    def getAlias(self, filter=None):
        """
        Return a list of alias(names) of vRO nodes
        """
        alias  = list()

        for item in self.list:
            s = self.list.get(item)

            if filter not in s.tags and filter != item and filter != "*":
                continue

            alias.append(item)
        
        return alias

    def getSession(self, alias=None):
    
        if not alias:
            alias = os.environ.get('UNITTEST_SERVER')

        if not alias:
            alias = 'dev-de'

        sessionId = self.alias.get(alias)        
        
        if not sessionId:
            sessionId = alias
        
        session = self.list.get(sessionId)
        
        if not session:
            print "Session: " + alias + ", not found."

        return session
    

    def load(self, path=None):

        if len(self.list) > 0:
            return 

        #Read config/credentials files
        path = ".secrets/vro-credentials.yml"
        dirname = os.path.expanduser("~")
        configFile = os.path.join(dirname, path)

        with open(configFile, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print exc

        defUsername = safeget(config, 'default', 'login')
        defPassword = safeget(config, 'default', 'password')
        proxies = dict(https='socks5://127.0.0.1:8888')

        #Read the node list
        configFile = "./sample-config/vro.yml"

        with open(configFile, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print exc


        for item in config:

            if item == "default":
                continue

            url =     safeget(config, item, 'url')
            tags =    safeget(config, item, 'tags')
            aliases = safeget(config, item, 'alias')

            s = Session(url=url, username=defUsername, password=defPassword, proxies=proxies, alias=item, tags=tags)            
            self.list[item]=s

            #Update alias list
            self.alias[url]=item
            for alias in aliases:
                self.alias[alias]=item
            
