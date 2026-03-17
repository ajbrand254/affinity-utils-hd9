import os
import sys
import argparse
from layer_exporter import export_layers
from affinity_file_parser import parse_affinity_file

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Export layers from Affinity Designer documents to PNG files.")
    parser.add_argument("input_file", help="Path to the Affinity Designer file (.afdesign)")
    parser.add_argument("output_dir", help="Directory to save exported PNG files")
    
    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: The file '{args.input_file}' does not exist.")
        sys.exit(1)

    # Check if the output directory exists, create it if it doesn't
    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            print(f"Output directory '{args.output_dir}' created.")
        except Exception as e:
            print(f"Error creating output directory: {e}")
            sys.exit(1)

    # Parse the Affinity file to get layer information
    try:
        layers = parse_affinity_file(args.input_file)
    except Exception as e:
        print(f"Error parsing file '{args.input_file}': {e}")
        sys.exit(1)

    # Export layers to PNG files
    try:
        export_layers(layers, args.output_dir)
        print(f"Export completed successfully. Layers exported to '{args.output_dir}'.")
    except Exception as e:
        print(f"Error exporting layers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# TODO: 
# - Add more user-friendly logging
# - Implement support for other file formats
# - Handle cases where layers might not be exportable
# - Improve error handling for specific export failures
# - Add tests for each component of the utility
