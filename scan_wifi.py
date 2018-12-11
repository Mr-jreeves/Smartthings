/**
 *  Copyright 2018 James Reeves
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 *	Check Wifi Presence
 *
 *	Author: James Reeves. Based on original work by Stuart Buchanan with thanks
 *
 *	Date: 2018-12-11 v1.0 Initial Release
**/

/#!/usr/bin/python
#
#


#Imports
from subprocess import Popen, PIPE
import re   # For Regular Expressions
import pycurl
import time

#
# Make sure your URL domain matches how you access Smartthings
Smartthings_URL = "https://graph-na02-useast1.api.smartthings.com/api/smartapps/installations/"

#
# Remove entries that are not used in your setup
#          ["Name","AppID","AccessToken","IP_Addr","Present"],
UserInfo = ["User-1","AppID-1","Access-1","IP-1",None], \
           ["User-2","AppID-2","Access-2","IP-2",None], \
           ["User-3","AppID-3","Access-3","IP-3",None], \
           ["User-4","AppID-4","Access-4","IP-4",None]

def main():
   while True:
      CheckPresence()
      time.sleep(10)   # 10 second sleep timer - make it longer if you wish

def CheckPresence():
	c = pycurl.Curl()
	for user in UserInfo:
	   pingdata = Popen(["ping","-n","-c","3",user[3]],stdout=PIPE)
     pid = Popen(["arp", "-n", user[3]], stdout=PIPE)
     s = pid.communicate()[0]
     mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s)

     if mac is not None:  # Means no Mac HW address was found
	      if user[4] is not True:
#	         print user[0]+" is present at ", time.asctime( time.localtime(time.time()) )
	         c.setopt(c.URL, Smartthings_URL+user[1]+"/Phone/home?access_token="+user[2])
	         c.perform()
	         user[4] = True
	   else:
	      if user[4] is True:
#	         print user[0]+" is away at ", time.asctime( time.localtime(time.time()) )
	         c.setopt(c.URL, Smartthings_URL+user[1]+"/Phone/away?access_token="+user[2])
	         c.perform()
	         user[4] = False

if __name__ == '__main__':

        main()
