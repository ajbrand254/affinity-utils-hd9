import os
import xml.etree.ElementTree as ET

class AffinityFileParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.layers = []

    def parse_file(self):
        """Parse the Affinity Designer file to extract layer information."""
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            self._extract_layers(root)
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _extract_layers(self, element):
        """Recursively extract layers from the XML structure."""
        for layer in element.findall('.//layer'):
            layer_info = {
                'name': layer.get('name'),
                'id': layer.get('id'),
                'type': layer.get('type'),
                'visible': layer.get('visible') == 'true',
                # Additional attributes can be added here as needed
            }
            self.layers.append(layer_info)
            # Removed recursive call to prevent infinite recursion
            # since './/layer' already finds all descendant layers

    def get_layers(self):
        """Return the extracted layers."""
        return self.layers

    def save_layer_info(self, output_dir):
        """Save layer information to a text file."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            output_file = os.path.join(output_dir, 'layer_info.txt')
            with open(output_file, 'w') as f:
                for layer in self.layers:
                    f.write(f"{layer['name']} (ID: {layer['id']} Type: {layer['type']} Visible: {layer['visible']})\n")
            print(f"Layer info saved to {output_file}")
        except IOError as e:
            print(f"Failed to write to file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving: {e}")

# Usage example (this would be in main.py or another part of the application):
# parser = AffinityFileParser('path/to/your/file.afdesign')
# parser.parse_file()
# layers = parser.get_layers()
# parser.save_layer_info('output_directory')
