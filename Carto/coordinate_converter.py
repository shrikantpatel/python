"""
Coordinate Converter for MVT Decoder

Handles conversion between different coordinate systems and bounding box calculations.
"""

import math


class CoordinateConverter:
    """Handles coordinate system conversions for MVT processing."""
    
    @staticmethod
    def tile_to_bbox(z, x, y):
        """
        Convert tile coordinates (z, x, y) to geographic bounding box.
        
        Uses Web Mercator projection (EPSG:3857) tile coordinate system.
        
        Args:
            z (int): Zoom level
            x (int): Tile X coordinate
            y (int): Tile Y coordinate
            
        Returns:
            tuple: (west, south, east, north) in decimal degrees
        """
        def tile_to_lon(x, z):
            """Convert tile X coordinate to longitude"""
            return x / (2.0 ** z) * 360.0 - 180.0
        
        def tile_to_lat(y, z):
            """Convert tile Y coordinate to latitude"""
            n = math.pi - 2.0 * math.pi * y / (2.0 ** z)
            return math.degrees(math.atan(math.sinh(n)))
        
        # Calculate bounding box coordinates
        west = tile_to_lon(x, z)
        east = tile_to_lon(x + 1, z)
        north = tile_to_lat(y, z)
        south = tile_to_lat(y + 1, z)
        
        return (west, south, east, north)
    
    @staticmethod
    def tile_space_to_wgs84(tile_x, tile_y, z, x, y, extent=8192):
        """
        Convert MVT tile space coordinates to WGS84 geographic coordinates.
        
        This handles MVT coordinates that may extend beyond the standard extent
        due to buffering or feature clipping at tile boundaries.
        
        Args:
            tile_x (float): X coordinate in tile space (may extend beyond 0-extent)
            tile_y (float): Y coordinate in tile space (may extend beyond 0-extent)
            z (int): Zoom level of the tile
            x (int): Tile X coordinate
            y (int): Tile Y coordinate
            extent (int): MVT extent (default 8192 for this dataset)
            
        Returns:
            tuple: (longitude, latitude) in WGS84 decimal degrees
        """
        # Convert tile space coordinates to fractional tile coordinates
        # Allow coordinates outside 0-extent range for buffered MVT data
        frac_x = x + (tile_x / extent)
        frac_y = y + (tile_y / extent)
        
        # Convert fractional tile coordinates to WGS84
        lon = (frac_x / (2.0 ** z)) * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi - (2.0 * math.pi * frac_y) / (2.0 ** z)))
        lat = math.degrees(lat_rad)
        
        return (lon, lat)
    
    def convert_geometry_to_wgs84(self, geometry, z, x, y, extent=8192):
        """
        Convert MVT tile space geometry to WGS84 geographic coordinates.
        
        Args:
            geometry (dict): GeoJSON-like geometry object
            z (int): Zoom level of the tile
            x (int): Tile X coordinate
            y (int): Tile Y coordinate
            extent (int): MVT extent (default 8192 for this dataset)
            
        Returns:
            dict: Geometry with WGS84 coordinates
        """
        if not isinstance(geometry, dict) or 'type' not in geometry or 'coordinates' not in geometry:
            return geometry
        
        geom_type = geometry['type']
        coords = geometry['coordinates']
        
        def convert_point(pt):
            """Convert a single point from tile space to WGS84"""
            if len(pt) >= 2:
                lon, lat = self.tile_space_to_wgs84(pt[0], pt[1], z, x, y, extent)
                return [lon, lat] + pt[2:]  # Preserve any Z/M coordinates
            return pt
        
        if geom_type == 'Point':
            converted_coords = convert_point(coords)
        elif geom_type == 'LineString':
            converted_coords = [convert_point(pt) for pt in coords]
        elif geom_type == 'Polygon':
            converted_coords = [[convert_point(pt) for pt in ring] for ring in coords]
        elif geom_type == 'MultiPoint':
            converted_coords = [convert_point(pt) for pt in coords]
        elif geom_type == 'MultiLineString':
            converted_coords = [[convert_point(pt) for pt in line] for line in coords]
        elif geom_type == 'MultiPolygon':
            converted_coords = [[[convert_point(pt) for pt in ring] for ring in poly] for poly in coords]
        else:
            # Unsupported geometry type, return as-is
            return geometry
        
        return {
            'type': geom_type,
            'coordinates': converted_coords
        }
    
    @staticmethod
    def create_tile_bbox_wkt(bbox):
        """
        Create a WKT polygon from a tile bounding box.
        
        Args:
            bbox (tuple): Bounding box as (west, south, east, north)
            
        Returns:
            str: WKT polygon representation of the bounding box
        """
        west, south, east, north = bbox
        return f"POLYGON (({west} {south}, {east} {south}, {east} {north}, {west} {north}, {west} {south}))"