import json
from pathlib import Path

openapi_json_fileppath = (
    Path(__file__).parent.parent / "dnd5esheets" / "front" / "openapi.json"
)

openapi_content = json.loads(openapi_json_fileppath.read_text())

# taken from https://fastapi.tiangolo.com/advanced/generate-clients/#fastapi-app-with-tags
# generates sensible tags for each operation, to make sure the code is as human-readable as possible
for path_data in openapi_content["paths"].values():
    for operation in path_data.values():
        tag = operation["tags"][0]
        operation_id = operation["operationId"]
        to_remove = f"{tag}-"
        new_operation_id = operation_id[len(to_remove) :]
        operation["operationId"] = new_operation_id

# Mark frontend evaluated schema fields as non optional, as we send a non-nil default
# value server-side, to make sure the associated fields in the TS client are marked
# as non-optional.
for name, schema in openapi_content["components"]["schemas"].items():
    for property_name, property_meta in schema.get("properties", {}).items():
        if property_meta.get("description") == "frontend_computed":
            property_meta.pop("default")
            property_meta.pop("description")
            schema["required"].append(property_name)

openapi_json_fileppath.write_text(json.dumps(openapi_content, indent=2))
