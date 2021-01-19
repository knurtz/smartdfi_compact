# SmartDFI_compact
Compact version of the original [smartDFI scripts](https://github.com/knurtz/smartdfi). Ready for running as a CGI script.

Instead of multiple background daemons waiting for new display data, the main program (html/cgi-bin/compact.py) is now invoked once and terminates after each transmission.
