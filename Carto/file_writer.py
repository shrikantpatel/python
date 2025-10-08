"""
File Writer for MVT Decoder

Handles writing geometry collections and tile data to files.
"""

import os
from coordinate_converter import CoordinateConverter
from geometry_processor import GeometryProcessor


class FileWriter:
    """Handles file writing operations for geometry collections and tile data."""
    
    def __init__(self):
        """Initialize the file writer."""
        self.coordinate_converter = CoordinateConverter()
        self.geometry_processor = GeometryProcessor()
    
    def save_geometry_collection_to_file(self, geometry_collection, tiles_count, tiles_info, all_decoded_tiles):
        """
        Save the formatted geometry collection with tile bounding boxes and individual feature geometries.
        
        Args:
            geometry_collection (str): WKT geometry collection string
            tiles_count (int): Number of tiles in the collection
            tiles_info (list): List of tile information dictionaries
            all_decoded_tiles (list): List of decoded tile data
            
        Returns:
            str: formatted_filename - name of created file
        """
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Save formatted version with comprehensive geometry data
        formatted_filename = os.path.join(script_dir, "tiles_geometry_collection_formatted.wkt")
        
        with open(formatted_filename, 'w') as formatted_file:
            # Write header
            self._write_file_header(formatted_file, tiles_count)
            
            # Write tile bounding boxes collection
            self._write_tile_bounding_boxes(formatted_file, geometry_collection)
            
            # Write individual tile details and feature geometries
            self._write_individual_tiles_and_features(formatted_file, tiles_info, all_decoded_tiles)
        
        return os.path.basename(formatted_filename)
    
    def _write_file_header(self, file_handle, tiles_count):
        """Write the file header with metadata."""
        file_handle.write(f"-- Combined Geometry Collection of {tiles_count} MVT Tiles (Comprehensive)\n")
        file_handle.write(f"-- Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file_handle.write("-- This collection includes tile bounding boxes and individual feature geometries\n\n")
    
    def _write_tile_bounding_boxes(self, file_handle, geometry_collection):
        """Write the tile bounding boxes section."""
        file_handle.write("-- ===== TILE BOUNDING BOXES =====\n")
        file_handle.write("-- Geometry collection of all tile bounding boxes\n\n")
        
        # Format the geometry collection for better readability
        formatted_geom = geometry_collection.replace("GEOMETRYCOLLECTION(", "GEOMETRYCOLLECTION(\n  ")
        formatted_geom = formatted_geom.replace("), POLYGON", "),\n  POLYGON")
        formatted_geom = formatted_geom.replace("))", ")\n)")
        
        file_handle.write(formatted_geom)
        file_handle.write("\n\n")
    
    def _write_individual_tiles_and_features(self, file_handle, tiles_info, all_decoded_tiles):
        """Write individual tiles and their features."""
        file_handle.write("-- ===== INDIVIDUAL TILES AND FEATURES =====\n\n")
        
        for i, (tile_info, decoded_tile) in enumerate(zip(tiles_info, all_decoded_tiles)):
            z, x, y = tile_info['z'], tile_info['x'], tile_info['y']
            bbox = tile_info['bbox']
            west, south, east, north = bbox
            
            # Write tile header
            file_handle.write(f"-- Tile {i+1}: z={z}, x={x}, y={y}\n")
            file_handle.write(f"-- Bounding Box: West={west:.6f}, South={south:.6f}, East={east:.6f}, North={north:.6f}\n")
            
            # Write tile bounding box
            tile_bbox_wkt = self.coordinate_converter.create_tile_bbox_wkt(bbox)
            file_handle.write(f"-- Tile Bounding Box:\n{tile_bbox_wkt}\n\n")
            
            # Write feature geometries if available
            if decoded_tile:
                self._write_tile_features(file_handle, decoded_tile, i, z, x, y)
            else:
                file_handle.write(f"-- No decoded data available for Tile {i+1}\n\n")
            
            file_handle.write("-" * 60 + "\n\n")
    
    def _write_tile_features(self, file_handle, decoded_tile, tile_index, z, x, y):
        """Write features for a specific tile."""
        file_handle.write(f"-- Features in Tile {tile_index+1}:\n")
        feature_count = 0
        
        for layer_name, layer_data in decoded_tile.items():
            features = layer_data.get('features', [])
            file_handle.write(f"-- Layer: {layer_name} ({len(features)} features)\n")
            
            for j, feature in enumerate(features):
                feature_count += 1
                
                # Process feature geometry using shared function
                processed = self.geometry_processor.process_feature_geometry(feature, z, x, y, show_tile_space=False)
                
                if processed['wgs84_wkt'] and not processed['error']:
                    # Write feature info
                    file_handle.write(f"-- Feature {feature_count} (Layer: {layer_name})\n")
                    if processed['properties']:
                        prop_str = self.geometry_processor.format_properties_string(processed['properties'])
                        file_handle.write(f"-- Properties: {prop_str}\n")
                    file_handle.write(f"{processed['wgs84_wkt']}\n\n")
                else:
                    error_msg = processed['error'] or "No valid geometry"
                    file_handle.write(f"-- Feature {feature_count}: {error_msg}\n\n")
        
        if feature_count == 0:
            file_handle.write("-- No valid features found in this tile\n\n")