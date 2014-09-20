#!/usr/bin/env python
 
## Tiny Syslog Server in Python.
##
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.
## That's it... it does nothing else...
## There are a few configuration parameters.

HOST, PORT = "0.0.0.0", 514
 
#
# NO USER SERVICEABLE PARTS BELOW HERE...
#

import win32evtlog
import win32evtlogutil
import SocketServer

logger_name = "Eventlog2Syslog"


class SyslogUDPHandler(SocketServer.BaseRequestHandler):
 
	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		print()
		win32evtlogutil.ReportEvent( 
                    logger_name, # Application name
                    1001, # Event ID
                    0, # Event category
                    win32evtlog.EVENTLOG_INFORMATION_TYPE,
                    (self.client_address[0], str(data)))
 
if __name__ == "__main__":
	try:
                win32evtlogutil.AddSourceToRegistry(logger_name)
		win32evtlogutil.ReportEvent( 
                    logger_name, # Application name
                    1001, # Event ID
                    0, # Event category
                    win32evtlog.EVENTLOG_INFORMATION_TYPE,
                    (logger_name, "Started."))
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
