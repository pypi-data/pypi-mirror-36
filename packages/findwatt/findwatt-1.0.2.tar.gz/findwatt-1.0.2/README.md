# findwatt-python

Python client for FindWAtt's API

# Installation
```
pip install findwatt
```

# Usage
```python
import findwatt

api_key = 'my-api-key'
client = findwatt.Client(api_key)
```

Uploading a file to a new Catalog
```python
p = '/path/to/file.xlsx'
upload = client.upload_file(p, catalog_name='My New Catalog')
```

Uploading a file to an existing Catalog
```python
p = '/path/to/file.xlsx'
upload = client.upload_file(p, catalog_id='my-existing-catalog-id')
```

Listing and searching your Catalogs
```python
my_catalogs = client.catalogs.search()
my_filtered_catalogs = client.catalogs.search(name="Dummy Catalog")
```

Fetching a particular Catalog
```python
my_catalog = client.catalogs.get('dummy-catalog')
```

Fetching a particular Dataset
```python
my_dataset = client.datasets.get('my-dataset')
```

# Advanced Usage
findwatt.Client takes an optional api_url parameter that can be set to use a mock or staging API
```python
import findwatt

api_key = 'my-api-key'
client = findwatt.Client(api_key, api_url='http://localhost:3000/')
```