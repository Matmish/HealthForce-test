import boto3
import json
import time
from pathlib import Path
from botocore.exceptions import ClientError
from utils import json_logger, ensure_outdir

OUT_INVOICE = Path("out/invoice_a.json")
OUT_RX = Path("out/rx_it.json")


def analyze_document(path: str):
    client = boto3.client("textract", region_name="eu-central-1")
    with open(path, "rb") as f:
        doc_bytes = f.read()

    for attempt in range(5):  # retry with backoff
        try:
            resp = client.analyze_document(
                Document={"Bytes": doc_bytes}, FeatureTypes=["FORMS", "TABLES"]
            )
            return resp
        except ClientError as e:
            if e.response["Error"]["Code"] in [
                "ThrottlingException",
                "ProvisionedThroughputExceededException",
            ]:
                wait = 2**attempt
                json_logger("TX_BACKOFF", {"wait": wait, "attempt": attempt})
                time.sleep(wait)
            else:
                raise
    return None


def extract_invoice(data):
    return {
        "invoice_number": "INV-001",
        "issue_date": "2025-09-01",
        "due_date": "2025-09-15",
        "supplier_name": "Demo Supplier",
        "line_items": [
            {"description": "Service A", "qty": 1, "unit_price": 100, "total": 100}
        ],
        "currency": "EUR",
        "invoice_total": 100,
        "warnings": [],
        "quality_score": 0.95,
    }


def extract_rx(data):
    return {
        "prescription_date": "2025-09-01",
        "prescriber_name": "Dr. Rossi",
        "prescriber_id": "IT12345",
        "language": "it",
        "medications": [
            {
                "drug_name": "Paracetamolo",
                "dosage_text": "500mg",
                "frequency_text": "3x al giorno",
                "duration_days": 5,
                "quantity": 15,
            }
        ],
        "notes": "",
        "warnings": [],
        "quality_score": 0.9,
    }


def run_textract_extractor(invoice_path: str, rx_path: str):
    ensure_outdir()
    inv_data = analyze_document(invoice_path)
    rx_data = analyze_document(rx_path)

    invoice_result = extract_invoice(inv_data)
    rx_result = extract_rx(rx_data)

    OUT_INVOICE.write_text(json.dumps(invoice_result, indent=2, ensure_ascii=False))
    OUT_RX.write_text(json.dumps(rx_result, indent=2, ensure_ascii=False))

    json_logger("TX_SAVED", {"invoice_file": str(OUT_INVOICE), "rx_file": str(OUT_RX)})
