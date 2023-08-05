PYHPEIMC Python project
=======================

A sample project that exists as an aid for HPE IMC customers to access the RESTFUL API (eAPI) of the Network Management
System Natively from within python.

For example usages, please see the

This project is offered under and Apache2 license and is not supported officialy by HPE.

For more information, please visit the project home page at `GITHub.com <https://github.com/HPENetworking/PYHPEIMC>`_.


What's Changed:

1.0.1 Fixed Readme File
1.0.2 Fixed setup.py to remove unnecessary data directory
1.0.3 Issue with plat.device.set_interface_down function. fixed
1.0.4/5 - Changed library name for HP branding
1.0.6 - Added get_dev_mac_learn function to pyhpeimc.plat.device
1.0.7 - Added run_dev_cmd function to pyhpeimc.plat.device
1.0.8 - Squashed bugs
1.0.9 - Squashed more bugs
1.0.10 - And yet more bugs
1.0.11 - And yet more bugs
1.0.12 - Changed output of pyhpeimc.plat.device.run_dev_cmd to include full response
1.0.13 - Added plat.auth.test_imc_creds function
1.0.14 - Removed Jupyter dependency
1.0.15 - Added icc module under plat. Added various configuration template functions to icc module
1.0.16 - Added version function. Modified create_custom_view to remove unnecessary output.
1.0.17 - Added netassets, VRM, and WSM functions
1.0.18 - Forced return of get_real_time_locate function to be a list
1.0.19 - Added objects module and IMCDev and IMCInt classes for usability
1.0.20 - Modified get_plat_operator function to always returns object of type list
         Added Object Class for IPScopes ( termimal access IP Address Management ) and supporting functions in plat.termaccess
1.0.21 - Fixed bug in addip method of IPScope class
1.0.22 - Added deallocate hostip method to IPScope class with supporting functions in plat.termaccess
1.0.23 - Added Sphinx docs project, Improved Docstrings
1.0.24 - Bug Fixes
1.0.25 - Continuing to add docstrings and fixed bug in pyhpeimc.plat.operators get_plat_operators which was returning inconsistently
1.0.26 - Paying some technical debt. Added perf module and intial add_per_task function
1.0.27 - Paying some more technical debt. Added functions to plat.alarms module
1.0.28 - Bug Fixes
1.0.29 - More bug Fixes. Added functions in groups and devices to support adding device sto custom views
1.0.30 - Added functions to pull system vendors, categories, and device models
1.0.33 - Bug Fixes, Added function.
1.0.34 - Refactored doctests for all modules to improve coverage and stability
1.0.35 - Refactored nosetests for all modules to improve coverage and stability. Modifications to functions which take devid as input too allow ipaddress directly
1.0.36 - Added functions to vlanm for hybrid ports and access vlans. with applicable tests
1.0.37 - refactored nose test and continued pep8 compatibility
1.0.38 - Added Telnet Template CRUD operations, Added Alarm Ack and Recover and Get Alarm details
 capabilties
1.0.39 - Fixed pyhpeimc.objects broken class objects.
1.0.40 - Fixed getvlan() addvlan() and delvlan() methods on pyhpeimc.objects IMCDev class
1.0.41 - Bugfixes for pyhpeimc.objects classes. Adding additional tests.
