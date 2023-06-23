import json
from pathlib import Path

openapi_json_fileppath = (
    Path(__file__).parent.parent / "dnd5esheets" / "client" / "openapi.json"
)

openapi_content = json.loads(openapi_json_fileppath.read_text())

for path_data in openapi_content["paths"].values():
    for operation in path_data.values():
        tag = operation["tags"][0]
        operation_id = operation["operationId"]
        to_remove = f"{tag}-"
        new_operation_id = operation_id[len(to_remove) :]
        operation["operationId"] = new_operation_id

openapi_json_fileppath.write_text(json.dumps(openapi_content, indent=2))
