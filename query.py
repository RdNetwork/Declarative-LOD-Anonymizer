import xml.etree.ElementTree
from prefix import Prefix

class Query(object):
    """SPARQL query handling methods"""

    def __init__(self, select, where, filt=None):
        self.select = select
        self.where = where
        if filt is None:
            self.filt = []
        else:
            self.filt = filt

    def __str__(self):
        select_str = "SELECT "
        for var in self.select:
            select_str += var + " "
        return select_str + "WHERE { " + ' '.join(self.where) + "}"


    def evaluate(self, graph, prefixes):
        """
            Evaluates the SPARQL query for a given Query object.
            Return an iterable query result
        """
        select_str = "SELECT "
        for var in self.select:
            select_str += var + " "
        select_str += "\n"

        return graph.query(Prefix.writePrefixes(prefixes, "SPARQL") + select_str +
                           "WHERE { " + '\n'.join(self.where) + "}" +
                           "FILTER { " + self.filt.serialize(format="trig") + "}")


    @staticmethod
    def parse_gmark_queries(xml_file):
        """Converts an XML Gmark query node to a Query object."""
        res = []
        e = xml.etree.ElementTree.parse(xml_file).getroot()
        for q in e.findall('query'):
            query = Query([], [])
            if q.find('head') is not None:
                for v in q.find('head').findall('var'):
                    query.select.append(v.text)
            if q.find('bodies') is not None:
                for c in q.find('bodies').find('body').findall('conjunct'):
                    s = c.find('disj').find('concat').find('symbol')
                    if s.get('inverse') == 'true':
                        query.where.append(c.get('trg') + " " + s.text + " " + c.get('src')  + " .")
                    else:
                        query.where.append(c.get('src')  + " " + s.text + " " + c.get('trg')  + " .")
            res.append(query)
        return res
