import os
try:
    import png  # pypng library
except ImportError:
    raise ImportError("pypng library is required. Install with: pip install pypng")

try:
    from affinity_file_parser import parse_affinity_file
except ImportError:
    raise ImportError("affinity_file_parser module not found. Ensure it exists in the project.")

class LayerExporter:
    def __init__(self, affinity_file_path, output_directory):
        self.affinity_file_path = affinity_file_path
        self.output_directory = output_directory
        self.layers = []

    def load_layers(self):
        """ Load layers from the Affinity Designer file. """
        try:
            self.layers = parse_affinity_file(self.affinity_file_path)
            if not self.layers:
                raise ValueError("No layers found in the provided file.")
        except Exception as e:
            print(f"Error loading layers: {e}")
            return False
        return True

    def export_layers(self):
        """ Export each layer to a PNG file. """
        if not self.layers:
            print("No layers to export.")
            return

        os.makedirs(self.output_directory, exist_ok=True)

        for layer in self.layers:
            try:
                self.export_layer(layer)
            except Exception as e:
                print(f"Failed to export layer '{layer.get('name', 'unknown')}': {e}")

    def export_layer(self, layer):
        """ Export a single layer to a PNG file. """
        layer_name = layer.get('name', 'unnamed_layer')
        layer_data = layer.get('data', {})
        
        # Validate required data
        if not all(key in layer_data for key in ['width', 'height', 'pixels']):
            raise ValueError(f"Layer '{layer_name}' missing required data (width, height, pixels)")

        # Construct the output path for the PNG file
        # Sanitize filename
        safe_name = "".join(c for c in layer_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        output_path = os.path.join(self.output_directory, f"{safe_name}.png")

        # Export the layer data to PNG
        with open(output_path, 'wb') as png_file:
            writer = png.Writer(width=layer_data['width'], height=layer_data['height'], greyscale=False)
            # Ensure pixels is in the correct format for pypng (iterable of rows)
            pixels = layer_data['pixels']
            if not hasattr(pixels, '__iter__'):
                raise ValueError(f"Layer '{layer_name}' pixels data must be iterable")
            writer.write(png_file, pixels)

        print(f"Exported layer '{layer_name}' to '{output_path}'.")

# TODO: Add support for batch exporting multiple Affinity files.
# TODO: Implement more sophisticated error handling and logging.
# TODO: Consider supporting other file formats besides PNG.

if __name__ == "__main__":
    # Example usage
    exporter = LayerExporter("example.afdesign", "exported_layers")
    if exporter.load_layers():
        exporter.export_layers()
