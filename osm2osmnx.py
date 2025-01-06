import networkx as nx
import osmnx as ox

import time

import os
import sys


start = time.time()
print('Start: '+str(start))


input_path = '/home/orkcloud/research/osm/africa/raw/'
ouput_path='/home/orkcloud/research/osm/africa/clean/'
files = (file for file in os.listdir(input_path)
         if os.path.isfile(os.path.join(input_path, file)) & file.endswith('.osm') )
for fname in files:
    print(fname)

    filename=input_path+fname

    G=ox.graph_from_xml(filename)  # osm --> MultiDiGraph
    print('Done osm-graph for '+ fname)

    G_proj = ox.project_graph(G) 
    G2 = ox.consolidate_intersections(G_proj, rebuild_graph=True, tolerance=5, dead_ends=True)
    print('Done consolidation for '+ fname)

    filename=ouput_path+fname[:-4]+'.gpkg'
    ox.save_graph_geopackage(G2,filename)

    print('Saved '+ filename)
    end = time.time()
    print('Total time for '+fname+' '+str(end - start))

end = time.time()
print('Total time '+str(end - start))

