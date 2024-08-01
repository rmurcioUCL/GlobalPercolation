# Some figures to work out the size of things
## Case study: Australia

**Raw data from OSM (shp)** - 1.2 GB.  2,783,126 roads. Road types:  'bridleway'  'busway'  'cycleway'  'footway'  'living_street'  'motorway'  'motorway_link'  'path'  'pedestrian'  'primary'  'primary_link'  'residential'
'secondary'  'secondary_link'  'service'  'steps'  'tertiary'  'tertiary_link'  'track'  'track_grade1'  'track_grade2'  'track_grade3'  'track_grade4'  'track_grade5'  'trunk'  'trunk_link'  'unclassified'  'unknown'

**After removing unwanted roads (shp)** - 1.1 GB. 2,095,754 roads. Road types: 'living_street'  'motorway'  'motorway_link'  'primary'  'primary_link'  'residential'  'secondary'  'secondary_link'  'tertiary'  'tertiary_link'
'trunk'  'trunk_link'  'unclassified'  'unknown'

**After simplifying (gpkg)** - 942.6 MB. Nodes: 1,637,749  Edges: 2,091,298
**After consolidation (gpkg)** 746.3 MB. Nodes: 1,109,530  Edges: 1,515,020

**After running percolation** 
 - clustersinfoT - 115.9 KB (40,000 rows, 5 columns)
 - memTablesT - 41 GB
 - cluster_sizesT - 255.3 MB


