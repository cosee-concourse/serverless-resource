sourceSchema = {
    "type": "object",
    "properties": {
        "apiKey": {
            "type": "string"
        },
        "secretKey": {
            "type": "string"
        },
        "region": {
            "type": "string"
        }
    },
    "required": [
        "apiKey",
        "secretKey"
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
                "serverlessFile": {
                    "type": "string"
                },
                "directory": {
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
            "required": ["directory"],
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
