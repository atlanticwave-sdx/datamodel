class MongoCollections:
    TOPOLOGIES = "topologies"
    CONNECTIONS = "connections"
    BREAKDOWNS = "breakdowns"
    DOMAINS = "domains"
    LINKS = "links"
    PORTS = "ports"
    HISTORICAL_CONNECTIONS = "historical_connections"


class Constants:
    DOMAIN_LIST = "domain_list"
    LINK_CONNECTIONS_DICT = "link_connections_dict"
    PORT_CONNECTIONS_DICT = "port_connections_dict"
    LATEST_TOPOLOGY = "latest_topology"
    LATEST_TOPOLOGY_TS = "latest_topology_ts"
    TOPOLOGY_VERSION = "topology_version"


class MessageQueueNames:
    OXP_UPDATE = "oxp_update"
    CONNECTIONS = "connections"
    SDX_QUEUE_1 = "sdx_queue_1"
