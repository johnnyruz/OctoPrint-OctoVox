import json
import requests
import datetime

from octoprint.events import Events

class UpdateStatus:

	def __init__(self):
		self._statusItemIds = {
			'hotend_temp': 1,
			'bed_temp': 2,
			'printer_state': 3,
			'completion_percent': 4,
			'print_time_remaining': 5,
			'currentZ': 6,
			'file_name': 7,
			'last_print_time': 8,
			'last_print_result': 9
		}
		self._previousJobResult = ""
		self._failureCount = 0

	def handle_event(self, event, payload):
		if event == Events.PRINT_STARTED:
			self._previousJobResult = ""

		if event == Events.PRINT_DONE:
			self._previousJobResult = "Success"

		if event == Events.PRINT_FAILED:
			self._previousJobResult = payload['reason']

	def create_printer_registration(self, settings):

		self._logger.info("Requesting New Printer Id")

		path = "/api/CreatePrinterRegistration"

		try:
			r = requests.post(settings.get(['baseUrl']) + path)

			jsonResponse = r.json()

			if 'printerId' in jsonResponse:
				return jsonResponse['printerId']

		except BaseException as e:
			self._logger.error("Failed to Register a new ID (%s)" % str(e))

		return None

	def update_status(self, printer, settings):

		path = "/api/UpdatePrinterStatus"
		printerId = settings.get(['printer_uid'])
		printerName = settings.get(['printer_name'])

		if printerId:
			#self._logger.info("Updating Status %s" % printerId)
			printerStatus = printer.get_current_data()
			printerTemps = printer.get_current_temperatures()
			statusList = []

			if 'tool0' in printerTemps:
				if 'actual' in printerTemps['tool0']:
					if printerTemps['tool0']['actual'] is not None:
						temp = "{:.1f}".format(printerTemps['tool0']['actual'])
						statusList.append(dict(StatusTypeId=self._statusItemIds['hotend_temp'], StatusValue=temp))

			if 'bed' in printerTemps:
				if 'actual' in printerTemps['bed']:
					if printerTemps['bed']['actual'] is not None:
						temp = "{:.1f}".format(printerTemps['bed']['actual'])
						statusList.append(dict(StatusTypeId=self._statusItemIds['bed_temp'], StatusValue=temp))

			if 'state' in printerStatus:
                                if 'text' in printerStatus['state']:
                                        if printerStatus['state']['text'] is not None:
						statusList.append(dict(StatusTypeId=self._statusItemIds['printer_state'], StatusValue=printerStatus['state']['text']))

			if 'progress' in printerStatus:
                        	if 'completion' in printerStatus['progress']:
                                	if printerStatus['progress']['completion'] is not None:
                                        	perc = "{:.1f}".format(printerStatus['progress']['completion'])
						statusList.append(dict(StatusTypeId=self._statusItemIds['completion_percent'], StatusValue=perc))

				if 'printTimeLeft' in printerStatus['progress']:
					if printerStatus['progress']['printTimeLeft'] is not None:
						statusList.append(dict(StatusTypeId=self._statusItemIds['print_time_remaining'], StatusValue=printerStatus['progress']['printTimeLeft']))

			if 'currentZ' in printerStatus:
				if printerStatus['currentZ'] is not None:
					statusList.append(dict(StatusTypeId=self._statusItemIds['currentZ'], StatusValue=printerStatus['currentZ']))

			if 'job' in printerStatus:
				if 'file' in printerStatus['job']:
					if 'name' in printerStatus['job']['file']:
						if printerStatus['job']['file']['name'] is not None:
							statusList.append(dict(StatusTypeId=self._statusItemIds['file_name'], StatusValue=printerStatus['job']['file']['name']))
				if 'lastPrintTime' in printerStatus['job']:
					if printerStatus['job']['lastPrintTime'] is not None:
						timeRem = "{:.0f}".format(printerStatus['job']['lastPrintTime'])
						statusList.append(dict(StatusTypeId=self._statusItemIds['last_print_time'], StatusValue=timeRem))

			#Previous Job Status
			statusList.append(dict(StatusTypeId=self._statusItemIds['last_print_result'], StatusValue=self._previousJobResult))


			payload = dict(PrinterId=printerId, PrinterName=printerName, Details=statusList)
			headers = {'content-type': 'application/json'}


			try:
				r = requests.post(settings.get(['baseApiUrl']) + path, json=payload, headers=headers)
				jsonResponse = r.json()

				if 'apiResult' in jsonResponse:
					if not jsonResponse['apiResult'] == 'Success':
						if 'apiResultMessage' in jsonResponse:
							self._logger.error("Failed to update printer status: %s" % (jsonResponse['apiResultMessage']))
							settings.set(['printer_last_update_result'], 'ERROR: ' + jsonResponse['apiResultMessage'])
						else:
							self._logger.error("Failed to update printer status. Invalid Response from Server")
							settings.set(['printer_last_update_result'], 'ERROR')
						self._failureCount += 1
					else:
						self._failureCount = 0
						settings.set(['printer_last_update_result'], datetime.datetime.now())
			except BaseException as e:
				self._failureCount += 1
				self._logger.error("Failed to update printer status (%s)" % str(e))


			#Back-off frequency of updates if we encounter 10 failures in a row
			if (self._failureCount > 0 and self._failureCount % 10 == 0 and settings.get_int(['update_settings_interval']) < 300):

				currentInterval = settings.get_int(['update_settings_interval'])
				currentInterval *= 2

				if (currentInterval > 300):
					self._logger.info("OctoVox Backoff. New interval %i" % 300)
					settings.set(['update_settings_interval'], 300)
					settings.save()
					return True
				else:
					self._logger.info("OctoVox Backoff. New interval %i" % currentInterval)
					settings.set(['update_settings_interval'], currentInterval)
					settings.save()
					return True


		return False
