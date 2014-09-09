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
	parser.add_argument('--vservername', metavar='LBVSERVERNAME', required=True, help='name of vserver; Use ALL to get a list of all vservers')

	parser.add_argument('--dargs', action='store_true', help='show args')
	
	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

	nitro = NSNitro(args.host, args.user, args.password, args.ssl)

	try:
		nitro.login()

		if args.vservername == "ALL":
			vservers = NSLBVServer().get_all(nitro)
			for vserver in sorted(vservers, key=lambda k: k.get_name()):
				print vserver.get_name() + ": " + vserver.get_effectivestate() + "; Health: " + vserver.get_health() + "%"
			nitro.logout()
			sys.exit(3)

		if args.vservername:
			vserver = NSLBVServer()
			vserver.set_name(args.vservername)
			vserver = NSLBVServer().get(nitro, vserver)
			if (vserver.get_effectivestate() != "UP") | (int(vserver.get_health()) == 0):
				print "CRITICAL: " + vserver.get_name() + " state: " + vserver.get_effectivestate() + ", Health: " + vserver.get_health() + \
					"% | health=" + vserver.get_health() + "%;;;;"
				nitro.logout()
				sys.exit(2)	
			elif int(vserver.get_health()) < 100:
				print "WARNING: " + vserver.get_name() + " state: " + vserver.get_effectivestate() + ", Health: " + vserver.get_health() + \
					"% | health=" + vserver.get_health() + "%;;;;"
				nitro.logout()
				sys.exit(1)	
			elif (vserver.get_effectivestate() == "UP") & (int(vserver.get_health()) == 100):
				print "OK: " + vserver.get_name() + " state: " + vserver.get_effectivestate() + ", Health: " + vserver.get_health() + \
					"% | health=" + vserver.get_health() + "%;;;;"
				nitro.logout()
				sys.exit(0)	

		print "Oops, something went wrong"
		sys.exit(3)

	except NSNitroError, e:
		print "Error: %s" % e.message
		sys.exit(3)
