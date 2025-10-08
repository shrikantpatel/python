"""
Configuration Manager for MVT Decoder

Handles loading and validation of configuration files.
"""

import os
import json


class ConfigManager:
    """Manages configuration loading and validation for the MVT decoder."""
    
    def __init__(self, config_filename='config.json'):
        """
        Initialize the configuration manager.
        
        Args:
            config_filename (str): Name of the configuration file
        """
        self.config_filename = config_filename
        self.config = None
    
    def load_configuration(self):
        """
        Load configuration from config.json file in the same directory as the script.
        
        Returns:
            dict: Configuration dictionary containing credential_file and bigquery_query
            
        Raises:
            SystemExit: If config file cannot be loaded or is invalid
        """
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(script_dir, self.config_filename)
        
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
                print(f"Configuration loaded from: {config_file}")
                
                # Validate required fields
                self._validate_configuration()
                
                return self.config
        except FileNotFoundError:
            self._handle_config_not_found(config_file)
        except json.JSONDecodeError as e:
            self._handle_json_error(e)
        except Exception as e:
            self._handle_general_error(e)
    
    def _validate_configuration(self):
        """Validate that all required configuration fields are present."""
        required_fields = ['credential_file', 'bigquery_query', 'project_id']
        missing_fields = [field for field in required_fields if field not in self.config]
        
        if missing_fields:
            print(f"ERROR: Missing required configuration fields: {missing_fields}")
            print("Please ensure config.json contains 'credential_file', 'bigquery_query', and 'project_id'")
            exit(1)
    
    def _handle_config_not_found(self, config_file):
        """Handle case when configuration file is not found."""
        print(f"ERROR: Configuration file not found: {config_file}")
        print("Please create a config.json file in the same directory as this script.")
        print("Example config.json:")
        print('{"credential_file": "your-service-account.json", "bigquery_query": "SELECT t.z, t.x, t.y, t.data FROM `your-table` AS t WHERE z = 2", "project_id": "your-project-id"}')
        exit(1)
    
    def _handle_json_error(self, error):
        """Handle JSON parsing errors."""
        print(f"ERROR: Invalid JSON in configuration file: {error}")
        print("Please check the syntax of your config.json file.")
        exit(1)
    
    def _handle_general_error(self, error):
        """Handle general configuration loading errors."""
        print(f"ERROR: Failed to load configuration: {error}")
        exit(1)
    
    def find_service_account_credentials(self, credential_filename):
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
    
    def get_config_value(self, key):
        """
        Get a specific configuration value.
        
        Args:
            key (str): Configuration key to retrieve
            
        Returns:
            Any: Configuration value
            
        Raises:
            ValueError: If configuration not loaded or key not found
        """
        if self.config is None:
            raise ValueError("Configuration not loaded. Call load_configuration() first.")
        
        if key not in self.config:
            raise ValueError(f"Configuration key '{key}' not found.")
        
        return self.config[key]