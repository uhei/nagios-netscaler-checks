#!/usr/bin/python
import sys
import time
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.stat.basic.service_stats import service_stats
from nssrc.com.citrix.netscaler.nitro.resource.stat.basic.servicegroupmember_stats import servicegroupmember_stats
from nssrc.com.citrix.netscaler.nitro.resource.stat.lb.lbvserver_stats import lbvserver_stats
from nssrc.com.citrix.netscaler.nitro.resource.stat.network.Interface_stats import Interface_stats
from nssrc.com.citrix.netscaler.nitro.resource.stat.ns.ns_stats import ns_stats
from nssrc.com.citrix.netscaler.nitro.resource.stat.system.system_stats import system_stats
from nssrc.com.citrix.netscaler.nitro.resource.stat.vpn.vpn_stats import vpn_stats
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
import argparse
import datetime

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler CPU usage (in percent)')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nagios', help='Netscaler username')
	parser.add_argument('--password', metavar='PASSWORD', default='api_user', help='Netscaler password')
	parser.add_argument('--ssl', action="store_true", help='turn ssl on')
	parser.add_argument('-w', '--warning', metavar='WARNING', help='warning')
	parser.add_argument('-c', '--critical', metavar='CRITICAL', help='critcal')

	parser.add_argument('--dargs', action='store_true', help='show service')
	
	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

#	nitro = NSNitro(args.host, args.user, args.password, args.ssl)
	if args.ssl:
		nitro_session = nitro_service(args.host, "HTTPS")
		nitro_session.certvalidation = False
		nitro_session.hostnameverification = False
	else:
		nitro_session = nitro_service(args.host, "HTTP")

	nitro_session.set_credential(args.user, args.password)
	nitro_session.timeout = 310

	try:
		nitro_session.login()
                try :
                        obj = ns_stats.get(nitro_session)
                        for i in range(len(obj)) :
				if  args.warning and args.critical:
					if ( float(obj[i].cpuusagepcnt) >= float(args.critical) ) or ( float(obj[i].pktcpuusagepcnt) >= float(args.critical) ):
						print("CRITICAL: CPU " + str(obj[i].cpuusagepcnt) + "%, PE CPU " + str(obj[i].pktcpuusagepcnt) + "% | 'cpu'=" + str(obj[i].cpuusagepcnt) + "%;" + args.warning + ";" + args.critical + ";; 'pecpu'=" + str(obj[i].pktcpuusagepcnt) + "%;" + args.warning + ";" + args.critical + ";;")
						nitro_session.logout()
						sys.exit(2)
					elif ( float(obj[i].cpuusagepcnt) >= float(args.warning) ) or ( float(obj[i].pktcpuusagepcnt) >= float(args.warning) ):
						print("WARNING: CPU " + str(obj[i].cpuusagepcnt) + "%, PE CPU " + str(obj[i].pktcpuusagepcnt) + "% | 'cpu'=" + str(obj[i].cpuusagepcnt) + "%;" + args.warning + ";" + args.critical + ";; 'pecpu'=" + str(obj[i].pktcpuusagepcnt) + "%;" + args.warning + ";" + args.critical + ";;")
						nitro_session.logout()
						sys.exit(1)
					else:
						print("OK: CPU " + str(obj[i].cpuusagepcnt) + "%, PE CPU " + str(obj[i].pktcpuusagepcnt) + "% | 'cpu'=" + str(obj[i].cpuusagepcnt) + "%;" + args.warning + ";" + args.critical + ";; 'pecpu'=" + str(obj[i].pktcpuusagepcnt) + "%;" + args.warning + ";" + args.critical + ";;")
						nitro_session.logout()
						sys.exit(0)
				else:
					print("OK: CPU " + str(obj[i].cpuusagepcnt) + "%, PE CPU " + str(obj[i].pktcpuusagepcnt) + "% | 'cpu'=" + str(obj[i].cpuusagepcnt) + "%;;;; 'pecpu'=" + str(obj[i].pktcpuusagepcnt) + "%;;;;")
					nitro_session.logout()
					sys.exit(0)
				
                except nitro_exception as e :
                        print("Exception::statsystem::errorcode="+str(e.errorcode)+",message="+ e.message)
                except Exception as e :
                        print("Exception::statsystem::message="+str(e.args))
	except nitro_exception as e :
		print("Exception::statsystem::errorcode="+str(e.errorcode)+",message="+ e.message)
	except Exception as e :
		print("Exception::statsystem::message="+str(e.args))
