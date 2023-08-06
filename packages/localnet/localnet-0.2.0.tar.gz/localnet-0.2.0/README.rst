Module and script to test local network membership (IPv4)
===========================================================

A set of utility functions and a command-line script useful in testing local
machine membership in IPv4 networks. Requires no external modules
("batteries-included" only).

Command-line usage
++++++++++++++++++

#. Sample usage

Test all network interfaces, and return success if any interface has an IP
address in the 10.100.3.0/24 network:
   
   .. code-block:: bash
		   
      user@localhost$ local_net 10.100.3.0/24; echo $?
      0
      user@localhost$

Specific interfaces may be tested by inclusion of the -i/--iface flag, which
may be repeated:

   .. code-block:: bash
		
      user@localhost$ local_net -i etho -i wlan2 192.168.1.0/24

Asserting that no local interface is a member of a given network is also
possible by using the -n/--negate flag:

   .. code-block:: bash
		   
      user@localhost$ local_net -n 10.1.0.0/16


Test success or failure is indicated by exit status code - 0 for success, 1
for failure. This allows for ease of use in conditional statements and other
tests (e.g. ssh config 'exec' testing). Exit status 64 is returned if an
unrecoverable error occurs (e.g. an interface was passed that does not exist),
and error information may be written to stderr. Otherwise, no output is made.


Requirements and compatibility
++++++++++++++++++++++++++++++

The code should work on any POSIX-compatible system, but has only been tested
on modern Linux installs. Pull requests and bug reports for other operating
systems are welcome. Supports Python versions 2.6+.  Python versions < 3.3
require a system libc which supports if_nameindex() to get around lack of same
in socket module.
