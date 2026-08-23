from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
import random

app = FastAPI(title="RENAL ADMET AI API", description="API for RENAL ADMET AI Platform")

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
    rings = rdMolDescriptors.CalcNumRings(mol)
    rotatable_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
    aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)

    # Solubility heuristic
    solubility = "High" if logp < 3 and mw < 400 else "Moderate" if logp < 5 else "Low"

    # Simple drug-likeness heuristic (Lipinski's Rule of 5)
    lipinski = {
        "mw": mw < 500,
        "logp": logp < 5,
        "hbd": hbd < 5,
        "hba": hba < 10
    }
    lipinski_violations = sum([not v for v in lipinski.values()])
    drug_likeness = "Yes" if lipinski_violations <= 1 else "No"

    # Mock Overall Risk
    risk_score = round(random.uniform(0.1, 0.9), 2)
    overall_safety_label = "🟢 Low Risk" if risk_score < 0.4 else "🟡 Moderate Risk" if risk_score < 0.7 else "🔴 High Risk"

    # Mock CYP Metabolism
    cyp_metabolism = {
        "CYP3A4": random.choice(["High", "Moderate", "Low"]),
        "CYP2D6": random.choice(["High", "Moderate", "Low"]),
        "CYP2C9": random.choice(["High", "Moderate", "Low"]),
        "CYP2C19": random.choice(["High", "Moderate", "Low"]),
        "CYP1A2": random.choice(["High", "Moderate", "Low"]),
    }

    # Mock Renal Transport System
    renal_transport = {
        "OAT1": round(random.uniform(0.6, 0.95), 2),
        "OAT3": round(random.uniform(0.4, 0.8), 2),
        "OCT2": round(random.uniform(0.5, 0.9), 2),
        "MATE1": round(random.uniform(0.2, 0.7), 2),
        "MATE2-K": round(random.uniform(0.1, 0.6), 2),
    }

    # Mock Kidney Toxicity
    kidney_toxicity = {
        "Tubular Injury": round(random.uniform(0.1, 0.9), 2),
        "Oxidative Stress": round(random.uniform(0.1, 0.9), 2),
        "Mitochondrial Toxicity": round(random.uniform(0.1, 0.5), 2),
    }

    # ADMET Dashboard stats
    admet = {
        "Absorption": random.choice(["High", "Moderate", "Low"]),
        "Distribution": random.choice(["High", "Moderate", "Low"]),
        "Metabolism": random.choice(["High", "Moderate", "Low"]),
        "Excretion": random.choice(["High", "Moderate", "Low"]),
        "Toxicity": random.choice(["High", "Moderate", "Low"])
    }

    return {
        "smiles": smiles,
        "compound": "Aspirin", # Mocked as aspirin for dashboard defaults
        "molecular_info": {
            "mw": round(mw, 2),
            "formula": formula,
            "logp": round(logp, 2),
            "tpsa": round(tpsa, 2),
            "solubility": solubility,
            "hbd": hbd,
            "hba": hba,
            "atoms": atoms,
            "bonds": bonds,
            "rings": rings,
            "rotatable_bonds": rotatable_bonds,
            "aromatic_rings": aromatic_rings,
            "drug_likeness": drug_likeness,
            "lipinski": lipinski
        },
        "overall_safety_label": overall_safety_label,
        "cyp_metabolism": cyp_metabolism,
        "renal_transport": renal_transport,
        "kidney_toxicity": kidney_toxicity,
        "admet": admet
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
