#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.stat.system.system_stats import system_stats
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Check Netscaler Hardware')
	parser.add_argument('--host', metavar='HOSTNAME', required=True, help='Netscaler hostname')
	parser.add_argument('--user', metavar='USERNAME', default='nagios', help='Netscaler username')
	parser.add_argument('--password', metavar='PASSWORD', default='api_user', help='Netscaler password')
	parser.add_argument('--ssl', action="store_true", help='turn ssl on')
	parser.add_argument('--nosslverify', action="store_true", help='turn ssl verify off')
	parser.add_argument('-w', '--warning', metavar='WARNING', help='warning internal temp')
	parser.add_argument('-c', '--critical', metavar='CRITICAL', help='critcal internal temp')
	parser.add_argument('-m', '--model', choices=['mpx8005', 'mpx11500'], required=True, help='MPX model to check')

	parser.add_argument('--dargs', action='store_true', help='show service')

	args = parser.parse_args()
	if args.dargs:
		print(args)
		sys.exit(3)

	#general init
	ps1 = ps2 = ps3 = ps4 = cpufan0 = cpufan1 = inttemp = cpu0temp = cpu1temp = volt12 = volt5 = voltbat = fan = fan2 = False

	if args.model == 'mpx8005':
		ps1 = ps2 = cpufan0 = cpufan1 = inttemp = cpu0temp = volt12 = volt5 = voltbat = fan = True
	elif args.model == 'mpx11500':
		ps1 = ps2 = cpufan0 = cpufan1 = inttemp = cpu0temp = cpu1temp = volt12 = volt5 = voltbat = fan = fan2 = True

	errorstate = False
	warningstate = False
	outputstring = ""
	perfdatastring = ""


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
			obj = system_stats.get(nitro_session)
			for i in range(len(obj)) :
				# print("DEBUG: PS1:" + str(obj[i].powersupply1status) + " PS2:" + str(obj[i].powersupply2status) + " PS3:" + str(obj[i].powersupply3status) + " PS4:" + str(obj[i].powersupply4status) + " CPUFan0:" + str(obj[i].cpufan0speed) + " CPUFan1:" + str(obj[i].cpufan1speed) + " IntTemp:" + str(obj[i].internaltemp) + " CPU0Temp:" + str(obj[i].cpu0temp) + " CPU1Temp:" + str(obj[i].cpu1temp) + " Volt12:" + str(obj[i].voltagev12p) + " Volt5:" + str(obj[i].voltagev5p) + " VoltBat:" + str(obj[i].voltagevbat) + " Fan:" + str(obj[i].fanspeed) + " Fan2:" + str(obj[i].fan2speed) + " Fan3:" + str(obj[i].fan3speed) + " Fan4:" + str(obj[i].fan4speed) + " Fan5:" + str(obj[i].fan5speed) + " Aux0Temp:" + str(obj[i].auxtemp0) + " Aux1Temp:" + str(obj[i].auxtemp1) + " Aux2Temp:" + str(obj[i].auxtemp2) + " Aux3Temp:" + str(obj[i].auxtemp3))

				if ps1:
					if not str(obj[i].powersupply1status) == 'NORMAL':
						errorstate = True
					outputstring += "PS1: " + str(obj[i].powersupply1status)
				if ps2:
					if not str(obj[i].powersupply2status) == 'NORMAL':
						errorstate = True
					outputstring += ", PS2: " + str(obj[i].powersupply2status)
				if ps3:
					if not str(obj[i].powersupply3status) == 'NORMAL':
						errorstate = True
					outputstring += ", PS3: " + str(obj[i].powersupply3status)
				if ps4:
					if not str(obj[i].powersupply4status) == 'NORMAL':
						errorstate = True
					outputstring += ", PS3: " + str(obj[i].powersupply4status)
				if cpufan0:
					if not int(obj[i].cpufan0speed) > 1000:
						errorstate = True
					outputstring += ", CPUFan0: " + str(obj[i].cpufan0speed) +"rpm"
					perfdatastring += " 'cpufan0'=" + str(obj[i].cpufan0speed) + ";;1000;;"
				if cpufan1:
					if not int(obj[i].cpufan1speed) > 1000:
						errorstate = True
					outputstring += ", CPUFan1: " + str(obj[i].cpufan1speed) +"rpm"
					perfdatastring += " 'cpufan1'=" + str(obj[i].cpufan1speed) + ";;1000;;"
				if inttemp:
					if args.warning and args.critical:
						if int(obj[i].internaltemp) > int(args.warning):
							warningstate = True
						if int(obj[i].internaltemp) > int(args.critical):
							errorstate = True
					outputstring += ", InternalTemp: " + str(obj[i].internaltemp) +"°C"
					if args.warning and args.critical:
						perfdatastring += " 'inttemp'=" + str(obj[i].internaltemp) + ";" + args.warning + ";" + args.critical + ";;"
					else:
						perfdatastring += " 'inttemp'=" + str(obj[i].internaltemp) + ";;;;"
				if cpu0temp:
				    outputstring += ", CPU0Temp: " + str(obj[i].cpu0temp) +"°C"
				    perfdatastring += " 'cpu0temp'=" + str(obj[i].cpu0temp) + ";;;;"
				if cpu1temp:
				    outputstring += ", CPU1Temp: " + str(obj[i].cpu1temp) +"°C"
				    perfdatastring += " 'cpu1temp'=" + str(obj[i].cpu1temp) + ";;;;"
				if volt12:
					outputstring += ", PS +12V output: " + str(obj[i].voltagev12p) + "V"
					perfdatastring += " 'volt12'=" + str(obj[i].voltagev12p) + ";;;;"
				if volt5:
					outputstring += ", PS +5V output: " + str(obj[i].voltagev5p) + "V"
					perfdatastring += " 'volt5'=" + str(obj[i].voltagev5p) + ";;;;"
				if voltbat:
					outputstring += ", Battery output: " + str(obj[i].voltagevbat) + "V"
					perfdatastring += " 'voltbat'=" + str(obj[i].voltagevbat) + ";;;;"
				if fan:
					if not int(obj[i].fanspeed) > 1000:
						errorstate = True
					outputstring += ", Fan: " + str(obj[i].fanspeed) +"rpm"
					perfdatastring += " 'fan'=" + str(obj[i].fanspeed) + ";;1000;;"
				if fan2:
					if not int(obj[i].fan2speed) > 1000:
						errorstate = True
					outputstring += ", Fan2: " + str(obj[i].fan2speed) +"rpm"
					perfdatastring += " 'fan2'=" + str(obj[i].fan2speed) + ";;1000;;"
				
				nitro_session.logout()
				if errorstate:
					print("CRITICAL: " + outputstring + " | " + perfdatastring)
					sys.exit(2)
				elif warningstate:
					print("WARNING: " + outputstring + " | " + perfdatastring)
					sys.exit(1)
				elif not errorstate and not warningstate:
					print("OK: " + outputstring + " | " + perfdatastring)
					sys.exit(0)
				else:
					sys.exit(4)

		except nitro_exception as e :
			print("Exception::statsystem::errorcode="+str(e.errorcode)+",message="+ e.message)
		except Exception as e :
			print("Exception::statsystem::message="+str(e.args))
	except nitro_exception as e :
		print("Exception::statsystem::errorcode="+str(e.errorcode)+",message="+ e.message)
	except Exception as e :
		print("Exception::statsystem::message="+str(e.args))
