#!/usr/bin/python2.7

import os
import subprocess
import plistlib
import datetime

managedinstalldir = '/Library/Managed Installs/'
conditionalitemspath = os.path.join(managedinstalldir, 'ConditionalItems.plist')



def mac_chrome_extensions_facts():
  cmd='/usr/bin/find /Users/*/Library/Application\ Support/Google/Chrome/*/Extensions -name manifest.json'
  try:
    return [b for b in subprocess.check_output(cmd,universal_newlines=True,shell=True).split('\n')
if b ] 
  except:
    return []

def main():

    # CRITICAL! Checks if the ConditionalItems.plist already exists or not
    crx_ext_dict = dict(chrome_extensions = mac_chrome_extensions_facts()) 
    if os.path.exists(conditionalitemspath):
        # "ConditionalItems.plist" exists, so read it FIRST (existing_dict)
        existing_dict = plistlib.readPlist(conditionalitemspath)
        # Create output_dict which joins new data generated in this script with existing data
        output_dict = dict(existing_dict.items() + crx_ext_dict.items())
    else:
        # "ConditionalItems.plist" does not exist,
        # output only consists of data generated in this script
        output_dict = crx_ext_dict

        # Write out data to "ConditionalItems.plist"
    plistlib.writePlist(output_dict, conditionalitemspath)


if __name__ == '__main__':
    main()
