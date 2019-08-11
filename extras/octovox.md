---
layout: plugin

id: octovox
title: OctoPrint-Octovox
description: OctoPrint plugin for Octovox
author: John Ruzick
license: AGPLv3

# TODO
date: 2019-07-29

homepage: https://github.com/johnnyruz/OctoPrint-Octovox
source: https://github.com/johnnyruz/OctoPrint-Octovox
archive: https://github.com/johnnyruz/OctoPrint-Octovox/archive/master.zip

# TODO
# Set this to true if your plugin uses the dependency_links setup parameter to include
# library versions not yet published on PyPi. SHOULD ONLY BE USED IF THERE IS NO OTHER OPTION!
#follow_dependency_links: false

# TODO
tags:
- octovox
- Amazon Echo
- Alexa
- Printer Status
- Printer Temperature

# TODO
screenshots:
- url: url of a screenshot, /assets/img/...
  alt: alt-text of a screenshot
  caption: caption of a screenshot
- url: url of another screenshot, /assets/img/...
  alt: alt-text of another screenshot
  caption: caption of another screenshot
- ...

# TODO
featuredimage: url of a featured image for your plugin, /assets/img/...

---

The Octovox plugin for OctoPrint sends limited printer information to a database for access via Amazon Echo devices. 
The problem with other Alexa solutions is that they require exposing access to your Octoprint server over the public internet 
as well as require providing the external service with your Octoprint API key.

The Octovox plugin eliminates that security risk by publishing only small informational status updates about your printer 
that can then be retrieved by the Octovox Amazon Alexa Skill. This plugin and Alexa Skill do not allow any manipulation or
control over your printer, it is entirely read-only and secured via user accounts.

## Installation

Installation is straightforward and broken down into easy steps on the plugin settings page.

1. Download and install this plugin either through the Plugin Repository or directly via the Github zip
2. Follow the steps on the Octovox settings screen in OctoPrint to setup your account and request a registration key for your printer
3. Enable the Octovox Skill from your Amazon Echo device or via the companion app
4. Link your account in the Alexa app
5. Ask Octovox for your status by asking "Alexa, ask Octovox for my printer status"

## Privacy

This plugin uses two external services to function. A user management and registration portal, and an API/Database to store printer information. 
Upon successful configuration, your OctoPrint server will occasionally publish updates to the service via the API. These updates are secured
using your unique printer API key. This is NOT your OctoPrint API key! At no point will you need to provide your OctoPrint API key or Url, and
you do not need to expose your server to the public.

Currently, the Octovox service stores the following information which can be retrieved by Alexa:
- Registration Email Address
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

Printers that have not updated their status in 10 days will automatically be removed from the database and will have to be re-registered 
