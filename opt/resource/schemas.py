source_schema = {
    "type": "object",
    "properties": {
        "access_key_id": {
            "type": "string"
        },
        "secret_access_key": {
            "type": "string"
        },
        "region_name": {
            "type": "string"
        }
    },
    "required": [
        "access_key_id",
        "secret_access_key"
    ]
}

version_schema = {
    "oneOf": [{
        "type": "object",
        "properties": {
            "schema": {
                "type": "string"
            }
        }
    }, {
        "type": "null"
    }]
}

check_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": source_schema,
        "version": version_schema
    },
    "required": [
        "source"
    ]
}

out_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": source_schema,
        "params": {
            "type": "object",
            "properties": {
                "stageFile": {
                    "type": "string"
                },
                "stage": {
                    "type": "string"
                },
                "deploy": {
                    "type": "boolean"
                },
                "remove": {
                    "type": "boolean"
                },
                "serverless_file": {
                    "type": "string"
                },
                "artifact_folder": {
                    "type": "string"
                }
            },
            "oneOf": [{
                "required": ["deploy"]
            }, {
                "required": ["remove"]
            }],
            "dependencies": {
                "deploy": {
                    "required": {
                        "serverless_file",
                        "artifact_folder"
                    }
                },
                "remove": {
                    "required": {
                        "serverless_file"
                    }
                }
            },
            "additionalProperties": "false"
        }
    },
    "required": [
        "source",
        "params"
    ]
}

in_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": source_schema,
        "version": version_schema
    },
    "required": [
        "source",
        "version"
    ]
}
