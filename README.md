The Python scripts in this repository can be used to collect
diagnostic information about your system and post them as anonymous
public gists at http://gist.github.com/.

# Neutron configuration dump

The `neutron-gist.py` script will gather neutron configuration
information from the perspective of your current OpenStack
credentials.

Run it like this:

    ./neutron-gist.py | ./create-gist.py

This will return the URL to the created gist (or, if there are any
problems, it will simply blow up with a Python exception).

# Network configuration dump

The `network-gist.py` script will gather information about the network
configuration of your system.  It must be run with `root` privileges,
like this:

    sudo ./network-gist.py | ./create-gist.py

# Obfuscating data

If you wish to obfuscate ip addresses or anything else before
uploading the data you can insert `sed` (or another tool of your
choice) into the pipeline.  For example, to transform all ip addresses
of the form 10.1.3.nnn into x.x.x.nnn:

    sudo ./network-gist.py |
      sed 's/10.1.3.\([0-9]*\)/x.x.x.\1/g' |
      ./create-gist.py

