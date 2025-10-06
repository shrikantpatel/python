"""
MVT Decoder - BigQuery Integration

This script fetches Mapbox Vector Tile (MVT) data from Google BigQuery
and decodes the tiles to display their contents.

Features:
- Connects to BigQuery using service account authentication
- Decodes multiple MVT tiles from compressed binary data
- Calculates geographic bounding boxes from tile coordinates
- Displays tile metadata and decoded features

Dependencies:
- google-cloud-bigquery: For BigQuery integration
- mapbox-vector-tile: For MVT decoding
- Built-in libraries: base64, gzip, math, json, os

Author: Your Name
Date: October 2025
"""

import base64
import gzip
import os
import math
import json
from mapbox_vector_tile import decode
from google.cloud import bigquery


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


def load_configuration():
    """
    Load configuration from config.json file in the same directory as the script.
    
    Returns:
        dict: Configuration dictionary containing credential_file and bigquery_query
        
    Raises:
        SystemExit: If config file cannot be loaded or is invalid
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, 'config.json')
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            print(f"Configuration loaded from: {config_file}")
            
            # Validate required fields
            required_fields = ['credential_file', 'bigquery_query', 'project_id']
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print(f"ERROR: Missing required configuration fields: {missing_fields}")
                print("Please ensure config.json contains 'credential_file', 'bigquery_query', and 'project_id'")
                exit(1)
            
            return config
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found: {config_file}")
        print("Please create a config.json file in the same directory as this script.")
        print("Example config.json:")
        print('{"credential_file": "your-service-account.json", "bigquery_query": "SELECT t.z, t.x, t.y, t.data FROM `your-table` AS t WHERE z = 2"}')
        exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in configuration file: {e}")
        print("Please check the syntax of your config.json file.")
        exit(1)
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {e}")
        exit(1)


def find_service_account_credentials(credential_filename):
    """
    Search for service account credential files in common locations.
    
    Args:
        credential_filename (str): Specific credential filename to search for
    
    Returns:
        str: Path to the found credential file
        
    Raises:
        SystemExit: If credential file cannot be found
    """
    credential_paths = [
        credential_filename,                                    # Current directory
        f'./{credential_filename}',                             # Explicit current directory
        os.path.expanduser(f'~/{credential_filename}'),         # Home directory
        os.path.join('..', credential_filename)                 # Parent directory
    ]
    
    for path in credential_paths:
        if os.path.exists(path):
            return path
    
    # If we get here, credential file was not found
    print(f"ERROR: Service account credential file not found: {credential_filename}")
    print("Searched in the following locations:")
    for path in credential_paths:
        print(f"  - {path}")
    print("Please ensure the credential file exists in one of these locations.")
    exit(1)


def setup_bigquery_client(project_id, credential_filename):
    """
    Initialize BigQuery client with proper authentication.
    
    Args:
        project_id (str): Google Cloud project ID for running queries
        credential_filename (str): Name of the credential file to use
        
    Returns:
        bigquery.Client: Configured BigQuery client
        
    Raises:
        SystemExit: If BigQuery client setup fails
    """
    # Find service account credentials (will exit if not found)
    credential_file = find_service_account_credentials(credential_filename)
    
    print(f"Using service account credentials from: {credential_file}")
    # Set environment variable for Google Cloud authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_file
        
    try:
        client = bigquery.Client(project=project_id)
        print(f"Using project '{project_id}' for query execution...")
        return client
    except Exception as e:
        print(f"ERROR: Failed to create BigQuery client: {e}")
        print("Please check your credentials and project configuration.")
        exit(1)


def execute_bigquery_query(client, custom_query):
    """
    Execute the BigQuery query to fetch MVT tile data.
    
    Args:
        client (bigquery.Client): Configured BigQuery client
        custom_query (str): SQL query to execute from configuration
        
    Returns:
        list: List of tile information dictionaries
        
    Raises:
        SystemExit: If query execution fails
    """
    print("Using query from configuration file...")
    
    try:
        print("Executing BigQuery query...")
        query_job = client.query(custom_query)
        results = query_job.result()
        
        # Process query results and build tile information
        all_tiles = []
        row_count = 0
        
        for row in results:
            # Calculate bounding box for each tile
            bbox = tile_to_bbox(row.z, row.x, row.y)
            
            tile_info = {
                'z': row.z,         # Zoom level
                'x': row.x,         # Tile X coordinate  
                'y': row.y,         # Tile Y coordinate
                'data': row.data,   # Binary MVT data
                'bbox': bbox        # Geographic bounding box (west, south, east, north)
            }
            all_tiles.append(tile_info)
            row_count += 1
            
        print(f"Successfully fetched {row_count} tiles from BigQuery!")
        
        if not all_tiles:
            print("WARNING: Query returned no results. Please check your query and data.")
            
        return all_tiles
        
    except Exception as e:
        print(f"ERROR: Failed to execute BigQuery query: {e}")
        print("Please check your query syntax and table permissions.")
        exit(1)


def get_mvt_data_from_bigquery():
    """
    Main function to fetch MVT data from BigQuery.
    
    This function coordinates the BigQuery connection, authentication,
    and data retrieval process using configuration from config.json.
    
    Returns:
        list: List of tile information dictionaries
        
    Raises:
        SystemExit: If configuration loading or BigQuery operations fail
    """
    # Step 1: Load configuration (will exit if not found)
    config = load_configuration()
    
    # Extract required configuration values
    credential_filename = config['credential_file']
    custom_query = config['bigquery_query']
    query_project_id = config['project_id']
    
    print(f"Using credential file: {credential_filename}")
    print("Using custom query from config file")
    
    # Step 2: Set up BigQuery client with authentication (will exit if fails)
    client = setup_bigquery_client(query_project_id, credential_filename)
    
    # Step 3: Execute query and fetch data (will exit if fails)
    return execute_bigquery_query(client, custom_query)


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


def display_tile_features(decoded_tile, tile_index):
    """
    Display the contents of a decoded MVT tile.
    
    Args:
        decoded_tile (dict): Decoded MVT tile data
        tile_index (int): Index of the tile for display purposes
    """
    if decoded_tile:
        print(f"--- Decoded MVT Tile {tile_index + 1} Contents ---")
        for layer_name, layer_data in decoded_tile.items():
            features = layer_data.get('features', [])
            print(f"Layer: {layer_name}")
            print(f"  Total Features: {len(features)}")
            
            # Print details of the first few features as samples
            for i, feature in enumerate(features[:3]):  # Show first 3 features
                print(f"  --- Sample Feature {i + 1} ---")
                print(f"  Geometry Type: {feature.get('geometry_type')}")
                print(f"  Properties: {feature.get('properties')}")
                # Note: Geometry coordinates here are in MVT tile space (0-4095), 
                # not WGS84 latitude/longitude.
                print(f"  Geometry (Tile Space): {feature.get('geometry')}")
            
            if len(features) > 3:
                print(f"  ... and {len(features) - 3} more features")
    else:
        print(f"Tile {tile_index + 1} is empty or failed to parse.")


def decode_mvt_tile(tile_info, tile_index):
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
        bool: True if decoding was successful, False otherwise
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
        mvt_binary = decompress_mvt_data(mvt_data)

        # Step 2: Decode the MVT using mapbox-vector-tile library
        decoded_tile = decode(mvt_binary)
        print("MVT decoded successfully")

        # Step 3: Display the decoded tile contents
        display_tile_features(decoded_tile, tile_index)
            
        return True
        
    except Exception as e:
        print(f"An error occurred decoding tile {tile_index + 1}: {e}")
        return False


def main():
    """
    Main execution function that orchestrates the entire MVT processing workflow.
    
    Workflow:
    1. Fetch MVT data from BigQuery (with fallback to hardcoded data)
    2. Process and decode each MVT tile
    3. Display processing summary
    """
    print("=== MVT Decoder - BigQuery Integration ===")
    print("Starting MVT tile processing workflow...\n")
    
    # Step 1: Fetch MVT data from BigQuery
    print("Step 1: Fetching data from BigQuery...")
    mvt_tiles_list = get_mvt_data_from_bigquery()
    
    # Step 2: Process all MVT tiles
    print(f"\nStep 2: Processing {len(mvt_tiles_list)} MVT tile(s)...")
    successful_decodes = 0
    
    for i, tile_info in enumerate(mvt_tiles_list):
        if decode_mvt_tile(tile_info, i):
            successful_decodes += 1

    # Step 3: Generate processing summary
    print(f"\n=== Processing Summary ===")
    print(f"Total tiles processed: {len(mvt_tiles_list)}")
    print(f"Successfully decoded: {successful_decodes}")
    print(f"Failed to decode: {len(mvt_tiles_list) - successful_decodes}")
    
    print(f"\n=== Processing Complete ===")
    print("MVT tiles have been successfully processed and decoded!")
    return True


# ============================================================================
# MAIN EXECUTION SECTION
# ============================================================================

if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting...")
        exit(1)
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        print("Please check your configuration and try again.")
        exit(1)