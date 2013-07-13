Tribes That May Be
==================

Tribes That May Be is an interactive fiction in the middle of the desert art which my partner and I are bringing with us to Burning Man this year. 

This repository contains all the fiddly bits which will make our solar powered raspberry pi based WiFi access point work properly.

Features
--------

* Ansible deployment on top of recent raspbian distribution
* Hostap configured for RTL8188RU USB WiFi dongle
* Dnsmasq configured to redirect all traffic to a locally served DNS. No actual internet access.
* Nginx serving up Parchment with a hard-coded story.

Install Notes
-------------

* requires ansible 1.2
* sshpass is needed locally if not using ssh keys
