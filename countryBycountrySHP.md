## Procedure to prepare a OSM shapefile into a MultiDiGraph object (NetworkX) ready for the percolation process

### This assume you will use the get_cleanNW.py script and QGIS

1. Get the shape file from OSM.
2. Extract on a new layer only the roads - 
"fclass" in ( 'living_street' , 'motorway' , 'motorway_link' , 'primary' , 'primary_link' , 'residential' , 'secondary' , 'secondary_link' , 'tertiary' , 'tertiary_link' , 'trunk' , 'trunk_link' , 'track', 'track_grade1','track_grade2','track_grade3','track_grade4','track_grade5','unclassified', 'unknown' )

3. Run Split with Lines from the toolbox over the extracted layer
4. Export the split layer as a shapefile (named after the region + _raw) and keep only the columns: osmd_id, code, class, name.
5. Calculate the length of _raw by creating a new field named length with the expression $length. Make sure to save the layer
6. Edit get_cleanNW.py with the filename from point 4 and run

Notes: On a 658 Mb file (Australia), Point 3 took 5 minutes. After running 4, the file went to 340 Mb

Once you have a clean file (_raw_clean.gpkg) we can run percolation.py. We need to manually modify the name at this point in the script. This script will generate three directories: clustersinfoT - Number of clusters and LCC info per threshold; membTablesT - Membership data per Th (nodeid,clusterid); cluster_sizesT - cluster sizes per Th (cluster_id,cluster_size)
