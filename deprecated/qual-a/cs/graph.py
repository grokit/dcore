
import re

class Graph:
    
    def __init__(self):
        self.vertices = {}
    
    def __str__(self):
        "Assumes that the graph is fully connected."
        
        sBuf = []
        Visited = set()
        
        rNode = None
        for v in self.vertices.values():
            rNode = v
            break
        
        ToVisit = [rNode]
        while len(ToVisit) != 0:
            v = ToVisit.pop()
            Visited.add(v)
            
            for e in v.edges:
                if not e.to in Visited:
                    ToVisit.append(e.to)
                    Visited.add(e.to)
                sBuf.append( "%s -- %s (weight: %s)" % (v.label, e.to.label, e.weight))
        
        return "\n".join(sBuf)
    
    def addVertexFromLabel(self, v):
        vertex = Vertex()
        vertex.label = v
        
        self.vertices[vertex.label] = vertex
        
    def addBidirectionalEdgeFromLabels(self, efrmLabel, etoLabel, weight):
        
        vFrom = self.vertices[efrmLabel]
        vTo = self.vertices[etoLabel]
        
        e = Edge()
        e.frm = vFrom
        e.to = vTo
        e.weight = weight
        
        vFrom.edges.add(e)
        
        e = Edge()
        e.frm = vTo
        e.to = vFrom
        e.weight = weight
        
        vTo.edges.add(e)
    
class Vertex:
    "Vertex is synonymous to node."
    
    def __init__(self):
        self.edges = set()
        self.label = None
    
    def __str__(self):
        return "Vextex.label: %s" % (self.label)

    def __repr__(self):
	    return self.__str__()
    
class Edge:
    "Connect the vertices together."
    
    def __init__(self):
        self.frm = None    
        self.to = None    
        self.weight = None
    
    def __str__(self):
        return "edge %s -- %s (weight: %i)" % (self.frm.label, self.to.label, self.weight)

def graphFromDotString(dotStr):
    
    G = Graph()
    
    edges = []
    for line in dotStr.splitlines():
        m = re.search(r'(\w+)[ ]*--[ ]*(\w+)', line)
        mw = re.search(r'weight="([0-9]+)"', line)
        if m is not None:
            e = Edge()
            e.frm = m.group(1)
            e.to = m.group(2)
            e.weight = int(mw.group(1))
            edges.append( e )
    
    for e in edges:
        G.addVertexFromLabel(e.to)
        G.addVertexFromLabel(e.frm)
    
    for e in edges:
        G.addBidirectionalEdgeFromLabels(e.frm, e.to, e.weight)
    
    return G

def getTestGraph():
    dotGraph = """
    graph 
    {
        a -- b [weight="2", label="2"];
        b -- c [weight="1", label="1"];
        c -- d [weight="2", label="2"];
        b -- d [weight="7", label="7"];
        e -- a [weight="2", label="2"];
        d -- e [weight="2", label="2"];
    }
    """
    G = graphFromDotString(dotGraph)    
    return G

if __name__ == '__main__':
    print(getTestGraph())
    
