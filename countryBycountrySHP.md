A variety of scripts to acquire OSM data to build a hierarchical percolation dataset

Requirements for get_cleanNW.py

Get the shape file from OSM.
Extract on a new layer only the roads - 
"fclass" in ( 'living_street' , 'motorway' , 'motorway_link' , 'primary' , 'primary_link' , 'residential' , 'secondary' , 'secondary_link' , 'tertiary' , 'tertiary_link' , 'trunk' , 'trunk_link' , 'track', 'track_grade1','track_grade2','track_grade3','track_grade4','track_grade5','unclassified', 'unknown' )

Run Split with Lines from the toolbox over the extracted layer
Export the split layer as a shapefile (named after the region + _raw) and keep only the columns: osmd_id, code, class, name.
Calculate the length of _raw by creating a new field named length with the expression $length. Make sure to save the layer
Edit get_cleanNW.py with the filename from point 4 and run
Still need to ensure it can be done in one run or have small save scripts.

Notes : On a 658 Mb file (Australia), Point 3 took 5 minutes. After running 4, the file went to 340 Mb

Once you have a clean file (_raw_clean.gpkg) we can run percolation.py. We need to manually modify the name at this point in the script. This script will generate three directories: clustersinfoT - Number of clusters and LCC info per threshold; membTablesT - Membership data per Th (nodeid,clusterid); cluster_sizesT - cluster sizes per Th (cluster_id,cluster_size)
