from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_compound():
    response = client.get("/api/analyze?smiles=CC(=O)OC1=CC=CC=C1C(=O)O")
    assert response.status_code == 200
    data = response.json()
    assert data["smiles"] == "CC(=O)OC1=CC=CC=C1C(=O)O"
    assert "molecular_info" in data
    assert "pregnancy_safety" in data
    assert "cyp_metabolism" in data
    assert "placental_transport" in data
    assert "admet" in data
    assert data["molecular_info"]["mw"] > 180
    assert data["molecular_info"]["drug_likeness"] == "Yes"

def test_invalid_smiles():
    response = client.get("/api/analyze?smiles=INVALID")
    assert response.status_code == 200
    assert "error" in response.json()
