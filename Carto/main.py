"""
MVT Processor - Main orchestration class for MVT processing workflow

This is the main class that coordinates all MVT processing operations.
"""

from config_manager import ConfigManager
from bigquery_client import BigQueryClient
from mvt_tile_decoder import MVTTileDecoder
from geometry_processor import GeometryProcessor
from file_writer import FileWriter


class MVTProcessor:
    """Main processor that orchestrates the entire MVT processing workflow."""
    
    def __init__(self):
        """Initialize the MVT processor with all required components."""
        self.config_manager = ConfigManager()
        self.bigquery_client = BigQueryClient(self.config_manager)
        self.mvt_decoder = MVTTileDecoder()
        self.geometry_processor = GeometryProcessor()
        self.file_writer = FileWriter()
    
    def process_mvt_tiles(self):
        """
        Main execution function that orchestrates the entire MVT processing workflow.
        
        Workflow:
        1. Fetch MVT data from BigQuery
        2. Process and decode each MVT tile
        3. Create geometry collections
        4. Save results to file
        
        Returns:
            bool: True if processing was successful, False otherwise
        """
        print("=== MVT Decoder - BigQuery Integration ===")
        print("Starting MVT tile processing workflow...\n")
        
        try:
            # Step 1: Fetch MVT data from BigQuery
            print("Step 1: Fetching data from BigQuery...")
            mvt_tiles_list = self.bigquery_client.get_mvt_data()
            
            # Step 2: Process all MVT tiles
            print(f"\nStep 2: Processing {len(mvt_tiles_list)} MVT tile(s)...")
            successful_decodes, all_decoded_tiles = self._process_tiles(mvt_tiles_list)
            
            # Step 3: Generate processing summary
            self._print_processing_summary(mvt_tiles_list, successful_decodes)
            
            # Step 4: Create combined geometry collection
            print(f"\nStep 3: Creating combined geometry collection...")
            geometry_collection = self.geometry_processor.create_geometry_collection(mvt_tiles_list)
            
            # Step 5: Save geometry collection to file
            print("Step 4: Saving geometries to files...")
            formatted_filename = self.file_writer.save_geometry_collection_to_file(
                geometry_collection, len(mvt_tiles_list), mvt_tiles_list, all_decoded_tiles
            )
            
            # Step 6: Display results
            self._print_results(formatted_filename, mvt_tiles_list, geometry_collection)
            
            print(f"\n=== Processing Complete ===")
            print("MVT tiles have been successfully processed and combined into a geometry collection!")
            return True
            
        except Exception as e:
            print(f"\nERROR: Processing failed: {e}")
            return False
    
    def _process_tiles(self, mvt_tiles_list):
        """
        Process all MVT tiles and return results.
        
        Args:
            mvt_tiles_list (list): List of tile information dictionaries
            
        Returns:
            tuple: (successful_decodes: int, all_decoded_tiles: list)
        """
        successful_decodes = 0
        all_decoded_tiles = []
        
        for i, tile_info in enumerate(mvt_tiles_list):
            success, decoded_tile = self.mvt_decoder.decode_mvt_tile(tile_info, i)
            if success:
                successful_decodes += 1
            all_decoded_tiles.append(decoded_tile)
        
        return successful_decodes, all_decoded_tiles
    
    def _print_processing_summary(self, mvt_tiles_list, successful_decodes):
        """Print processing summary statistics."""
        print(f"\n=== Processing Summary ===")
        print(f"Total tiles processed: {len(mvt_tiles_list)}")
        print(f"Successfully decoded: {successful_decodes}")
        print(f"Failed to decode: {len(mvt_tiles_list) - successful_decodes}")
    
    def _print_results(self, formatted_filename, mvt_tiles_list, geometry_collection):
        """Print final results and file information."""
        print(f"\n=== Geometry Files Generated ===")
        print(f"Comprehensive geometry file: Carto/{formatted_filename}")
        print(f"Total tiles in collection: {len(mvt_tiles_list)}")
        
        # Display a preview of the geometry collection
        preview_length = 200
        if len(geometry_collection) > preview_length:
            preview = geometry_collection[:preview_length] + "..."
        else:
            preview = geometry_collection
        
        print(f"\nGeometry Collection Preview:")
        print(f"  {preview}")


def main():
    """Main entry point for the MVT processing application."""
    processor = MVTProcessor()
    return processor.process_mvt_tiles()


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