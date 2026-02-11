import csv
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "MyNewPass123!")  # ✅ Confirm this password is correct!

File_name = 'graph/Relationship'

def create_relationships(tx, batch):
    tx.run("""
    UNWIND $batch AS rel
    // Dynamically match source and target nodes by label + property
    CALL apoc.cypher.run(
      'MATCH (n:`' + rel.src_label + '` {Name: $name}) RETURN n AS node',
      {name: rel.src}
    ) YIELD value AS src_result

    CALL apoc.cypher.run(
      'MATCH (n:`' + rel.dst_label + '` {Name: $name}) RETURN n AS node',
      {name: rel.tgt}
    ) YIELD value AS dst_result

    WITH rel, src_result.node AS a, dst_result.node AS b
    WHERE a IS NOT NULL AND b IS NOT NULL
    CALL apoc.create.relationship(a, rel.type, {source: 'import'}, b) YIELD rel AS r
    RETURN count(r) AS created
    """, batch=batch)

rels = []
try:
    with open(File_name, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            # Skip empty or malformed rows
            if not row.get('Src_Name') or not row.get('Dst_Name') or not row.get('Relationship'):
                continue
            rels.append({
                'src_label':row['Src_Label'].strip(),
                'src': row['Src_Name'].strip(),
                'dst_label':row['Dst_Label'].strip(),
                'tgt': row['Dst_Name'].strip(),
                'type': row['Relationship'].strip()  # e.g., "BASED_ON", "EXTENDS"
            })
except FileNotFoundError:
    print("❌ File not found! Check path: 'graph/Root_R_Fundamental_Model'")
    exit(1)
except Exception as e:
    print(f"❌ Error reading file: {e}")
    exit(1)

if not rels:
    print("⚠️ No relationships loaded — check file format & headers.")
    exit(0)

print(f"📤 Preparing to load {len(rels)} relationships...")

# Batch insert
driver = GraphDatabase.driver(URI, auth=AUTH)

# Optional: Verify connectivity & APOC availability
with driver.session() as session:
    try:
        session.run("RETURN 1").consume()
        print("✅ Connected to Neo4j.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        driver.close()
        exit(1)

    # Check if APOC is available (critical for dynamic rel types)
    try:
        session.run("RETURN apoc.version()").single()
        print("✅ APOC is available.")
    except:
        print("⚠️ APOC not found! Install it or use fixed relationship types.")
        # Alternative: fallback to static rel type — see note below.

# Do batch insertion
batch_size = 500  # Smaller batches reduce memory pressure
total_created = 0

with driver.session() as session:
    for i in range(0, len(rels), batch_size):
        batch = rels[i:i + batch_size]
        try:
            result = session.execute_write(create_relationships, batch)
            # `result` is a Result object; extract summary
            summary = result.consume()
            # Since our Cypher returns count(r), we can fetch it:
            # But easier: just count input batch size for progress
            created_in_batch = len(batch)  # approximate (skips missing nodes)
            total_created += created_in_batch
            print(f"  → Batch {i//batch_size + 1}: {len(batch)} attempted")
        except Exception as e:
            print(f"❌ Batch {i//batch_size + 1} failed: {e}")
            continue

driver.close()
print(f"✅ Done! Attempted {len(rels)} relationships. (Check for missing nodes if count seems low.)")