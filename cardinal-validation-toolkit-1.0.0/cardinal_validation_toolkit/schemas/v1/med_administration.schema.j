{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "med_administration",
  "type": "object",
  "properties": {
    "patient_id": {
      "type": "string",
      "pattern": "^\\w+$"
    },
    "administration_id": {
      "type": "string",
      "pattern": "^\\w+$"
    },
    "dose_administered": {
      "type": "string",
      "pattern": "^\\w+$"
    },
    "dose_approved": {
      "enum": [
        "Y",
        ""
      ]
    },
    "drug_name": {
      "type": "string",
      "pattern": "^\\w+$"
    },
    "form": {
      "type": "string"
    },
    "ndc_code": {
      "type": "string",
      "pattern": "^(\\d{5}-\\d{3}-\\d{2})?$"
    },
    "ordered_date": {
      "type": "string",
      "format": "date-time"
    },
    "administered_units": {
      "type": "string",
      "pattern": "^\\w+$"
    },
    "route": {
      "enum": [
        "CI",
        "IM",
        "IT",
        "IV",
        "IVC",
        "IVP",
        "Other",
        "PO",
        "SQ",
        "ID",
        "INH",
        "IVP",
        "gtts",
        "IUD",
        "NC"
      ]
    },
    "transaction_timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "administration_timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "icd_code": {
      "type": "string"
    },
    "diagnosis_code_sys": {
      "enum": [
        "ICD-10-CM",
        "ICD-9-CM",
        ""
      ]
    },
    "extract_generation_datetime": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "patient_id",
    "administration_id",
    "dose_administered",
    "dose_approved",
    "drug_name",
    "form",
    "ndc_code",
    "ordered_date",
    "administered_units",
    "route",
    "transaction_timestamp",
    "administration_timestamp",
    "icd_code",
    "diagnosis_code_sys"
  ]
}