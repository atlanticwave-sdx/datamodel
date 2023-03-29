class DataModelException(Exception):
    """
    Base exception for topology data model functions.
    """

    pass


class MissingAttributeException(DataModelException):
    """
    A required attribute was missing when parsing a model element.
    """

    def __init__(self, data, attribute):
        """
        :param data: The data that is being parsed.
        :param attribute: The attribute that is required to be present.
        """
        self.data = data
        self.attribute = attribute

    def __str__(self):
        return (
            f"Missing required attribute '{self.attribute}' "
            f"while parsing <{self.data}>"
        )


class GraphNotConnectedException(DataModelException):
    """
    The topology is not connected.
    """

    def __init__(self, graph, connectivity):
        """
        :param graph: The graph that is being checked.
        :param connectivity: Connectivity status for the graph.
        """
        self.graph = graph
        self.connectivity = connectivity

    def __str__(self):
        return f"Graph <{self.graph}> is not connected: {self.connectivity}"
