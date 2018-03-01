# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "AskMeraki":
        return {}
    
    if req.get("result").get("action") == "AskMeraki":
        baseurl = "https://dashboard.meraki.com/api/v0/organizations/419894/admins"
        #baseurl = "https://dashboard.meraki.com/api/v0/organizations/"
        request_headers = {'X-Cisco-Meraki-API-Key': '35e1fed7af6f534c4b42747ff0feaed1685413f7',
                           'Content-Type': 'application/json'}
        request = Request(baseurl, headers=request_headers)  
        result = urlopen(request).read()

        try:
            data = json.loads(result)
        except ValueError:
            return speak('Sorry, looks like the network has gone to sleep!!!, try again later')

        return speak(GetAdminCount(data))

    if req.get("result").get("action") == "AskAdmin":
        baseurl = "https://dashboard.meraki.com/api/v0/organizations/419894/admins"
        #baseurl = "https://dashboard.meraki.com/api/v0/organizations/"
        request_headers = {'X-Cisco-Meraki-API-Key': '35e1fed7af6f534c4b42747ff0feaed1685413f7',
                           'Content-Type': 'application/json'}
        request = Request(baseurl, headers=request_headers)  
        result = urlopen(request).read()

        try:
            data = json.loads(result)
        except ValueError:
            return speak('Sorry, looks like the network has gone to sleep!!!, try again later')

        return speak(GetAdminList(data))

def speak(text):
    
    return {
        "speech": text,
        "displayText": text,
        "source": "webhook"
    }

def GetAdminCount(data):
    Kount = len(data)
    if Kount == 0:
        speech = "Sorry but there are no admin accounts available"
    else:
        speech = "There are " + str(Kount) + " admin accounts, do you wish me to list them"

    return speech

def GetAdminList(data):
    speech = " They are, "
    Kount = len(data)
    if Kount == 0:
        for current in data:
        speech = speech + current["name"] + ","


    return speech


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
