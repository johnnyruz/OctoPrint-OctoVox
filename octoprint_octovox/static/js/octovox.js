/*
 * View model for OctoPrint-OctoVox
 *
 * Author: John Ruzick
 * License: Apache-2.0
 */
$(function() {
    function OctovoxViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        self.settingsViewModel = parameters[0];

        self.testActive = ko.observable(false);
        self.testResult = ko.observable(false);
        self.testSuccessful = ko.observable(false);
        self.testMessage = ko.observable();
		
	self.requestActive = ko.observable(false);
        self.requestResult = ko.observable(false);
        self.requestMessage = ko.observable();
				
	self.requestRegistration = function() {
			
            self.requestResult(false);
            self.requestMessage("");
			
			var printer_name = $('#printer_name').val();
			
			if(printer_name !== null && printer_name !== '') {
				
				self.settings.plugins.octovox.printer_is_registered(false);
				
				var payload = {
					PrinterName: printer_name,
					PrinterId: printer_uid
				};
				
				var url = self.settings.plugins.octovox.baseRegistrationUrl() + 
					"?response_type=code" +
					"&client_id=" + self.settings.plugins.octovox.registration_client_key() +
					"&redirect_uri=" + self.settings.plugins.octovox.baseApiUrl() + "/api/CreatePrinterRegistration" +
					"&state=" + printer_name;
				
				var win = window.open(url, '_blank');
				win.focus();
				
				self.requestResult(true);
				
			}
			else{
				self.requestResult(true);
				self.requestMessage("Please enter a valid Printer Name");
			}			
		};

        self.verifyRegistration  = function() {
            self.testActive(true);
            self.testResult(false);
            self.testSuccessful(false);
            self.testMessage("");
						

            var printer_name = $('#printer_name').val();
            var printer_uid = $('#printer_uid').val();

			if(printer_name !== null && printer_name !== '' && printer_uid !== null && printer_uid !== '') {

				var payload = {
					PrinterName: printer_name,
					PrinterId: printer_uid
				};

				$.ajax({
					url: self.settings.plugins.octovox.baseApiUrl()  + "/api/VerifyPrinterRegistration",
					type: "POST",
					dataType: "json",
					data: JSON.stringify(payload),
					contentType: "application/json; charset=UTF-8",
					success: function(response) {
						self.testResult(true);
						
						if (response.apiResult == "Success"){
							self.testSuccessful(true);
							self.testMessage("Printer successfully registered!");
							
							self.settings.plugins.octovox.printer_is_registered(true);							
						}
						else{
							self.testSuccessful(false);
							self.testMessage("Printer Registration Not Found!");
						}					
					},
					complete: function() {
						self.testActive(false);
					}
				});
			}
			else{
				self.testSuccessful(false);
				self.testActive(false);
				self.testResult(true);
				self.testMessage("Please enter a valid Printer Name and Printer Id");
			}
        };

        self.onBeforeBinding = function() {
            self.settings = self.settingsViewModel.settings;
			
			if (self.settings.plugins.octovox.printer_is_registered()){
				self.testMessage("Printer successfully registered!");
			}
			
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: OctovoxViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_octovox, #tab_plugin_octovox, ...
        elements: [ "#settings_plugin_octovox" ]
    });
});
