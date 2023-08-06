INSTALLATION
------------
1)  Homebrew
  a) Install Homebrew (if you don't have it)
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  b) Update Homebrew
  brew update && brew upgrade
2) Install python3
  brew install python
3) Install package
  pip install macvpnhelper

Now you can just type "macvpnhelper" in the terminal.

Alternatively, you can run the script located in this package directly. It is located in the bin/ folder.
  ./macvpnhelper


USAGE
-----
macvpnhelper [-h] [--duration DURATION] [--clickspeed CLICKSPEED]
                    [--fillpassword FILLPASSWORD] [--simulate] [--reset]
                    [--vpn VPN]

optional arguments:
  -h, --help            show this help message and exit
  --duration DURATION, -d DURATION
                        (time in hours|'wd'|'fd') E.g., 8h, the amount of time
                        (in hours) to keep the VPN active. Use 'wd' to do 9-12
                        and 1-6 (default), or 'fd' to do 9-6.
  --clickspeed CLICKSPEED, -cs CLICKSPEED
                        (superfast|fast|normal|slow|superslow) adjust based on
                        responsiveness of your GUI
  --fillpassword FILLPASSWORD, -fp FILLPASSWORD
                        (yes|no|andReturn) type in password and optionally hit
                        return in the dialogs. CAUTION: since this password is
                        provided to the GUI, it is possible that intermediate
                        clicks will result in your password being typed to,
                        e.g., chat dialogs. Prevent this by using 'yes'
                        instead of 'andReturn', or making sure the clickspeed
                        matches your GUI responsiveness.
  --simulate, -s        When set, script which would be executed is instead
                        printed to the terminal.
  --reset               Use to reset your login information.
  --vpn VPN, -n VPN     Name of VPN to connect to. Must match your configured
                        connection.
