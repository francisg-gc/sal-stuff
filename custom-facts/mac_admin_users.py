#!/usr/bin/python2.7

import os
import grp
import plistlib
import datetime

managedinstalldir = '/Library/Managed Installs/'
conditionalitemspath = os.path.join(managedinstalldir, 'ConditionalItems.plist')

def get_mac_admin_users():
  try:
    return grp.getgrgid(80)[3]
  except:
    return []

def main():

    new_dict = dict( mac_admin_users = get_mac_admin_users() ) 

    # CRITICAL! Checks if the ConditionalItems.plist already exists or not
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
