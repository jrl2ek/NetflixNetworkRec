# utility.py
#
# Contains a collection of utility scripts that will be used by the models.

def parse_nodes_edge_file(filename):
    import networkx as nx
    import re
    
    # open the file
    with open(filename,'r') as f:
        lines = f.readlines()
    
    network = {}
    objects = []
    for i,line in enumerate(lines):
        line=line.strip()
        if line[:2] == '*v':
            continue
        elif line[:2] == '*e':
            network['nodes'] = objects
            objects = []
        else:
            objects.append(line)
    network['edges'] = objects 
    # print(network['edges'][:10])
    
    # Get the titles and nodes, and store them as a dict. The <title_dict> maps node # to 
    # node name (i.e. title of the movie).
    titles = [re.search(r'\s(.+)\s0.0 0.0 ellipse',x).group(1).replace('"','') for x in network['nodes']]
    nodes = [int(re.search(r'(\d+)',x).group(1)) for x in network['nodes']]
    title_dict = {}
    for n,title in zip(nodes,titles):
        title_dict[n] = title
       
    # Add the nodes (films)
    G = nx.Graph()
    for n in title_dict:
        G.add_node(title_dict[n])
    #print(title_dict)    
    
    # Add the edges (things in common between the films)
    for edge in network['edges']:
        e = edge.split()
        G.add_edge(title_dict[int(e[0])],title_dict[int(e[1])],weight=int(e[2]))
        
    #print(G["never die alone"]) # To get one node and its edges
    #print(G.edges(data=True)) # To get all of the edges and their attributes
    #nx.set_node_attributes(G, title_dict) # To add node attributes
    
    return G

def graph_info(g):
        
    # Get number of connected components
    n_components = nx.number_connected_components(g)

    # Get the % of largest component
    gc = g.subgraph(max(nx.connected_components(g), key=len)).copy()
    num_nodes_largest_component = gc.number_of_nodes()
    percent_largest_component = gc.number_of_nodes()/g.number_of_nodes()
    
    print('Got the largest component...')

    # Get the diameter of the largest component
    diameter_largest_component = nx.diameter(gc)

    # Get the average shortest path lenth for the largest component
    average_shortest_path_largest_component = nx.average_shortest_path_length(gc)
    
    print('Got the avg shortest path...')

    # Get the average degree of the whole graph
    average_degree = np.mean(np.array([x[1] for x in g.degree()]))

    # Get the average clustering coefficient of the whole graph
    clustering_coeff = nx.average_clustering(g)
    
    output = {}
    output['n_components'] = n_components
    output['num_nodes_largest_component'] = num_nodes_largest_component
    output['percent_largest_component'] = percent_largest_component
    output['diameter_largest_component'] = diameter_largest_component
    output['average_shortest_path_largest_component'] = average_shortest_path_largest_component
    output['average_degree'] = average_degree
    output['average_clustering_coefficient'] = clustering_coeff
    
    return output