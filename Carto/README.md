# MVT Decoder - BigQuery Integration

This script decodes Mapbox Vector Tile (MVT) data fetched from Google BigQuery.

## Prerequisites

1. **Google Cloud SDK** - Install and configure authentication
2. **Python 3.7+** - Required for the script
3. **Virtual Environment** - Recommended for dependency isolation

## Setup Instructions

### 1. Clone/Download the project
```bash
cd /path/to/your/project
```

### 2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate    # macOS/Linux
# OR
venv\Scripts\activate       # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the script using config.json (REQUIRED)

**The script requires a `config.json` file to run.** 

**IMPORTANT**: Copy `config.json.template` to `config.json` and update with your values:

```bash
cp config.json.template config.json
# Then edit config.json with your actual values
```

Create the `config.json` file in the same directory as the script:

```json
{
  "credential_file": "your-service-account-file.json",
  "project_id": "your-project-id",
  "bigquery_query": "SELECT t.z, t.x, t.y, t.data FROM `project.dataset.table` AS t WHERE z = 2"
}
```

**Required Configuration Fields:**
- `credential_file`: Name of your Google Cloud service account JSON file (REQUIRED)
- `project_id`: Google Cloud project ID for running queries (REQUIRED)
- `bigquery_query`: The BigQuery SQL query to fetch MVT data (REQUIRED)

**Note:** The script will exit with an error if:
- The `config.json` file is missing
- The JSON syntax is invalid  
- Either required field is missing

### 5. Configure Google Cloud Authentication

Place your service account credential file in one of these locations:
- Same directory as the script
- Parent directory
- Your home directory

The script will automatically search for the credential file specified in `config.json`.

## Usage

Run the script:
```bash
python MVT_decoder.py
```

The script will:
1. Load configuration from `config.json`
2. Connect to BigQuery using your configured credentials
3. Execute the custom query to fetch MVT data
4. Decode the compressed MVT data
5. Display the decoded tile contents including layers and features

## Configuration File Format

The `config.json` file supports the following options:

```json
{
  "credential_file": "your-service-account-file.json",
  "project_id": "your-google-cloud-project-id",
  "bigquery_query": "SELECT t.z, t.x, t.y, t.data FROM `your-project.your-dataset.your-table` AS t WHERE z = 13 LIMIT 10"
}
```

**Notes:**
- Both fields in `config.json` are mandatory - the script will fail if either is missing
- The credential file must exist in one of the searched locations
- The script provides clear error messages if configuration or credentials are missing

## Dependencies

- `mapbox-vector-tile` - For decoding MVT data
- `google-cloud-bigquery` - For BigQuery integration
- Standard Python libraries: `base64`, `gzip`, `json`, `os`

## Troubleshooting

### Configuration Errors
- Ensure `config.json` is in the same directory as `MVT_decoder.py`
- Verify JSON syntax is valid
- Check that credential file exists in the specified location

### Authentication Errors
- Ensure Google Cloud credentials are properly configured
- Verify your service account has BigQuery access permissions
- Check that the dataset/table exists and you have read permissions

### Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Query Errors
- Verify the BigQuery table name and structure in your `config.json`
- Ensure your credentials have access to the specified dataset
- Check the SQL syntax in your custom query