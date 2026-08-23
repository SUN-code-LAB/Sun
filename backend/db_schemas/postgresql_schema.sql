-- PostgreSQL Schema for MaternalSafe AI X

CREATE TABLE IF NOT EXISTS compounds (
    id SERIAL PRIMARY KEY,
    pubchem_cid INTEGER UNIQUE,
    name VARCHAR(255) NOT NULL,
    smiles TEXT NOT NULL,
    formula VARCHAR(100),
    mw DECIMAL,
    logp DECIMAL,
    tpsa DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS toxicity_predictions (
    id SERIAL PRIMARY KEY,
    compound_id INTEGER REFERENCES compounds(id) ON DELETE CASCADE,
    model_version VARCHAR(50),
    developmental_risk VARCHAR(50),
    embryotoxicity VARCHAR(50),
    prediction_score DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transfer_predictions (
    id SERIAL PRIMARY KEY,
    compound_id INTEGER REFERENCES compounds(id) ON DELETE CASCADE,
    placenta_prob DECIMAL,
    breast_milk_prob DECIMAL,
    milk_plasma_ratio DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
