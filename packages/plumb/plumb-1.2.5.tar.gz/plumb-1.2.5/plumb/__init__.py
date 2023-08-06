
# TODO: fix this doc to show the protocol, and the responsibilities of an
# implemnetation.
"""Fetch raw packages and push processed packages.

To fetch raw packages use a "Package Source" object, which handles a backend
connection and its configuration and exposes a "get()" method. Similarly, a
"Package Sink" object exposes a "put(pkg)" method.
"""
from plumb.factories import create_sinks_from_config, create_sources_from_config
