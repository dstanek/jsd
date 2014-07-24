jsd - Declarative JSONSchema Generation
=======================================

.. WARNING:
   The is just a proof of concept right now.

This all started at the `OpenStack Juno design summit`. We had just begun
using JSONSchema in Keystone and I just couldn't believe how ugly it looked to
embed large schema dictionaries in code. After working with it I started to
see how it would be difficult to reason about large schemas if they were
dictionaries.

It seemed obvious there we were missing a declarative way to specify schemas!

.. image:: https://secure.travis-ci.org/dstanek/jsd.png

.. OpenStack Juno design summit: https://wiki.openstack.org/wiki/Summit/Juno
.. Keystone: http://docs.openstack.org/developer/keystone/
