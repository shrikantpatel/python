"""
MVT Tile Decoder for handling Mapbox Vector Tile decoding

Handles decompression and decoding of MVT tiles.
"""

import base64
import gzip
from mapbox_vector_tile import decode
from geometry_processor import GeometryProcessor


class MVTTileDecoder:
    """Handles MVT tile decompression, decoding, and feature display."""
    
    def __init__(self):
        """Initialize the MVT decoder."""
        self.geometry_processor = GeometryProcessor()
    
    @staticmethod
    def decompress_mvt_data(mvt_data):
        """
        Decompress MVT data based on its format (binary or base64).
        
        Args:
            mvt_data: Either binary data (bytes) or base64-encoded string
            
        Returns:
            bytes: Decompressed MVT binary data ready for decoding
            
        Raises:
            Exception: If decompression fails
        """
        if isinstance(mvt_data, bytes):
            print("Data is already in binary format, skipping base64 decode")
            # Data is already binary, likely gzip compressed
            mvt_binary = gzip.decompress(mvt_data)
            print(f"Gzip decompressed successfully, length: {len(mvt_binary)}")
            return mvt_binary
        else:
            print("Data is base64 string, decoding...")
            # Fix base64 padding if needed
            missing_padding = len(mvt_data) % 4
            if missing_padding:
                mvt_data += '=' * (4 - missing_padding)
                print("Fixed base64 padding")
            
            # Base64 decode first
            base64_decoded = base64.b64decode(mvt_data)
            print(f"Base64 decoded successfully, length: {len(base64_decoded)}")
            
            # Then gzip decompress
            mvt_binary = gzip.decompress(base64_decoded)
            print(f"Gzip decompressed successfully, length: {len(mvt_binary)}")
            return mvt_binary
    
    def display_tile_features(self, decoded_tile, tile_index, z, x, y):
        """
        Display decoded MVT tile features with enhanced detail and geometry conversion.
        
        Args:
            decoded_tile (dict): Decoded MVT tile data
            tile_index (int): Zero-based tile index for display
            z (int): Zoom level
            x (int): Tile X coordinate
            y (int): Tile Y coordinate
        """
        if decoded_tile:
            print(f"--- Decoded MVT Tile {tile_index + 1} Contents ---")
            for layer_name, layer_data in decoded_tile.items():
                features = layer_data.get('features', [])
                extent = layer_data.get('extent', 8192)  # Get extent from layer data
                
                print(f"Layer: {layer_name}")
                print(f"  Total Features: {len(features)}")
                print(f"  Extent: {extent}")
                
                # Print details of the first few features as samples
                for i, feature in enumerate(features[:3]):  # Show first 3 features
                    print(f"  --- Sample Feature {i + 1} ---")
                    
                    # Process feature geometry using shared function with correct extent
                    processed = self.geometry_processor.process_feature_geometry(
                        feature, z, x, y, extent=extent, show_tile_space=True
                    )
                    
                    print(f"  Geometry Type: {processed['geometry_type']}")
                    print(f"  Properties: {processed['properties']}")
                    print(f"  Geometry (Tile Space): {processed['tile_space_geom']}")
                    
                    if processed['error']:
                        print(f"  [Error: {processed['error']}]")
                    else:
                        print(f"  Geometry (WGS84): {processed['wgs84_geom']}")
                        print(f"  WKT (Tile Space): {processed['tile_space_wkt']}")
                        print(f"  WKT (WGS84): {processed['wgs84_wkt']}")
                
                if len(features) > 3:
                    print(f"  ... and {len(features) - 3} more features")
        else:
            print(f"Tile {tile_index + 1} is empty or failed to parse.")
    
    def decode_mvt_tile(self, tile_info, tile_index):
        """
        Decode a single MVT tile with comprehensive logging and error handling.
        
        This function handles the complete MVT decoding process:
        1. Extracts tile metadata and displays bounding box information
        2. Decompresses the MVT data (handles both binary and base64 formats)
        3. Decodes the MVT using mapbox-vector-tile library
        4. Displays the decoded features and layer information
        
        Args:
            tile_info (dict): Dictionary containing tile metadata and data
            tile_index (int): Zero-based index of the tile for display purposes
            
        Returns:
            tuple: (success: bool, decoded_tile: dict or None) - True/decoded_data if successful, False/None otherwise
        """
        try:
            # Extract tile information
            z, x, y = tile_info['z'], tile_info['x'], tile_info['y']
            mvt_data = tile_info['data']
            bbox = tile_info['bbox']
            
            # Display tile metadata and geographic information
            print(f"\n=== Processing Tile {tile_index + 1} ===")
            print(f"Tile Coordinates: z={z}, x={x}, y={y}")
            print(f"Bounding Box (west, south, east, north): {bbox}")
            print(f"  West: {bbox[0]:.6f}°, South: {bbox[1]:.6f}°")
            print(f"  East: {bbox[2]:.6f}°, North: {bbox[3]:.6f}°")
            
            # Display data information
            print(f"Data type: {type(mvt_data)}")
            print(f"Data length: {len(mvt_data) if mvt_data else 'None'}")
            
            # Step 1: Decompress the MVT data
            mvt_binary = self.decompress_mvt_data(mvt_data)

            # Step 2: Decode the MVT using mapbox-vector-tile library
            decoded_tile = decode(mvt_binary)
            print("MVT decoded successfully")

            # Step 3: Display the decoded tile contents
            self.display_tile_features(decoded_tile, tile_index, z, x, y)
                
            return True, decoded_tile
            
        except Exception as e:
            print(f"An error occurred decoding tile {tile_index + 1}: {e}")
            return False, None