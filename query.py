import xml.etree.ElementTree
from prefix import Prefix
import fyzz

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

    @staticmethod
    def parse_txt_queries(p_pol_size, u_pol_size):
        """Parses textual policies files to a set of queries"""
        root_path = "./conf/workloads/policies/"
        queries_str = []
        for i in range(1,p_pol_size+1):
            with open(root_path+'p'+str(i)+'.rq', 'r') as f:
                queries_str.append(f.read())
        for i in range(1,u_pol_size+1):
            with open(root_path+'u'+str(i)+'.rq', 'r') as f:
                queries_str.append(f.read())

        queries = []
        for q_str in queries_str:
            q = Query([], [])
            fyzz_q = fyzz.parse(q_str)
            for sel in fyzz_q.selected:
                q.select.append('?'+sel.name)
            for wh in fyzz_q.where:
                wh_str = ""
                for wh_part in range(0,3):
                    if type(wh[wh_part]) is fyzz.ast.SparqlVar:
                        wh_str += '?' + wh[wh_part].name + ' '
                    elif type(wh[wh_part]) is fyzz.ast.SparqlLiteral:
                        wh_str += wh[wh_part].value + ' '
                    elif type(wh[wh_part]) is tuple:        #for IRIs
                        wh_str += wh[wh_part][0] + wh[wh_part][1] + ' '
                    elif type(wh[wh_part]) is str:          #for expanded URIs
                        wh_str += wh[wh_part][1:-1] + ' '
                wh_str += "."
                q.where.append(wh_str)
            queries.append(q)
        return queries

            