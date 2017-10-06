#!/usr/bin/env python
import sys
import time
from massrc.com.citrix.mas.nitro.exception.nitro_exception import nitro_exception
from massrc.com.citrix.mas.nitro.resource.config.mps.mps_health import mps_health
from massrc.com.citrix.mas.nitro.service.nitro_service import nitro_service
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler MAS health')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler MAS hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nagios', help='Netscaler MAS username')
	parser.add_argument('--password', metavar='PASSWORD', default='api_user', help='Netscaler MAS password')
	parser.add_argument('--ssl', action="store_true", help='turn ssl on')
	parser.add_argument('--nosslverify', action="store_true", help='turn ssl verify off')
	parser.add_argument('-w', '--warning', metavar='WARNING', help='warning')
	parser.add_argument('-c', '--critical', metavar='CRITICAL', help='critcal')

	parser.add_argument('--dargs', action='store_true', help='show service')

	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

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
			obj = mps_health.get(nitro_session)
			for i in range(len(obj)) :
				if  args.warning and args.critical:
					if ( float(obj[i].cpu_usage) >= float(args.critical) ) or ( float(obj[i].disk_usage) >= float(args.critical) ) or ( float(obj[i].memory_usage) >= float(args.critical) ):
						print("CRITICAL: CPU " + str(obj[i].cpu_usage) + "%, Disk " + str(obj[i].disk_usage) + "%, Memory " + str(obj[i].memory_usage) + "% | 'cpu'=" + str(obj[i].cpu_usage) + "%;" + args.warning + ";" + args.critical + ";; 'disk'=" + str(obj[i].disk_usage) + "%;" + args.warning + ";" + args.critical + ";; 'memory'=" + str(obj[i].memory_usage) + "%;" + args.warning + ";" + args.critical + ";;")
						nitro_session.logout()
						sys.exit(2)
					elif ( float(obj[i].cpu_usage) >= float(args.warning) ) or ( float(obj[i].disk_usage) >= float(args.warning) ) or ( float(obj[i].memory_usage) >= float(args.warning) ):
						print("WARNING: CPU " + str(obj[i].cpu_usage) + "%, Disk " + str(obj[i].disk_usage) + "%, Memory " + str(obj[i].memory_usage) + "% | 'cpu'=" + str(obj[i].cpu_usage) + "%;" + args.warning + ";" + args.critical + ";; 'disk'=" + str(obj[i].disk_usage) + "%;" + args.warning + ";" + args.critical + ";; 'memory'=" + str(obj[i].memory_usage) + "%;" + args.warning + ";" + args.critical + ";;")
						nitro_session.logout()
						sys.exit(1)
					else:
						print("OK: CPU " + str(obj[i].cpu_usage) + "%, Disk " + str(obj[i].disk_usage) + "%, Memory " + str(obj[i].memory_usage) + "% | 'cpu'=" + str(obj[i].cpu_usage) + "%;" + args.warning + ";" + args.critical + ";; 'disk'=" + str(obj[i].disk_usage) + "%;" + args.warning + ";" + args.critical + ";; 'memory'=" + str(obj[i].memory_usage) + "%;" + args.warning + ";" + args.critical + ";;")
						nitro_session.logout()
						sys.exit(0)
				else:
					print("OK: CPU " + str(obj[i].cpu_usage) + "%, Disk " + str(obj[i].disk_usage) + "%, Memory " + str(obj[i].memory_usage) + "% | 'cpu'=" + str(obj[i].cpu_usage) + "%;;;; 'disk'=" + str(obj[i].disk_usage) + "%;;;; 'memory'=" + str(obj[i].memory_usage) + "%;;;;")
					nitro_session.logout()
					sys.exit(0)
				
		except nitro_exception as e :
			print("Exception::nitro_exceptione::errorcode="+str(e.errorcode)+",message="+ e.message)
		except Exception as e :
			print("Exception::message="+str(e.args))
	except nitro_exception as e :
		print("Exception::nitro_exception::errorcode="+str(e.errorcode)+",message="+ e.message)
	except Exception as e :
		print("Exception::message="+str(e)+str(e.message)+str(e.args))
