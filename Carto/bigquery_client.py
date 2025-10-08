"""
BigQuery Client for MVT Decoder

Handles BigQuery authentication, connection, and data retrieval.
"""

import os
from google.cloud import bigquery
from coordinate_converter import CoordinateConverter


class BigQueryClient:
    """Manages BigQuery client setup and data retrieval for MVT tiles."""
    
    def __init__(self, config_manager):
        """
        Initialize the BigQuery client.
        
        Args:
            config_manager: ConfigManager instance for accessing configuration
        """
        self.config_manager = config_manager
        self.client = None
        self.coordinate_converter = CoordinateConverter()
    
    def setup_client(self, project_id, credential_filename):
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
        credential_file = self.config_manager.find_service_account_credentials(credential_filename)
        
        print(f"Using service account credentials from: {credential_file}")
        # Set environment variable for Google Cloud authentication
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_file
            
        try:
            self.client = bigquery.Client(project=project_id)
            print(f"Using project '{project_id}' for query execution...")
            return self.client
        except Exception as e:
            print(f"ERROR: Failed to create BigQuery client: {e}")
            print("Please check your credentials and project configuration.")
            exit(1)
    
    def execute_query(self, custom_query):
        """
        Execute the BigQuery query to fetch MVT tile data.
        
        Args:
            custom_query (str): SQL query to execute from configuration
            
        Returns:
            list: List of tile information dictionaries
            
        Raises:
            SystemExit: If query execution fails
        """
        if self.client is None:
            raise ValueError("BigQuery client not initialized. Call setup_client() first.")
        
        print("Using query from configuration file...")
        
        try:
            print("Executing BigQuery query...")
            query_job = self.client.query(custom_query)
            results = query_job.result()
            
            # Process query results and build tile information
            all_tiles = []
            row_count = 0
            
            for row in results:
                # Calculate bounding box for each tile
                bbox = self.coordinate_converter.tile_to_bbox(row.z, row.x, row.y)
                
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
    
    def get_mvt_data(self):
        """
        Main function to fetch MVT data from BigQuery.
        
        This function coordinates the BigQuery connection, authentication,
        and data retrieval process using configuration.
        
        Returns:
            list: List of tile information dictionaries
            
        Raises:
            SystemExit: If configuration loading or BigQuery operations fail
        """
        # Load configuration
        config = self.config_manager.load_configuration()
        
        # Extract required configuration values
        credential_filename = config['credential_file']
        custom_query = config['bigquery_query']
        query_project_id = config['project_id']
        
        print(f"Using credential file: {credential_filename}")
        print("Using custom query from config file")
        
        # Set up BigQuery client with authentication
        self.setup_client(query_project_id, credential_filename)
        
        # Execute query and fetch data
        return self.execute_query(custom_query)