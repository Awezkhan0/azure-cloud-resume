Now let's create the function code. In your GitHub repo:

1. Click **Add file** → **Create new file**
2. In the filename box type `api/function_app.py` (typing the slash automatically creates the folder)

Then paste this code in:

```python
import azure.functions as func
import logging
from azure.data.tables import TableServiceClient
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor-counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Visitor counter function triggered.')

    connection_string = os.environ["COSMOS_CONNECTION_STRING"]
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service.get_table_client(table_name="visitors")

    try:
        entity = table_client.get_entity(partition_key="counter", row_key="visits")
        count = entity["Count"] + 1
        entity["Count"] = count
        table_client.update_entity(entity)
    except:
        count = 1
        table_client.create_entity({
            "PartitionKey": "counter",
            "RowKey": "visits",
            "Count": count
        })

    return func.HttpResponse(
        json.dumps({"count": count}),
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )
```

Commit the file when done and let me know.
