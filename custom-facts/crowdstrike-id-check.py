#!/usr/bin/python2.7

import os
import subprocess
import plistlib
import datetime

managedinstalldir = '/Library/Managed Installs/'
conditionalitemspath = os.path.join(managedinstalldir, 'ConditionalItems.plist')

def get_crowdstrike_id():
  cmd='/usr/sbin/sysctl -n cs.sensorid 2> /dev/null || echo NONE'
  try:
    return [b for b in subprocess.check_output(cmd,universal_newlines=True,shell=True).split('\n')
if b ] 
  except:
    return []

def main():

    # CRITICAL! Checks if the ConditionalItems.plist already exists or not
    crowdstrike_id_dict= dict(crowdstrike_id = get_crowdstrike_id())
    if os.path.exists(conditionalitemspath):
        # "ConditionalItems.plist" exists, so read it FIRST (existing_dict)
        existing_dict = plistlib.readPlist(conditionalitemspath)
        # Create output_dict which joins new data generated in this script with existing data
        output_dict = dict(existing_dict.items() + crowdstrike_id_dict.items() ) 
    else:
        # "ConditionalItems.plist" does not exist,
        # output only consists of data generated in this script
        output_dict = crowdstrike_id_dict

        # Write out data to "ConditionalItems.plist"
    plistlib.writePlist(output_dict, conditionalitemspath)


if __name__ == '__main__':
    main()
