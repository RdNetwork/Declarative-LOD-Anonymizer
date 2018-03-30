from prefix import Prefix

class Operation(object):
    """Anonymisation operations class and methods."""

    def __init__(self, del_head, upd_head, body):
        self.del_head = del_head
        self.upd_head = upd_head
        self.body = body

    def update(self, graph, prefixes):
        """
            Performs a SPARQL update operation for a the given parameters.
            :param self: the Operation object used to get parameters
            :param graph: Graph to be edited

            :return: The updated graph
        """
        return graph.update(Prefix.writePrefixes(prefixes, "SPARQL") + str(self))

    def __str__(self):
        res = "DELETE { " + ' '.join(self.del_head)  + "} "
        if self.upd_head:
            res = res + "INSERT { " + ' '.join(self.upd_head)  + "} "
        res = res + "WHERE { " + ' '.join(self.body) + "}"
        return res

    def __repr__(self):
        return "\t\t" + self.__str__() + "\n"

    def __eq__(self, other):
        return (self.del_head == other.del_head and 
            self.upd_head == other.upd_head and 
            self.body == other.body)
