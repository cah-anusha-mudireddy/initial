{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "advance_directives",
  "type": "object",
  "properties": {
    "patient_id": {
      "type": "string",
      "pattern": "^\\w+$"
    },
    "advance_directive_id": {
      "type": "string",
      "pattern": "^\\w+$"
    },
    "dnr": {
      "enum": [
        "Y",
        "N",
        ""
      ]
    },
    "lw": {
      "enum": [
        "Y",
        "N",
        ""
      ]
    },
    "dpa": {
      "enum": [
        "Y",
        "N",
        ""
      ]
    },
    "transaction_timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "extract_generation_datetime": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "patient_id",
    "advance_directive_id",
    "dnr",
    "lw",
    "dpa",
    "transaction_timestamp"
  ]
}