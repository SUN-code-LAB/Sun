// Neo4j Schema for MaternalSafe AI X Knowledge Graph

// Create Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Compound) REQUIRE c.smiles IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (t:Target) REQUIRE t.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (e:Evidence) REQUIRE e.pubmed_id IS UNIQUE;

// Example Node Creation Patterns
// CREATE (c:Compound {name: "Aspirin", smiles: "CC(=O)OC1=CC=CC=C1C(=O)O", mw: 180.16})
// CREATE (t:Target {name: "COX-1", type: "Enzyme"})
// CREATE (o:PregnancyOutcome {name: "Low Birth Weight"})
// CREATE (e:Evidence {pubmed_id: "12345678", title: "Study on Aspirin in Pregnancy"})

// Example Relationships
// MATCH (c:Compound {name: "Aspirin"}), (t:Target {name: "COX-1"}) CREATE (c)-[:INTERACTS_WITH]->(t)
// MATCH (c:Compound {name: "Aspirin"}), (o:PregnancyOutcome {name: "Low Birth Weight"}) CREATE (c)-[:ASSOCIATED_WITH]->(o)
// MATCH (e:Evidence), (c:Compound) WHERE e.pubmed_id = "12345678" AND c.name = "Aspirin" CREATE (e)-[:SUPPORTS]->(c)
