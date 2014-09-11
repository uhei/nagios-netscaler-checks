#!/usr/bin/python
import sys
import time
from nsnitro import *
import argparse

outputstring="" 
critical=False
warning=False

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler vserver status')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nagios', help='Netscaler username')
	parser.add_argument('--password', metavar='PASSWORD', default='api_user', help='Netscaler password')
	parser.add_argument('--ssl', action="store_true", help='turn ssl on')
        parser.add_argument('-w', '--warning', metavar='WARNING', required=True, help='warning level for remaining days to expire')
        parser.add_argument('-c', '--critical', metavar='CRITICAL', required=True, help='critical level for remaining days to expire')
	parser.add_argument('--dargs', action='store_true', help='show args')
	
	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

	nitro = NSNitro(args.host, args.user, args.password, args.ssl)

	try:
		nitro.login()

		certkeys = NSSSLCertKey().get_all(nitro)
		for certkey in sorted(certkeys, key=lambda k: k.get_certkey()):
                    if ( int(certkey.get_daystoexpiration()) <= int(args.critical) ):
                            outputstring +=  certkey.get_certkey() + " expires in " + str(certkey.get_daystoexpiration()) + " Days "
                            critical = True
                    elif ( int(certkey.get_daystoexpiration()) <= int(args.warning) ):
                            outputstring +=  certkey.get_certkey() + " expires in " + str(certkey.get_daystoexpiration()) + " Days "
                            warning = True
		nitro.logout()

                if critical :
                    print "CRITICAL: " + outputstring
		    sys.exit(2)
                elif warning :
                    print "WARNING: " + outputstring
		    sys.exit(1)
                else :
                    print "OK: No Cert to expire"
		    sys.exit(0)

	except NSNitroError, e:
		print "Error: %s" % e.message
		sys.exit(3)
