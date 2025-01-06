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
  
All downloadable from geofabrik (https://download.geofabrik.de/) as pbf.

A route map is in this [diagram](https://lucid.app/lucidchart/05c17c1d-c4d2-42d2-b877-642a685b454f/edit?viewport_loc=-1355%2C40%2C2125%2C1105%2C0_0&invitationId=inv_76e1f82c-d7ff-431c-a19c-4df6ed9cdd9c).
(You'll need to create a free account to see it...sorry but it is worth)

##Procedure for individual countries. Tested in Ubuntu 24.04.1
1. Download the pbf from geofabrik and save them in ../pbf
2. Run the shell script getosm.sh. Make sure to update the directories accordingly to your machine. This script will select only the road types we need and transform the pbf into an osm (XML) format.
3. Run the Python script osm2osmnx.py to create a clean (intersections simplified and consolidated) gpkg for each country. Make sure to update the directories accordingly to your machine.

That's it! We can now run the percolation.py for each gpkg.



## From a shapefile --> Deprecated. New definitions from osmnx make this former procedure unusable due to the MultiDigraph format. 
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



