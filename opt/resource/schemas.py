sourceSchema = {
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

versionSchema = {
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

checkSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": sourceSchema,
        "version": versionSchema
    },
    "required": [
        "source"
    ]
}

outSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": sourceSchema,
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
                "delete": {
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
                "required": ["stageFile"]
            }, {
                "required": ["stage"]
            }],
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

inSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": sourceSchema,
        "version": versionSchema
    },
    "required": [
        "source",
        "version"
    ]
}
