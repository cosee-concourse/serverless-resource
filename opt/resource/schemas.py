checkSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": {
            "type": "object",
            "properties": {
                "apiKey": {
                    "type": "string"
                },
                "secretKey": {
                    "type": "string"
                }
            },
            "required": [
                "apiKey",
                "secretKey"
            ]
        },
        "version": {
            "oneOf": [{
                "type": "object",
                "properties": {
                    "ref": {
                        "type": "string"
                    }
                }
            }, {
                "type": "null"
            }]
        }
    },
    "required": [
        "source"
    ]
}

outSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": {
            "type": "object",
            "properties": {
                "apiKey": {
                    "type": "string"
                },
                "secretKey": {
                    "type": "string"
                }
            },
            "required": [
                "apiKey",
                "secretKey"
            ]
        },
        "params": {
            "type": "object",
            "properties": {
                "appFile": {
                    "type": "string"
                },
                "appName": {
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
                "required": ["appFile"]
            }, {
                "required": ["appName"]
            }],
            "oneOf": [{
                "required": ["deploy"]
            }, {
                "required": ["delete"]
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
