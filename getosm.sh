#!/bin/bash

# Directory containing the files
INPUT_DIR="/home/orkcloud/research/pbf"  # Change to your directory
OUTPUT_DIR="/home/orkcloud/research/osm/africa/raw/"  # Change to your desired output directory

# Ensure the output directory exists
#mkdir -p "$OUTPUT_DIR"

# Check if Osmosis is installed
if ! command -v osmosis &> /dev/null; then
    echo "Osmosis is not installed or not in PATH. Please install it first."
    exit 1
fi

# Process each file in the directory
for file in "$INPUT_DIR"/*; do
    if [[ -f "$file" ]]; then
        filename=$(basename -- "$file")
        output_file="$OUTPUT_DIR/${filename%.*}"

        echo "Processing $file with Osmosis..."

        # Run Osmosis on the file
osmosis --read-pbf "$file" --way-key-value keyValueList="highway.primary,highway.secondary,highway.tertiary,highway.primary_link,highway.secondary_link,highway.tertiary_link,highway.residential,highway.motorway_link,highway.motorway,highway.unclassified,highway.road,highway.living_street,highway.trunk, highway.trunk_link,highway.trunk,highway.road,highway.rural" --used-node --write-xml "$output_file"

if [[ $? -eq 0 ]]; then
            echo "Successfully processed $file -> $output_file"
        else
            echo "Failed to process $file"
        fi
    fi
done

echo "All files processed."

