from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD

g = Graph()

andre = URIRef("http://example.org/andre")
g.add((andre, RDF.type, FOAF.Person))
g.add((andre, FOAF.name, Literal("Andre", datatype=XSD.string)))
g.add((andre, FOAF.nick, Literal("Andre Kusuma")))
g.add((andre, FOAF.mbox, URIRef('mailto:andre@example.org')))

sylia = URIRef("http://example.org/sylia")
g.add((sylia, RDF.type, FOAF.Person))
g.add((sylia, FOAF.name, Literal("Sylia", datatype=XSD.string)))
g.add((sylia, FOAF.nick, Literal("Sylia Caster")))
g.add((sylia, FOAF.mbox, URIRef('mailto:sylia@example.org')))

# Find email address of Andre
for s, p, o in g.triples((None, FOAF.name, Literal("Andre", datatype=XSD.string))):
	for s2, p2, o2 in g.triples((s, FOAF.mbox, None)):
		print(o2) # Output: mailto:andre@example.org

# Bind a prefix to a namespace
# This will allow us to use the prefix in the RDF graph
g.bind("foaf", FOAF)

# Print all data in n3 format
print(g.serialize(format='n3'))
