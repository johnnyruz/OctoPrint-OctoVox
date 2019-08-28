# OctoPrint-OctoVox

The OctoVox plugin for OctoPrint sends limited printer information to a database for access via Amazon Echo and Google Home devices. The problem with other voice solutions is that they require exposing access to your OctoPrint server over the public internet as well as require providing the external service with your OctoPrint API key.

The OctoVox plugin eliminates that security risk by publishing only small informational status updates about your printer that can then be retrieved by the Octovox Amazon Alexa Skill or the My Three D Printer Google Action.

## A Note about Naming Conventions

Amazon calls their Voice Applications "Skills", while Google calls their Voice Applications "Actions".

For Alexa Skills, Amazon allows your Skill Name to be different than your Invocation phrase, so you will see the Alexa Skill listed in the store under the appropriate name of "Octovox". However, the invocation name cannot be one word, so in order to activate the skill the required phrase has been configured as "My 3D Print Server". For example, "Alexa, ask my 3D Print Server for Status".

Google Actions uses the Action Name as the Invocation phrase so they cannot be different. They enforce a requirement that the Invocation Phrase cannot be one word. In order to keep the Invocation Phrase consistient between platforms, you will see the OctoVox Google Action listed under the name "My Three D Print Server" in the Assistant App and Assistant Directory. You can then interact via the phrase "OK, Google, ask my 3D Print Server for Status".

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

## Google Assistant Setup

1. Ask any Google Home device or the Assistant App on mobile to "Talk to My 3D Print Server" 
2. When you ask for your Printer Status, the Action will prompt you to link your OctoVox account with Google
3. If you respond "Yes" to the Link Account question, you will be directed to the login page on your mobile device.
4. Enter the Username and Password created in step 4 of the Plugin Configuration.
5. You can now ask the Google Assistant for your printer status by saying "OK Google, ask my 3D print server for my printer status"

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

