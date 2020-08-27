# electrum-paranoid
This is an installer script for linux, which disables autoconnect (permanently) in electrum preventing any unintended information leakage.


The script
*  Downloads the newest version
*  Verifies the signature
*  Installs it into /usr/local/bin/electrum. This prevents any malware without root access to modify this in the future.  
   * uninstall with: `sudo pip uninstall electrum`
*  Mofifies /usr/local/bin/electrum  to 
   * disable autoconnect permanently
   * enable oneserver permanently
   * the server argument can still be set to allow for a custom electrum server

