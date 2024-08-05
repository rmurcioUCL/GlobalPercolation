# GlobalPercolation
A variety of scripts to acquire OSM data to build a hierarchical percolation dataset.

We aim to go from OSM to a MultiDigraph that we can use in osmnx consolidate routine. Our massive target areas are:
* Africa 	
* Antarctica 	
* Asia 	
* Australia and Oceania 
* Central America 	
* Europe 
* North America 	
* South America
All downloadable from geofabrik as pbf.

A route map is in this [diagram](https://lucid.app/lucidchart/05c17c1d-c4d2-42d2-b877-642a685b454f/edit?viewport_loc=-1355%2C40%2C2125%2C1105%2C0_0&invitationId=inv_76e1f82c-d7ff-431c-a19c-4df6ed9cdd9c).
(You'll need to create a free account to see it...sorry but it is worthy)

## From a shapefile
In the contryBycountrySHP.md document, you can find a fully functional algorithm for this if you download shapefiles from OSM. This is quite useful for individual countries like all the islands.
To use this procedure for larger areas (not always available in shp, and maybe they would be too large for QGIS), we first need to merge the line and multiline data from the pbf into a single shp. 

An option is to use *osmosis to get an osm file, load this into QGIS, save it as a massive shapefile, and then use the procedure from contryBycountrySHP.md
osmosis example:
<code>
osmosis --read-pbf /home/orkcloud/research/africa/south-africa-and-lesotho-latest.osm.pbf --way-key-value keyValueList="highway.primary,highway.secondary,highway.tertiary,highway.primary_link,highway.secondary_link,highway.tertiary_link,highway.residential,highway.motorway_link,highway.motorway,highway.unclassified,highway.road,highway.living_street,highway.trunk, highway.trunk_link,highway.trunk,highway.road" --used-node --write-xml /home/orkcloud/research/africa/south-africa-and-lesotho_roads.osm
</code>
!!The above line works fine but still need to write this in the form a procedure to be useful for eveyone.

## From a pdf/osm file
 - Tobe writeup



