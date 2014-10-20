#!/usr/bin/python
import sys
import time
from nsnitro import *
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler vserver status')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nagios', help='Netscaler username')
	parser.add_argument('--password', metavar='PASSWORD', default='api_user', help='Netscaler password')
	parser.add_argument('--ssl', action="store_true", help='turn ssl on')
	parser.add_argument('--vservername', metavar='CSVSERVERNAME', required=True, help='name of CS vserver; Use ALL to get a list of all vservers')

	parser.add_argument('--dargs', action='store_true', help='show args')
	
	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

	nitro = NSNitro(args.host, args.user, args.password, args.ssl)

	try:
		nitro.login()

		if args.vservername == "ALL":
			vservers = NSCSVServer().get_all(nitro)
			for vserver in sorted(vservers, key=lambda k: k.get_name()):
				print vserver.get_name() + ": " + vserver.get_curstate()
			nitro.logout()
			sys.exit(3)

		if args.vservername:
			vserver = NSCSVServer()
			vserver.set_name(args.vservername)
			vserver = NSCSVServer().get(nitro, vserver)
			if (vserver.get_curstate() != "UP"):
				print "CRITICAL: " + vserver.get_name() + " state: " + vserver.get_curstate()
				nitro.logout()
				sys.exit(2)	
			elif (vserver.get_curstate() == "UP"):
				print "OK: " + vserver.get_name() + " state: " + vserver.get_curstate()
				nitro.logout()
				sys.exit(0)	

		print "Oops, something went wrong"
		sys.exit(3)

	except NSNitroError, e:
		print "Error: %s" % e.message
		sys.exit(3)
