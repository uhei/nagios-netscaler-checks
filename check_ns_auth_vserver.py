#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.config.authentication.authenticationvserver import authenticationvserver
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler authentication vserver status')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nagios', help='Netscaler username')
	parser.add_argument('--password', metavar='PASSWORD', default='api_user', help='Netscaler password')
	parser.add_argument('--ssl', action="store_true", help='turn ssl on')
	parser.add_argument('--nosslverify', action="store_true", help='turn ssl verify off')
        parser.add_argument('--vservername', metavar='LBVSERVERNAME', required=True, help='name of vserver; Use ALL to get a list of all vservers')

	parser.add_argument('--dargs', action='store_true', help='show service')

	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

#	nitro = NSNitro(args.host, args.user, args.password, args.ssl)
	if args.ssl:
		nitro_session = nitro_service(args.host, "HTTPS")
		if args.nosslverify:
			nitro_session.certvalidation = False
			nitro_session.hostnameverification = False
	else:
		nitro_session = nitro_service(args.host, "HTTP")

	nitro_session.set_credential(args.user, args.password)
	nitro_session.timeout = 310

	try:
		nitro_session.login()

		try :
			obj = authenticationvserver.get(nitro_session, name=args.vservername)
                        if (obj.curstate != "UP"):
                                print "CRITICAL: " + obj.name + " state: " + obj.curstate
                                nitro_session.logout()
                                sys.exit(2)
                        elif (obj.curstate == "UP"):
                                print "OK: " + obj.name + " state: " + obj.curstate + " | curusers=" + obj.curaaausers + ";;;;"
                                nitro_session.logout()
                                sys.exit(0)

		except nitro_exception as e :
			print("Exception::statsystem::errorcode="+str(e.errorcode)+",message="+ e.message)
			sys.exit(4)
		except Exception as e :
			print("Exception::statsystem::message="+str(e.args))
			sys.exit(4)
	except nitro_exception as e :
		print("Exception::statsystem::errorcode="+str(e.errorcode)+",message="+ e.message)
		sys.exit(4)
	except Exception as e :
		print("Exception::statsystem::message="+str(e.args))
		sys.exit(4)
