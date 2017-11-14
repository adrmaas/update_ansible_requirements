#!/usr/bin/python

import ConfigParser
import sys
import yaml
import urllib2
import json


# load input from configuration file
config = ConfigParser.ConfigParser()
config.read("update-requirements.conf")
gitHubUser	= config.get('main', 'gitHubUser')
authToken	= config.get('main', 'authToken')


requirementsFile=sys.argv[1] if len(sys.argv) > 1 else "requirements.yml"
newRequirementsFile=requirementsFile + ".new"

baseUrl="https://api.github.com/repos/" + gitHubUser + "/"

with open(requirementsFile) as f:
    # use safe_load instead load
    roleDataCurrent = yaml.safe_load(f)

# Strip the url and the '.git' to get the repository name
for i in roleDataCurrent:
  repository = i['src'].rsplit('/',1)[1]
  repository = repository.rsplit('.',1)[0]
  # Store the repository name with the name key
  i['name'] = repository

file = open(newRequirementsFile, 'w')

# For each role get the github latest release name, which is the release tag
# and write to a new requirements file
for i in roleDataCurrent:
  url = baseUrl + i['name'] + "/releases/latest"
  #print url
  req = urllib2.Request(url)
  req.add_header('Authorization', 'token ' + authToken)
  response = urllib2.urlopen(req)
  data_json = json.loads(response.read())
  #print " - src: " + i['src'] + "\n   version: " + data_json['name'] + "\n"
  output = " - src: " + i['src'] + "\n   version: " + data_json['name'] + "\n\n"
  file.write(output)

file.close()

