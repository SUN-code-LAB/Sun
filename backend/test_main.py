from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_valid_smiles():
    response = client.get("/api/analyze?smiles=CC(=O)OC1=CC=CC=C1C(=O)O")
    assert response.status_code == 200
    data = response.json()
    assert "molecular_info" in data
    assert data["molecular_info"]["formula"] == "C9H8O4"
    assert data["smiles"] == "CC(=O)OC1=CC=CC=C1C(=O)O"

def test_analyze_invalid_smiles():
    response = client.get("/api/analyze?smiles=INVALID")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Invalid SMILES string"
