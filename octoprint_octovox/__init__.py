# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import logging

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import RepeatedTimer
from .update_status import UpdateStatus

class OctovoxPlugin(octoprint.plugin.StartupPlugin,
		     octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.TemplatePlugin,
		     octoprint.plugin.EventHandlerPlugin):

	def __init__(self):
		super(OctovoxPlugin, self).__init__()
		self._updateStatusTimer = None
		self._update_status = UpdateStatus()


	##~~ StartupPlugin mixin

	def on_after_startup(self):
	        self._logger.info("OctoVox Is Alive!")
        	self._restart_timer()

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
			update_settings_interval=120,
			baseApiUrl="https://octovoxapi.azurewebsites.net",
			baseRegistrationUrl="https://octovox.auth.us-east-1.amazoncognito.com/login",
			registration_client_key="mqhq9vfgu4eq6t6f6usso7uik",
			printer_name=None,
			printer_uid=None,
			printer_is_registered=False,
			printer_last_update_result=None
		)

        def get_settings_restricted_paths(self):
		return dict(admin=[["printer_name"], ["printer_uid"], ["printer_is_registered"], ["printer_last_update_result"], ["update_settings_interval"],],
                		user=[[],],
                		never=[["baseApiUrl"], ["baseRegistrationUrl"], ["registration_client_key"],])

	def on_settings_save(self, data):
        	self._logger.info("saving settings")
		old_interval = self._settings.get_int(["update_settings_interval"])

        	octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        	new_interval = self._settings.get_int(["update_settings_interval"])

		if old_interval != new_interval:
			self._restart_timer()


	##~~ Asset Plugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/octovox.js"],
			css=["css/octovox.css"],
			less=["less/octovox.less"]
		)

	##~~ TemplatePlugin mixin

	def get_template_configs(self):
		return [
			dict(type="settings", name='OctoVox', custom_bindings=True)
		]

        ##~~ EventHandler Plugin

	def on_event(self, event, payload):
		if event == Events.PRINT_STARTED or event == Events.PRINT_DONE or event == Events.PRINT_FAILED or event == Events.PRINTER_STATE_CHANGED:
			self._update_status.handle_event(event, payload)
			#self._update_status.update_status(self._printer, self._settings)
			self._restart_timer()

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			octovox=dict(
				displayName="OctoVox Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="johnnyruz",
				repo="OctoPrint-OctoVox",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/johnnyruz/OctoPrint-OctoVox/archive/{target_version}.zip"
			)
		)

	##~~ Timer Functions

	def _restart_timer(self):
		# stop the timer
		if self._updateStatusTimer:
			self._logger.info(u"Stopping Timer...")
			self._updateStatusTimer.cancel()
			self.updateStatusTimer = None

		# start a new timer
		interval = self._settings.get_int(['update_settings_interval'])
		if interval:
			self._logger.info(u"Starting Timer...")
			self._updateStatusTimer = RepeatedTimer(interval, self.run_timer_job, None, None, True)
			self._updateStatusTimer.start()


	def run_timer_job(self):
		shouldRestartTimer = self._update_status.update_status(self._printer, self._settings)
		if (shouldRestartTimer == True):
			self._restart_timer()



# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "OctoVox Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = OctovoxPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
