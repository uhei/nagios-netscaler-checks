#!/usr/bin/env python
import sys
import time
from nsnitro import *
import argparse
import datetime

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler HA status')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nagios', help='Netscaler username')
	parser.add_argument('--password', metavar='PASSWORD', default='api_user', help='Netscaler password')
	parser.add_argument('--ssl', action="store_true", help='turn ssl on')
	parser.add_argument('-w', '--warning', metavar='WARNING', help='seconds since last change')

	parser.add_argument('--dargs', action='store_true', help='show args')
	
	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

	nitro = NSNitro(args.host, args.user, args.password, args.ssl)

	try:
		nitro.login()
		
		node = NSHANode()
		node.set_id("0")
		node = NSHANode.get(nitro, node)
		status = node.get_hastatus()
		state = node.get_state().lower()
		if status != "UP":
			print "CRITICAL: " + node.get_name() + " " + status
			nitro.logout()
			sys.exit(2)
		elif ( status == "UP") & (  state == "primary"):
			if args.warning:
				if int(node.get_masterstatetime()) <= int(args.warning):
					print "WARNING: " + node.get_name() + " " + status + " " + node.get_state() + " since " + str(datetime.timedelta(seconds=node.get_masterstatetime()))
					nitro.logout()
					sys.exit(1)

			print "OK: " + node.get_name() + " " + status + " " + node.get_state() + " since " + str(datetime.timedelta(seconds=node.get_masterstatetime()))
			nitro.logout()
			sys.exit(0)
		elif status == "UP":
			print "OK: " + node.get_name() + " " + status + " " + node.get_state()
			nitro.logout()
			sys.exit(0)
			
			
		nitro.logout()
		sys.exit(3)

	except NSNitroError, e:
		print "Error: %s" % e.message
		sys.exit(3)
