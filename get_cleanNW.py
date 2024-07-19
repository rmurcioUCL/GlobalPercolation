import networkx as nx
import osmnx as ox
import time
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd
import matplotlib.pyplot as plt 

import time


def convert_shp2graph(p, make_G_bidi = True, name='unamed'):
    """
    Read and extrae nodes and edges from a shapefile and return the data as a geopandas dataframe
    
    Parameters
    ----------
    p : str, File path - allowed formats geojson and ESRI Shapefile and other formats Fiona can read and write
    make_G_bidi : bool, if True, assumes linestrings are bidirectional
    name : str, Optional name of graph
    
    Returns
    -------
        df_node_xy - geopandas dataframe wit of nnodes as geopandas
        gdf  - geopandas dataframe with the edges connectivit
    """
    
    
# Load shapefile into GeoDataFrame
    gdf = gpd.read_file(p)
    
    # shapefile needs to include minimal: geometry linestring and the length computed (e.g. in QGIS)
    if 'length' not in gdf.columns:
        raise Exception('Shapefile is invalid: length not in attributes:\n{}'.format(gdf.columns))

    if  not gdf.geometry.map(lambda x: type(x) ==  LineString).all():
        s_invalid_geo = gdf.geometry[gdf.geometry.map(lambda x: type(x) ==  LineString)]
        raise Exception('Shapefile is invalid: geometry not all linestring \n{}'.format(s_invalid_geo))
   
    # Compute the start- and end-position based on linestring 
    gdf['Start_pos'] = gdf.geometry.apply(lambda x: x.coords[0])
    gdf['End_pos'] = gdf.geometry.apply(lambda x: x.coords[-1])
    
    # Create Series of unique nodes and their associated position
    s_points = gdf.Start_pos._append(gdf.End_pos).reset_index(drop=True)
    s_points = s_points.drop_duplicates()   
#     log('GeoDataFrame has {} elements (linestrings) and {} unique nodes'.format(len(gdf),len(s_points)))
    
    # Add index of start and end node of linestring to geopandas DataFrame
    df_points = pd.DataFrame(s_points, columns=['Start_pos'])
    df_points['u'] = df_points.index
    gdf = pd.merge(gdf, df_points, on='Start_pos', how='inner')

    df_points = pd.DataFrame(s_points, columns=['End_pos'])
    df_points['v'] = df_points.index
    gdf = pd.merge(gdf, df_points, on='End_pos', how='inner')
    
    # Bring nodes and their position in form needed for osmnx (give arbitrary osmid (index) despite not osm file)
    df_points.columns = ['pos', 'osmid'] 
    df_points[['x', 'y']] = df_points['pos'].apply(pd.Series)
    df_node_xy = df_points.drop('pos', axis=1)
    return df_node_xy,gdf

#Path to prepared shapefile -  To modify to read a bulk of files
start = time.time()
print('Start...')

path = '/home/orkcloud/research/africa/south-africa/'
fname = 'extracted1'
fnameshp = path+fname+'.shp'
nodesk,edgesk=convert_shp2graph(fnameshp)
end = time.time()
print('Done converting shp2nw '+ str(end - start))

#Modify nodes and edges dataset to put in osmnx format
nodesk = nodesk.set_index('osmid')
edgesk['key'] = 0
edgesk = edgesk.set_index(['u', 'v', 'key'])

#Create a osmnx graph from nodes and edges
edgesk.rename(columns={'osm_id':'osmid'},inplace=True)

graph_attrs = {"crs": "EPSG:4326"}
multi_digraph = ox.convert.graph_from_gdfs(
    nodesk, edgesk, graph_attrs=graph_attrs)
filename = path+fname+'_raw.gpkg'
#save the raw network
ox.save_graph_geopackage(multi_digraph,filename)
end = time.time()
print('Done saving raw '+ str(end - start))


# Now clean and consolidate edges
#assert nodesk.index.is_unique and edgesk.index.is_unique
graph_attrs = {'crs': 'epsg:4326', 'simplified': False}
G2 = ox.convert.graph_from_gdfs(nodesk, edgesk, graph_attrs)
G2 = ox.simplify_graph(G2,remove_rings=True)
end = time.time()
print('Done simplifying '+ str(end - start))

#Consolidate edges
multi_di_graph_utm = ox.project_graph(G2)
consoshp = ox.consolidate_intersections(multi_di_graph_utm, tolerance=15, rebuild_graph=True, dead_ends=False)
#save the cleaned network
filename = path+fname+'_clean.gpkg'
ox.save_graph_geopackage(consoshp,filename)

end = time.time()
print('Done ... '+ str(end - start))


