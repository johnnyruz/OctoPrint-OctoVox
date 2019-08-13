# OctoPrint-OctoVox

The OctoVox plugin for OctoPrint sends limited printer information to a database for access via Amazon Echo devices. The problem with other Alexa solutions is that they require exposing access to your Octoprint server over the public internet as well as require providing the external service with your Octoprint API key.

The OctoVox plugin eliminates that security risk by publishing only small informational status updates about your printer that can then be retrieved by the Octovox Amazon Alexa Skill.

## OctoPrint Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/johnnyruz/OctoPrint-OctoVox/archive/master.zip

## OctoVox Plugin Configuration

1. Open the Settings tab of the OctoPrint-OctoVox Plugin
2. Enter a desired name for your printer
3. Click the ***Request Printer Registration*** button
4. You will be redirected to the OctoVox Login Page. If you do not yet have an account, click "Sign-Up" and enter a valid email address and create a password. You will have to verify your email address and then you will be directed to a page that will provide a unique key for your printer.
5. Enter that unique key in the box for Step 3 on the OctoVox Settings Page
6. Click the ***Verify Registration***
7. After the info is verified, click Save

## Alexa Setup 

1. Use the Alexa companion mobile app or website to enable the Octovox Skill. 
2. Once enabled, click on Settings and select Link Account.
3. Enter the Username and Password created in step 4 of the Plugin Configuration.
4. You can now ask Alexa for your printer status by saying "Alexa, ask my 3-D print server for my printer status"


## What Data is Stored in the OctoVox Database (Updated as of 7/29/2019)
 - Email address
 - Printer Name
 - Encrypted Printer Key Value
 - Printer Status (Offline, Operational, Printing, etc.)
 - Hot End Temperature
 - Bed Temperature
 - Current Job Completion Percentage
 - Current Job Z-height
 - Current Filename
 - Previous Job Duration
 - Previous Job Result (Completed, Cancelled, Failed, etc.)
 
_Printers and their status are removed from the database if they have not checked-in within 10 days_

