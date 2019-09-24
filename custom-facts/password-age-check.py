#!/usr/bin/python2.7

import os
import subprocess
import plistlib
import datetime

managedinstalldir = '/Library/Managed Installs/'
conditionalitemspath = os.path.join(managedinstalldir, 'ConditionalItems.plist')

def get_date_changed(username, creation_date=None):
    '''Gets the date of last password change'''
    # return None
    # for 10.10+ or non-migrated accounts
    task = subprocess.check_output(['/usr/bin/dscl', '.', 'read', 'Users/' + username, 'accountPolicyData'])
    plist = plistlib.readPlistFromString('\n'.join(task.split()[1:]))
    if 'creationTime' in plist.keys():
        creation_date = datetime.datetime.utcfromtimestamp(plist['creationTime']).date()
    if 'passwordLastSetTime' in plist.keys():
        return datetime.datetime.utcfromtimestamp(plist['passwordLastSetTime']).date()
    else:
        # for 10.9.x and lower, or migrated accounts
        task = subprocess.Popen(['/usr/bin/dscl', '.', 'read', 'Users/' + username, 'PasswordPolicyOptions'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out, err) = task.communicate()
        if not err:
            plist = plistlib.readPlistFromString('\n'.join(out.split()[1:]))
            if 'passwordLastSetTime' in plist.keys():
                return plist['passwordLastSetTime'].date()
    return creation_date

def main():
    # Obtain username from last logged in user
    username = plistlib.readPlistFromString(subprocess.check_output(['/usr/bin/syslog', '-F', 'xml', '-k', 'Facility', 'com.apple.system.lastlog', '-k', 'Sender', 'loginwindow']))[-1]['ut_user']
    # username = 'luser'
    if username:
        changed = get_date_changed(username)
        if changed:
            today = datetime.datetime.utcnow().date()
            pw_age = (today - changed).days
            # Create a dictionary with the key/value pair(s) to add to the ConditionalItems.plist
            passwordinfo_dict = dict(password_age = pw_age,password_check = "True")

        else:
            passwordinfo_dict = dict(password_check = "False")

                # CRITICAL! Checks if the ConditionalItems.plist already exists or not
        if os.path.exists(conditionalitemspath):
            # "ConditionalItems.plist" exists, so read it FIRST (existing_dict)
            existing_dict = plistlib.readPlist(conditionalitemspath)
            # Create output_dict which joins new data generated in this script with existing data
            output_dict = dict(existing_dict.items() + passwordinfo_dict.items())
        else:
            # "ConditionalItems.plist" does not exist,
            # output only consists of data generated in this script
            output_dict = passwordinfo_dict

        # Write out data to "ConditionalItems.plist"
        plistlib.writePlist(output_dict, conditionalitemspath)


if __name__ == '__main__':
    main()
