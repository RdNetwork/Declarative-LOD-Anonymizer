class Prefix():
    
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def write(self, lang):
        if lang == 'SPARQL':
            return "PREFIX " + self.name + ": <" + self.url + ">"
        elif lang == 'RDF':
            return "@prefix " + self.name + ": <" + self.url + "> ."
        else:
            return ''

    @staticmethod
    def writePrefixes(prefixes, lang):
        str = ""
        for p in prefixes:
            str += p.write(lang) + "\n"

        return str
