# AtlanticWave-SDX Data Model

## System

Each domain, proxied by the customized SDX-LC who communicates between
the SDX-controller and the domain (1) provisioning system (eg, Kytos)
and (2) monitoring system (BAPM).

## Topology Models

In the whole SDX system, two types of topology models are needed: 

### Domain substrate description model

It's used by the intra-domain prvisioning system. 

### Domain declaration/advertisement model

Based on the information from the domain provisioning system, tt's
abstracted, generated, and passed by SDX-LC to the SDX-controller for
inter-domain topology assembly to support (a) inter-domain path
computation; and (b) inter-domain path monitoring and
reconfiguration. 

It would consist of three types of information: 

1. Topology abstraction

2. Network resources available for inter-domain connections and their
QoS metrics (eg, bw, latency, packet loss, vlan ranges, etc)

3. Switching capability (eg, vlan, Q-in-Q, etc).

There is a `service` attribute in the topology object, which is an
object that describes domain service meta information like owner,
provisiong system, and security features.

## Domain topology and state update

### Topology update:

On the events of addition, removal, and/or maintenance of ports,
nodes, links, an updated domain topology with version and timestamp
needs to be sent to the LC and subsequently the SDX controller. A new
topology object is supposed to be generated and passed on to the SDX
controller.

### Topology link state update

This set of updates mainly come from the domain monitoring system
which is supposed to stream periodical measurement information on the
links, like bandwidth, latency, and packet loss. A new link object is
supposed to generated and pass on to the SDX controller.


## Topology description schemas

There are defined in the `schema` subfolder. Some attributes of each
objects are requied (Can be found in the API definition) while some
are optional. Two attributes are worth of mentioning: 

1. In the `service` object, there is a `vendor` attribute for the
domain to list device vendors that are NOT in its domain.

2. In topology, link, node, and port objects, there is a `private`
attibute for the domain to list attributes that need to kept private.
  
## Using the library

### Running tests

When developing and testing datamodel, using a virtual environment is
a good idea, like so:

```console
$ git clone https://github.com/atlanticwave-sdx/datamodel.git
$ cd datamodel
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --editable .[test]
```

To run tests, use pytest:

```console
$ pytest
```

Or use Python's unittest module:

```console
$ python -m unittest
```

If you want to run some specific tests:

```console
$ python -m unittest -v tests.test_topology_handler
$ python -m unittest -v tests.test_topology_validator
```

## Installing datamodel

You can install datamodel direct from the git repository:

```console
$ pip install git+https://github.com/atlanticwave-sdx/datamodel@main
```

