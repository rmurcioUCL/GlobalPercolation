import pandas as pd
import networkx as nx
import osmnx as ox
import requests
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import os

def run_spercolation_authomatic_ps(input_path, output_path, p_min, p_step, p_max, LCC_perc,fname):
    """
    Function that runs the street percolation.
    The range of values for the percolation threshold p is authomatically detected.
    
    Input contains:
    
    -input_path: path of the edgelist file in the format (i,j,w)
    -output_path: desideredpath for the output files
    -p_min: minimum value of the percolation threshold p
    -p_step: increments for the percolation threshold p
    -p_max: maximum value considered for the authomatic p detection
    -LCC_perc: criterion for stopping the thresholding. When the size of the LCC reaches 0.98 of the original graph
    """
    
    #################### Preparing output folders
    #directory for membership tables
    dir_res_memb = output_path+'/membTablesT/' 
    if not os.path.exists(dir_res_memb): os.makedirs(dir_res_memb)
        
    #directory for cluster size tables    
    dir_clust_size = output_path+"/cluster_sizesT/"
    if not os.path.exists(dir_clust_size): os.makedirs(dir_clust_size)
        
    #file with global threshold info
    clusters_info = output_path+"/clustersinfoT/"
    if not os.path.exists(clusters_info): os.makedirs(clusters_info)
    clusters_info_filename = clusters_info+"clusters_info_p"+"_"+fname

    ########################################
    
    #Let us read the file that contains the list of nodes
    #print(input_path)
    edgelist = pd.read_csv(input_path, sep=",")
    edgelist.columns = ['start_point','end_point','length']
    
    #Calculating the size of the largest connected component for the entire graph
    G = nx.from_pandas_edgelist(edgelist, source='start_point', target='end_point', edge_attr='length',
                                create_using=nx.Graph())
    #Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
    Gcc = sorted((G.subgraph(c) for c in nx.connected_components(G)), key=len, reverse=True)
    G0 = len(Gcc[0])
    #Creating a file with global info on clusters given threshold p
    clusters_info_file = open(clusters_info_filename,'w')
    header = "threshold_p,n_clusters,LCC_id,LCC_size,LCC_size_normed\n"
    clusters_info_file.write(header)
    
    ######################################## PERCOLATION #######################
    
    #Creating a range of p values for the percolation
    ps = np.arange(p_min, p_max, step=p_step)
    
    for p in ps:
        print(p)
        #find sub-matrix such that all weights <= threshold p
        filtered_p = edgelist[edgelist['length']<=p]
    
        #create graph
        G = nx.from_pandas_edgelist(filtered_p, source='start_point', target='end_point', edge_attr='length',
                                create_using=nx.Graph())
        
        #Creating a membership table file
        file_name = dir_res_memb+'membership_'+'p'+str(p)+"_"+fname+'.txt'
        memb_table_file = open(file_name,'w')
        header = "node_id,cluster_id\n"
        memb_table_file.write(header)

        #Creating a cluster size file
        file_name = dir_clust_size+'clust_size_'+'p'+str(p)+"_"+fname+'.txt'
        cluster_size_file = open(file_name,'w')
        header = "cluster_id,cluster_size\n"
        cluster_size_file.write(header)

        #Looping over connected components
        LCC_size = 0 #initial value to store the size of the LCC
        LCC_id = 0
        cluster_id=0
        for cluster_id, cluster_nodes in enumerate(nx.connected_components(G)):
            #Saving cluster size to file
            cluster_size = len(cluster_nodes)
            #if cluster_size==361:
            	#print(cluster_nodes)
            line = "%i,%i\n"%(cluster_id, cluster_size)
            cluster_size_file.write(line)

            #Updating the value for the size of the LCC (I want to find the id)
            if cluster_size>LCC_size:
                LCC_size = cluster_size
                LCC_id = cluster_id

            #Looping over nodes in clusters and saving to membership table file 
            for n in cluster_nodes:
                line = "%i,%i\n"%(n,cluster_id)
                memb_table_file.write(line)

        #Saving global clusters info to file
        NCC = cluster_id+1 #last id index +1 since it started from 0
        LCC_size_normed = 1.*LCC_size/G0
        line = str(p)+',%i,%i,%i,%f\n'%(NCC,LCC_id,LCC_size,LCC_size_normed)

        #line = str(p)+str(NCC)+str(LCC_id)+str(LCC_size)+str(LCC_size_normed)
        clusters_info_file.write(line)

        memb_table_file.close()
        cluster_size_file.close()
        
        #Checking if I have reached the stopping criterion. In that case we don't look at higher ps
        if LCC_size_normed>= LCC_perc: break

    clusters_info_file.close()

    return None


############### This code receives a gpkg generated with osmnx
# It already has nodes, edges so we just need to loaded in the correct order
# We need to project the network to latlong for distance to make sense
   
path = '/home/orkcloud/research/australia/'
fname = 'australia_raw_clean'
fp = path+fname+'.gpkg'
gdf_nodes = gpd.read_file(fp, layer='nodes').set_index('osmid')
gdf_edges = gpd.read_file(fp, layer='edges').set_index(['u', 'v', 'key'])

gdf_nodes=ox.projection.project_gdf(gdf_nodes,to_latlong=True)
gdf_edges=ox.projection.project_gdf(gdf_edges,to_latlong=True)
 
#assert gdf_nodes.index.is_unique and gdf_edges.index.is_unique
G = ox.graph_from_gdfs(gdf_nodes, gdf_edges)

LCC_perc = 0.95 #It will stop before if it reaches this percentage of LCC desidered
p_min = 100
p_max = 40000 
p_step = 10

ledges = list(G.edges())
filename=fname+".csv"
fp=path+filename
print(fp)
f1 = open(fp,"w+")
for edge in ledges:
    nodew = str(edge[0])+","+str(edge[1])+","+str(G.get_edge_data(edge[0],edge[1])[0].get('length'))
    f1.write("%s\n" % nodew)
f1.close()

run_spercolation_authomatic_ps(path+"/"+filename, path, p_min, p_step, p_max, LCC_perc,filename)
