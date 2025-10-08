"""
Geometry Processor for MVT Decoder

Handles WKT generation, geometry processing, and feature processing.
"""

from coordinate_converter import CoordinateConverter


class GeometryProcessor:
    """Processes geometries, converts to WKT, and handles feature processing."""
    
    def __init__(self):
        """Initialize the geometry processor."""
        self.coordinate_converter = CoordinateConverter()
    
    @staticmethod
    def geometry_to_wkt(geometry):
        """
        Convert a GeoJSON-like geometry object to WKT format.
        
        Args:
            geometry (dict): GeoJSON-like geometry object
            
        Returns:
            str: WKT representation of the geometry
        """
        if not isinstance(geometry, dict) or 'type' not in geometry or 'coordinates' not in geometry:
            return "INVALID GEOMETRY"
        
        geom_type = geometry['type']
        coords = geometry['coordinates']
        
        def format_point(pt):
            """Format a point coordinate"""
            if len(pt) >= 2:
                return f"{pt[0]:.8f} {pt[1]:.8f}"
            return f"{pt[0]} {pt[1]}"
        
        try:
            if geom_type == 'Point':
                return f"POINT ({format_point(coords)})"
            elif geom_type == 'LineString':
                coords_str = ", ".join(format_point(pt) for pt in coords)
                return f"LINESTRING ({coords_str})"
            elif geom_type == 'Polygon':
                rings = []
                for ring in coords:
                    ring_coords = ", ".join(format_point(pt) for pt in ring)
                    rings.append(f"({ring_coords})")
                return f"POLYGON ({', '.join(rings)})"
            elif geom_type == 'MultiPoint':
                points = ", ".join(f"({format_point(pt)})" for pt in coords)
                return f"MULTIPOINT ({points})"
            elif geom_type == 'MultiLineString':
                lines = []
                for line in coords:
                    line_coords = ", ".join(format_point(pt) for pt in line)
                    lines.append(f"({line_coords})")
                return f"MULTILINESTRING ({', '.join(lines)})"
            elif geom_type == 'MultiPolygon':
                polygons = []
                for poly in coords:
                    rings = []
                    for ring in poly:
                        ring_coords = ", ".join(format_point(pt) for pt in ring)
                        rings.append(f"({ring_coords})")
                    polygons.append(f"({', '.join(rings)})")
                return f"MULTIPOLYGON ({', '.join(polygons)})"
            else:
                return f"UNSUPPORTED GEOMETRY TYPE: {geom_type}"
        except Exception as e:
            return f"WKT CONVERSION ERROR: {e}"
    
    def process_feature_geometry(self, feature, z, x, y, extent=8192, show_tile_space=True):
        """
        Process a single feature's geometry, converting from tile space to WGS84 and generating WKT.
        
        Args:
            feature (dict): Feature data from decoded MVT
            z (int): Zoom level
            x (int): Tile X coordinate  
            y (int): Tile Y coordinate
            extent (int): MVT extent for this tile (default 8192)
            show_tile_space (bool): Whether to include tile space geometry in output
            
        Returns:
            dict: Processed geometry information including WGS84 and WKT formats
        """
        result = {
            'tile_space_geom': None,
            'wgs84_geom': None,
            'tile_space_wkt': None,
            'wgs84_wkt': None,
            'properties': feature.get('properties', {}),
            'geometry_type': feature.get('geometry_type'),
            'error': None
        }
        
        tile_space_geom = feature.get('geometry')
        result['tile_space_geom'] = tile_space_geom
        
        if not tile_space_geom:
            result['error'] = "No geometry data available"
            return result
        
        try:
            # Convert geometry from tile space to WGS84
            wgs84_geom = self.coordinate_converter.convert_geometry_to_wgs84(tile_space_geom, z, x, y, extent)
            result['wgs84_geom'] = wgs84_geom
            
            # Generate WKT representations
            if show_tile_space:
                result['tile_space_wkt'] = self.geometry_to_wkt(tile_space_geom)
            result['wgs84_wkt'] = self.geometry_to_wkt(wgs84_geom)
            
        except Exception as e:
            result['error'] = f"Could not convert geometry: {e}"
        
        return result
    
    def create_geometry_collection(self, tiles_info):
        """
        Create a WKT geometry collection from all tile bounding boxes.
        
        Args:
            tiles_info (list): List of tile information dictionaries
            
        Returns:
            str: WKT GeometryCollection containing all tile bounding box polygons
        """
        polygons = []
        
        for tile_info in tiles_info:
            bbox = tile_info['bbox']
            # Create WKT polygon for this tile's bounding box using shared function
            polygon_wkt = self.coordinate_converter.create_tile_bbox_wkt(bbox)
            polygons.append(polygon_wkt)
        
        # Combine all polygons into a geometry collection
        geometry_collection = f"GEOMETRYCOLLECTION({', '.join(polygons)})"
        
        return geometry_collection
    
    @staticmethod
    def format_properties_string(properties, max_props=3):
        """
        Format properties dictionary into a readable string.
        
        Args:
            properties (dict): Feature properties
            max_props (int): Maximum number of properties to show
            
        Returns:
            str: Formatted properties string
        """
        if not properties:
            return ""
        
        prop_items = list(properties.items())[:max_props]
        prop_str = ", ".join(f"{k}: {v}" for k, v in prop_items)
        
        if len(properties) > max_props:
            prop_str += f", ... and {len(properties) - max_props} more properties"
        
        return prop_str