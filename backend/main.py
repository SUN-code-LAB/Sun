from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
import random

app = FastAPI(title="MaternalSafe AI API", description="API for MaternalSafe AI Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analyze")
def analyze_compound(smiles: str = Query(..., description="SMILES string of the compound")):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"error": "Invalid SMILES string"}

    # Calculate basic RDKit descriptors
    mw = Descriptors.MolWt(mol)
    formula = rdMolDescriptors.CalcMolFormula(mol)
    logp = Descriptors.MolLogP(mol)
    tpsa = Descriptors.TPSA(mol)
    hbd = rdMolDescriptors.CalcNumHBD(mol)
    hba = rdMolDescriptors.CalcNumHBA(mol)
    atoms = mol.GetNumAtoms()
    bonds = mol.GetNumBonds()
    rotatable_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
    aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)

    # Simple drug-likeness heuristic (Lipinski's Rule of 5)
    lipinski_violations = sum([
        mw > 500,
        logp > 5,
        hbd > 5,
        hba > 10
    ])
    drug_likeness = "Yes" if lipinski_violations <= 1 else "No"

    # Mock Placental Transfer Prediction
    placenta_prob = round(random.uniform(0.1, 0.95), 2)
    placenta_risk = "High" if placenta_prob > 0.7 else "Moderate" if placenta_prob > 0.4 else "Low"

    # Mock Breast Milk Transfer Prediction
    milk_prob = round(random.uniform(0.1, 0.95), 2)
    milk_risk = "High" if milk_prob > 0.7 else "Moderate" if milk_prob > 0.4 else "Low"

    # Mock Overall Toxicity Risk
    toxicity_score = round(random.uniform(0.1, 0.9), 2)
    toxicity_risk = "High" if toxicity_score > 0.7 else "Moderate" if toxicity_score > 0.4 else "Low"

    # Mock overall safety score (higher is safer)
    overall_safety_score = int(100 - (placenta_prob * 30 + milk_prob * 30 + toxicity_score * 40))
    overall_safety_label = "Low Risk" if overall_safety_score > 70 else "Moderate Risk" if overall_safety_score > 40 else "High Risk"

    # Mock CYP Metabolism
    cyp_metabolism = {
        "CYP3A4": random.choice(["High", "Moderate", "Low"]),
        "CYP2D6": random.choice(["High", "Moderate", "Low"]),
        "CYP2C9": random.choice(["High", "Moderate", "Low"]),
        "CYP2C19": random.choice(["High", "Moderate", "Low"]),
        "CYP1A2": random.choice(["High", "Moderate", "Low"]),
    }

    # Mock Placental Transport System
    placental_transport = {
        "ABCB1 (P-glycoprotein)": round(random.uniform(0.2, 0.9), 2),
        "ABCG2 (BCRP)": round(random.uniform(0.2, 0.9), 2),
        "SLC Transporters": round(random.uniform(0.1, 0.7), 2),
    }

    # ADMET Dashboard stats
    admet = {
        "Absorption": random.choice(["High", "Moderate", "Low"]),
        "Distribution": random.choice(["High", "Moderate", "Low"]),
        "Metabolism": random.choice(["High", "Moderate", "Low"]),
        "Excretion": random.choice(["High", "Moderate", "Low"]),
        "Toxicity": toxicity_risk
    }

    return {
        "smiles": smiles,
        "compound": "Analyzed Compound",  # In reality, might do name lookup
        "molecular_info": {
            "mw": round(mw, 2),
            "formula": formula,
            "logp": round(logp, 2),
            "tpsa": round(tpsa, 2),
            "hbd": hbd,
            "hba": hba,
            "atoms": atoms,
            "bonds": bonds,
            "rotatable_bonds": rotatable_bonds,
            "aromatic_rings": aromatic_rings,
            "drug_likeness": drug_likeness
        },
        "pregnancy_safety": {
            "placenta_transfer_prob": placenta_prob,
            "placenta_risk": placenta_risk,
            "milk_transfer_prob": milk_prob,
            "milk_risk": milk_risk,
            "toxicity_score": toxicity_score,
            "toxicity_risk": toxicity_risk,
            "overall_safety_score": overall_safety_score,
            "overall_safety_label": overall_safety_label
        },
        "cyp_metabolism": cyp_metabolism,
        "placental_transport": placental_transport,
        "admet": admet
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
