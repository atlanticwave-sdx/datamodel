## Table of Contents

- [How to Contribute](#contrib)
- [AW-SDX Data Model](#datamodel)
- [How to test and use](#usage)
- [AW-SDX Accompanying Projectsl](#accompany)

## <a name="contrib"></a>How to Contribute

1. Ensure you're able to run the existing code in your own [development environment](#setup).
2. Create a descriptive [GitHub issue](https://github.com/atlanticwave-sdx/datamodel/issues) that outlines what feature you plan to contribute.
3. Clone the repository, and start from the most recent version of the [develop branch](https://github.com/atlanticwave-sdx/datamodel/tree/develop).
4. Name your branch using the Github issue number as a prefix along with a brief name that corresponds to your feature (e.g., `8-how-to-contribute`).
5. Once satisfied with your completed and tested work, submit a [pull request](https://github.com/atlanticwave-sdx/datamodel/pulls) against the **develop** branch so that your code can be reviewed by the team.

Notes:

- Do not create a pull request against the **master** branch. The **master** branch is considered the production branch and must always remain stable. The **master** branch is periodically updated from the contents of the **develop** branch at the conclusion of a development cycle.
- Do not put any content (css, js, images, etc.) in the main `static` directory, instead create a directory named `static` in your app that can be imported into the main `static` directory using the `manage.py collectstatic` call.
- Use clear and concise naming conventions for apps, classes, functions, variables, etc. Ideally others will be able to reuse your work, and the more clear and concise your code is, the easier it is to reuse it.
- Include easy to understand documentation and complete unit/functional tests for each new feature being introduced to the project. ([pytest](https://docs.pytest.org/en/latest/) is the recommended framework to use for testing).

## <a name="datamodel"></a>AW-SDX Data Model

## System
Each domain, proxied by the customized SDX-LC who communicates between the SDX-controller and the domain (1) provisioning system (eg, Kytos) and (2) monitoring system (BAPM).

## Topology Models
In the whole SDX system, two types of topology models are needed: 
### Domain substrate description model
It's used by the intra-domain prvisioning system. 
### Domain declaration/advertisement model
Based on the information from the domain provisioning system, tt's abstracted/generated/passed by the SDX-LC to the SDX-controller for inter-domain topology assembly to support (a) inter-domain path computation; and (b) inter-domain path monitoring and reconfiguration. It would consist of three types of information: (1) Topology abstraction; (2) network resources available for inter-domain connections and their QoS metrics (eg, bw, latency, packet loss, vlan ranges, etc); (3) switching capability (eg, vlan, Q-in-Q, etc).

There is a *service* attribute in the topology object, which is an object that describes domain service meta information like owner, provisiong system, and security features. 

## Domain topology and state update
### Topology update:
On the events of addition, removal, and/or maintenance of ports, nodes, links, an updated domain topology with version and timestamp needs to be sent to the LC and subsequently the SDX controller. A new topology object is supposed to be generated and passed on to the SDX controller.

### Topology link state update
This set of updates mainly come from the domain monitoring system which is supposed to stream periodical measurement information on the links, like bandwidth, latency, and packet loss. A new link object is supposed to generated and pass on to the SDX controller.

## Topology description schemas
There are defined in the *schema* subfolder. Some attributes of each objects are requied (Can be found in the API definition) while some are optional. Two attributes are worth of mentioning: (1) In the *service* object, there is a *vender* attribute for the domain to list device vendors that are NOT in its domain, (2) in the topology, link, node, and port objects, there is an *private* attibute for the domain to list attributes that need to kept private.:wq
  
## <a name="usage"></a>Usage

### Running tests

Run tests with:

```
python -m pip install -r test-requirements.txt
python -m unittest
```

If you want to run some specific tests:

```
python -m unittest -v tests.test_topology_handler
python -m unittest -v tests.test_topology_validator
```

## Install
```
pip install -r requirements.txt
```
```
pip install -e .
```


## <a name="accompany"></a>Accompanying AW-SDX Projects
