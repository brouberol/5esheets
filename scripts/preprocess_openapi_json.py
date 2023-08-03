import inspect
import json
from pathlib import Path

from dnd5esheets import schemas

openapi_json_filepath = (
    Path(__file__).parent.parent / "dnd5esheets" / "front" / "openapi.json"
)

openapi_content = json.loads(openapi_json_filepath.read_text())

# taken from https://fastapi.tiangolo.com/advanced/generate-clients/#fastapi-app-with-tags
# generates sensible tags for each operation, to make sure the code is as human-readable as possible
for path_data in openapi_content["paths"].values():
    for operation in path_data.values():
        tag = operation["tags"][0]
        operation_id = operation["operationId"]
        to_remove = f"{tag}-"
        new_operation_id = operation_id[len(to_remove) :]
        operation["operationId"] = new_operation_id

# Hack: Mark frontend evaluated schema fields as non optional, as we send a non-nil default
# value server-side, to make sure the associated fields in the TS client are marked
# as non-optional.
for name, schema in openapi_content["components"]["schemas"].items():
    for property_name, property_meta in schema.get("properties", {}).items():
        if property_meta.get("description") == "frontend_computed":
            property_meta.pop("default")
            property_meta.pop("description")
            schema["required"].append(property_name)

# Hack: while https://github.com/tiangolo/fastapi/discussions/9856 is open,
# we need to manually register computed_property fields into the OpenAPI schema
schema_classes = {
    local_var
    for local_var in vars(schemas).values()
    if inspect.isclass(local_var)
    and local_var != schemas.BaseSchema
    and issubclass(local_var, schemas.BaseSchema)
}
python_type_to_openapi = {bool: "boolean"}
for schema_class in schema_classes:
    if computed_fields := schema_class.__pydantic_decorators__.computed_fields:
        for field, decorator in computed_fields.items():
            return_type = decorator.func.__annotations__["return"]
            openapi_return_type = python_type_to_openapi[return_type]
            openapi_content["components"]["schemas"][schema_class.__name__][
                "properties"
            ][field] = {"type": openapi_return_type, "title": decorator.func.__doc__}

openapi_json_filepath.write_text(json.dumps(openapi_content, indent=2))
