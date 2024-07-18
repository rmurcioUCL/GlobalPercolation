# GlobalPercolation
A variety of scripts to acquire OSM data to build a hierarchical percolation dataset

Usage:

1. Get the shape file from OSM.
2. Extract on a new layer only the roads -
   <code>
   "fclass" in ( 'living_street' , 'motorway' , 'motorway_link' , 'primary' , 'primary_link' , 'residential' , 'secondary' , 'secondary_link' , 'tertiary' , 'tertiary_link' , 'trunk' , 'trunk_link' , 'unclassified' , 'unknown' )
   </code>
3. Run Split with Lines from the toolbox over the extracted layer
4. Export the split layer as a shapefile (named after the region + _raw) and keep only the columns: osmd_id, code, class, name. This is our input data for the Python script
5. Run on the console 


Notes :
On a 658 Mb file (Australia), Point 3 took 5 minutes. After running 4, the file went to 340 Mb
