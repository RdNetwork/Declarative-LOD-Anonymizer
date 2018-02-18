from prefix import Prefix

class Operation():
    """Anonymisation operations class and methods."""

    def __init__(self, head, body):
        self.head = head
        self.body = body

    def delete(self, graph, prefixes):
        """
            Performs a SPARQL deletion operation for a the given parameters.
            :param self: the Operation object used to get deletion parameters
            :param graph: Graph to be edited

            :return: The updated graph
        """
        return graph.update(Prefix.writePrefixes(prefixes, "SPARQL") + str(self))

    def __str__(self):
        return "DELETE { " + ' '.join(self.head)  + "} WHERE { " + ' '.join(self.body) + "}"

    def __repr__(self):
        return "\t\t" + self.__str__() + "\n"