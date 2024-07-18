# GlobalPercolation
A variety of scripts to acquire OSM data to build a hierarchical percolation dataset

Usage:

1. Get the shape file from OSM.
2. Extract on a new layer only the roads -
   <code>
   "fclass" in ( 'living_street' , 'motorway' , 'motorway_link' , 'primary' , 'primary_link' , 'residential' , 'secondary' , 'secondary_link' , 'tertiary' , 'tertiary_link' , 'trunk' , 'trunk_link' , 'unclassified' , 'unknown' )
   </code>
3. Run Split with Lines from the toolbox over the extracted layer
4. Export the split layer as a shapefile. This is our input data for the Python script
