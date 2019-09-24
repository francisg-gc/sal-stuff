#!/usr/bin/python2.7

import os
import json
import subprocess
import plistlib
import datetime

managedinstalldir = '/Library/Managed Installs/'
conditionalitemspath = os.path.join(managedinstalldir, 'ConditionalItems.plist')

def get_mac_docker_running():
  cmd="docker container ls  --format '{{json .}}' 2> /dev/null"
  try:
    return json.loads(subprocess.check_output(cmd,universal_newlines=True,shell=True))
  except:
    return []

def main():

    # CRITICAL! Checks if the ConditionalItems.plist already exists or not
    new_dict= dict(mac_docker_running = get_mac_docker_running() ) 
    if os.path.exists(conditionalitemspath):
        # "ConditionalItems.plist" exists, so read it FIRST (existing_dict)
        existing_dict = plistlib.readPlist(conditionalitemspath)
        # Create output_dict which joins new data generated in this script with existing data
        output_dict = dict(existing_dict.items() + new_dict.items() ) 
    else:
        # "ConditionalItems.plist" does not exist,
        # output only consists of data generated in this script
        output_dict = new_dict

        # Write out data to "ConditionalItems.plist"
    plistlib.writePlist(output_dict, conditionalitemspath)


if __name__ == '__main__':
    main()
