import argparse
import os
import random
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

INSTITUTIONS = [
    {"id": "mit", "name": "MIT", "country": "USA", "ranking": 1},
    {"id": "stanford", "name": "Stanford University", "country": "USA", "ranking": 2},
    {"id": "cmu", "name": "Carnegie Mellon University", "country": "USA", "ranking": 3},
    {"id": "oxford", "name": "University of Oxford", "country": "UK", "ranking": 4},
    {"id": "cambridge", "name": "University of Cambridge", "country": "UK", "ranking": 5},
    {"id": "eth", "name": "ETH Zurich", "country": "Switzerland", "ranking": 6},
    {"id": "berkeley", "name": "UC Berkeley", "country": "USA", "ranking": 7},
    {"id": "tsinghua", "name": "Tsinghua University", "country": "China", "ranking": 8},
    {"id": "toronto", "name": "University of Toronto", "country": "Canada", "ranking": 9},
    {"id": "singapore", "name": "National University of Singapore", "country": "Singapore", "ranking": 10},
    {"id": "epfl", "name": "EPFL", "country": "Switzerland", "ranking": 11},
    {"id": "caltech", "name": "Caltech", "country": "USA", "ranking": 12},
    {"id": "columbia", "name": "Columbia University", "country": "USA", "ranking": 13},
    {"id": "princeton", "name": "Princeton University", "country": "USA", "ranking": 14},
    {"id": "ucl", "name": "University College London", "country": "UK", "ranking": 15},
]

TOPICS = [
    {"id": "ml", "name": "Machine Learning", "category": "Computer Science"},
    {"id": "nlp", "name": "Natural Language Processing", "category": "Computer Science"},
    {"id": "cv", "name": "Computer Vision", "category": "Computer Science"},
    {"id": "rl", "name": "Reinforcement Learning", "category": "Computer Science"},
    {"id": "graphs", "name": "Graph Neural Networks", "category": "Computer Science"},
    {"id": "bio", "name": "Bioinformatics", "category": "Biology"},
    {"id": "genomics", "name": "Genomics", "category": "Biology"},
    {"id": "proteomics", "name": "Proteomics", "category": "Biology"},
    {"id": "neuro", "name": "Computational Neuroscience", "category": "Neuroscience"},
    {"id": "climate", "name": "Climate Modeling", "category": "Environmental Science"},
    {"id": "materials", "name": "Materials Science", "category": "Physics"},
    {"id": "quantum", "name": "Quantum Computing", "category": "Physics"},
    {"id": "robotics", "name": "Robotics", "category": "Engineering"},
    {"id": "ethics", "name": "AI Ethics", "category": "Philosophy"},
    {"id": "privacy", "name": "Data Privacy", "category": "Computer Science"},
    {"id": "health", "name": "Digital Health", "category": "Medicine"},
    {"id": "drug", "name": "Drug Discovery", "category": "Medicine"},
    {"id": "energy", "name": "Energy Systems", "category": "Engineering"},
    {"id": "networks", "name": "Network Science", "category": "Computer Science"},
    {"id": "optimization", "name": "Mathematical Optimization", "category": "Mathematics"},
]

AUTHORS = [
    {"id": "a01", "name": "Alice Chen", "h_index": 85, "institution": "mit"},
    {"id": "a02", "name": "Bob Williams", "h_index": 72, "institution": "stanford"},
    {"id": "a03", "name": "Carlos Ruiz", "h_index": 68, "institution": "cmu"},
    {"id": "a04", "name": "Diana Patel", "h_index": 91, "institution": "oxford"},
    {"id": "a05", "name": "Erik Johansson", "h_index": 56, "institution": "eth"},
    {"id": "a06", "name": "Fang Li", "h_index": 78, "institution": "tsinghua"},
    {"id": "a07", "name": "Grace Kim", "h_index": 63, "institution": "toronto"},
    {"id": "a08", "name": "Hiroshi Tanaka", "h_index": 54, "institution": "singapore"},
    {"id": "a09", "name": "Isabelle Martin", "h_index": 88, "institution": "cambridge"},
    {"id": "a10", "name": "James O'Brien", "h_index": 45, "institution": "berkeley"},
    {"id": "a11", "name": "Kira Volkov", "h_index": 71, "institution": "epfl"},
    {"id": "a12", "name": "Liam Murphy", "h_index": 49, "institution": "caltech"},
    {"id": "a13", "name": "Mei Zhang", "h_index": 82, "institution": "mit"},
    {"id": "a14", "name": "Noah Fischer", "h_index": 60, "institution": "columbia"},
    {"id": "a15", "name": "Olivia Brown", "h_index": 77, "institution": "princeton"},
    {"id": "a16", "name": "Priya Sharma", "h_index": 66, "institution": "ucl"},
    {"id": "a17", "name": "Quinn Taylor", "h_index": 53, "institution": "stanford"},
    {"id": "a18", "name": "Rachel Green", "h_index": 41, "institution": "cmu"},
    {"id": "a19", "name": "Samuel Park", "h_index": 58, "institution": "toronto"},
    {"id": "a20", "name": "Tara Nguyen", "h_index": 73, "institution": "oxford"},
    {"id": "a21", "name": "Umesh Gupta", "h_index": 47, "institution": "tsinghua"},
    {"id": "a22", "name": "Victoria Rossi", "h_index": 80, "institution": "eth"},
    {"id": "a23", "name": "Wang Jun", "h_index": 62, "institution": "singapore"},
    {"id": "a24", "name": "Xena Lopez", "h_index": 50, "institution": "berkeley"},
    {"id": "a25", "name": "Yuki Sato", "h_index": 69, "institution": "epfl"},
]

PAPERS = [
    {
        "id": "p001",
        "title": "Transformer Architectures for Multi-Modal Learning",
        "year": 2024,
        "abstract": "We propose a novel transformer architecture that efficiently fuses visual and textual modalities for improved multi-task learning.",
        "citations_count": 247,
        "authors": ["a01", "a13"],
        "topics": ["ml", "nlp", "cv"],
        "cites": ["p005", "p010"],
    },
    {
        "id": "p002",
        "title": "Graph Attention Networks for Drug Interaction Prediction",
        "year": 2024,
        "abstract": "A graph neural network approach to predicting molecular drug-drug interactions using attention mechanisms over molecular graphs.",
        "citations_count": 189,
        "authors": ["a04", "a20"],
        "topics": ["graphs", "drug", "ml"],
        "cites": ["p008", "p012"],
    },
    {
        "id": "p003",
        "title": "Federated Learning with Differential Privacy Guarantees",
        "year": 2023,
        "abstract": "We present a framework combining federated learning and differential privacy that achieves strong privacy guarantees without sacrificing model utility.",
        "citations_count": 312,
        "authors": ["a02", "a17"],
        "topics": ["ml", "privacy"],
        "cites": ["p006"],
    },
    {
        "id": "p004",
        "title": "Reinforcement Learning for Autonomous Navigation",
        "year": 2023,
        "abstract": "A deep RL framework for real-time autonomous vehicle navigation in complex urban environments with safety guarantees.",
        "citations_count": 156,
        "authors": ["a03", "a18"],
        "topics": ["rl", "robotics"],
        "cites": ["p009"],
    },
    {
        "id": "p005",
        "title": "Self-Supervised Visual Representation Learning at Scale",
        "year": 2022,
        "abstract": "A scalable self-supervised method for learning visual representations from unlabeled image datasets.",
        "citations_count": 523,
        "authors": ["a01", "a02", "a13"],
        "topics": ["ml", "cv"],
        "cites": [],
    },
    {
        "id": "p006",
        "title": "Secure Multi-Party Computation for Healthcare Data",
        "year": 2022,
        "abstract": "Enabling collaborative analytics on sensitive medical records using cryptographic protocols.",
        "citations_count": 198,
        "authors": ["a09", "a16"],
        "topics": ["privacy", "health"],
        "cites": [],
    },
    {
        "id": "p007",
        "title": "Climate Emulation with Neural Operators",
        "year": 2024,
        "abstract": "Learning surrogate models for climate simulations using neural operator architectures, achieving 1000x speedup.",
        "citations_count": 134,
        "authors": ["a05", "a22"],
        "topics": ["climate", "ml"],
        "cites": ["p011"],
    },
    {
        "id": "p008",
        "title": "Protein Structure Prediction via Geometric Deep Learning",
        "year": 2023,
        "abstract": "Advances in geometric deep learning for predicting protein tertiary structures from amino acid sequences.",
        "citations_count": 445,
        "authors": ["a04", "a09"],
        "topics": ["bio", "proteomics", "ml"],
        "cites": ["p012"],
    },
    {
        "id": "p009",
        "title": "Multi-Agent Reinforcement Learning for Traffic Optimization",
        "year": 2023,
        "abstract": "A cooperative MARL approach for city-scale traffic signal optimization reducing congestion by 30%.",
        "citations_count": 87,
        "authors": ["a06", "a21"],
        "topics": ["rl", "optimization"],
        "cites": [],
    },
    {
        "id": "p010",
        "title": "Efficient Fine-Tuning of Large Language Models",
        "year": 2024,
        "abstract": "Parameter-efficient methods for adapting large language models to domain-specific tasks with minimal overhead.",
        "citations_count": 678,
        "authors": ["a02", "a07"],
        "topics": ["nlp", "ml"],
        "cites": ["p005"],
    },
    {
        "id": "p011",
        "title": "Neural ODEs for Physics Simulation",
        "year": 2022,
        "abstract": "Combining neural ordinary differential equations with physical inductive biases for accurate dynamical system modeling.",
        "citations_count": 201,
        "authors": ["a10", "a24"],
        "topics": ["ml", "materials"],
        "cites": [],
    },
    {
        "id": "p012",
        "title": "Genomic Variant Calling with Deep Learning",
        "year": 2022,
        "abstract": "A deep learning pipeline for accurate identification of genetic variants from whole-genome sequencing data.",
        "citations_count": 367,
        "authors": ["a08", "a23"],
        "topics": ["genomics", "bio", "ml"],
        "cites": [],
    },
    {
        "id": "p013",
        "title": "Causal Inference in Observational Studies Using GNNs",
        "year": 2024,
        "abstract": "Applying graph neural networks to estimate causal effects from observational data with confounding.",
        "citations_count": 95,
        "authors": ["a14", "a15"],
        "topics": ["graphs", "ml", "optimization"],
        "cites": ["p002", "p003"],
    },
    {
        "id": "p014",
        "title": "Quantum Error Correction with Machine Learning",
        "year": 2024,
        "abstract": "ML-assisted decoding of quantum error correcting codes for scalable fault-tolerant quantum computing.",
        "citations_count": 78,
        "authors": ["a12"],
        "topics": ["quantum", "ml"],
        "cites": ["p011"],
    },
    {
        "id": "p015",
        "title": "Bias Auditing Frameworks for NLP Systems",
        "year": 2023,
        "abstract": "A systematic framework for detecting and mitigating social biases in large-scale NLP deployments.",
        "citations_count": 234,
        "authors": ["a15", "a16", "a20"],
        "topics": ["nlp", "ethics"],
        "cites": ["p003", "p006"],
    },
    {
        "id": "p016",
        "title": "Energy-Aware Neural Architecture Search",
        "year": 2023,
        "abstract": "Jointly optimizing model accuracy and energy consumption during neural architecture search.",
        "citations_count": 112,
        "authors": ["a11", "a25"],
        "topics": ["ml", "energy", "optimization"],
        "cites": ["p010"],
    },
    {
        "id": "p017",
        "title": "Cross-Lingual Transfer Learning for Low-Resource Languages",
        "year": 2024,
        "abstract": "Methods for transferring NLP capabilities from high-resource to low-resource languages using multilingual models.",
        "citations_count": 143,
        "authors": ["a06", "a08", "a21"],
        "topics": ["nlp", "ml"],
        "cites": ["p010", "p015"],
    },
    {
        "id": "p018",
        "title": "Neural Architecture Search for Medical Imaging",
        "year": 2023,
        "abstract": "Automated design of efficient neural networks for medical image segmentation tasks.",
        "citations_count": 189,
        "authors": ["a19", "a07"],
        "topics": ["cv", "health", "ml"],
        "cites": ["p005", "p016"],
    },
    {
        "id": "p019",
        "title": "Network Epidemiology: Modeling Disease Spread on Contact Graphs",
        "year": 2024,
        "abstract": "Using graph-based models to simulate and predict disease transmission patterns in populations.",
        "citations_count": 267,
        "authors": ["a14", "a16"],
        "topics": ["networks", "health", "graphs"],
        "cites": ["p002", "p013"],
    },
    {
        "id": "p020",
        "title": "Adversarial Robustness in Vision-Language Models",
        "year": 2024,
        "abstract": "Analyzing and improving the adversarial robustness of combined vision-language pretrained models.",
        "citations_count": 156,
        "authors": ["a01", "a11"],
        "topics": ["cv", "nlp", "ml"],
        "cites": ["p001", "p010"],
    },
    {
        "id": "p021",
        "title": "Bio-Inspired Materials Discovery with GNNs",
        "year": 2023,
        "abstract": "Discovering novel bio-inspired materials using graph neural networks over molecular structures.",
        "citations_count": 98,
        "authors": ["a05", "a10"],
        "topics": ["materials", "bio", "graphs"],
        "cites": ["p008", "p011"],
    },
    {
        "id": "p022",
        "title": "Continual Learning Without Forgetting",
        "year": 2023,
        "abstract": "Novel methods for continual learning that prevent catastrophic forgetting in neural networks.",
        "citations_count": 276,
        "authors": ["a03", "a17", "a24"],
        "topics": ["ml", "rl"],
        "cites": ["p005", "p010"],
    },
    {
        "id": "p023",
        "title": "Urban Mobility Prediction with Spatio-Temporal Graphs",
        "year": 2024,
        "abstract": "Predicting urban mobility patterns using spatio-temporal graph neural networks.",
        "citations_count": 145,
        "authors": ["a06", "a25"],
        "topics": ["graphs", "networks", "optimization"],
        "cites": ["p009", "p019"],
    },
    {
        "id": "p024",
        "title": "Privacy-Preserving Genomic Data Analysis",
        "year": 2024,
        "abstract": "Secure computation methods for analyzing genomic data while preserving individual privacy.",
        "citations_count": 89,
        "authors": ["a12", "a22"],
        "topics": ["privacy", "genomics"],
        "cites": ["p006", "p012"],
    },
    {
        "id": "p025",
        "title": "Multi-Hop Reasoning in Knowledge Graphs",
        "year": 2023,
        "abstract": "Advanced methods for multi-hop reasoning and link prediction in large-scale knowledge graphs.",
        "citations_count": 203,
        "authors": ["a14", "a20"],
        "topics": ["graphs", "nlp", "ml"],
        "cites": ["p002", "p013", "p019"],
    },
]

COLLABORATIONS = [
    ("a01", "a02"), ("a01", "a13"), ("a02", "a07"), ("a02", "a17"),
    ("a03", "a18"), ("a03", "a24"), ("a04", "a09"), ("a04", "a20"),
    ("a05", "a22"), ("a06", "a21"), ("a06", "a25"), ("a07", "a19"),
    ("a08", "a23"), ("a09", "a16"), ("a10", "a24"), ("a11", "a25"),
    ("a14", "a15"), ("a14", "a16"), ("a15", "a20"), ("a16", "a20"),
    ("a11", "a01"), ("a07", "a19"), ("a19", "a08"),
]


def seed_database(driver):
    with driver.session() as session:
        print("Clearing existing data...")
        session.run("MATCH (n) DETACH DELETE n")

        print("Creating institutions...")
        for inst in INSTITUTIONS:
            session.run(
                "CREATE (i:Institution {id: $id, name: $name, country: $country, ranking: $ranking})",
                inst,
            )

        print("Creating topics...")
        for topic in TOPICS:
            session.run(
                "CREATE (t:Topic {id: $id, name: $name, category: $category})",
                topic,
            )

        print("Creating authors...")
        for author in AUTHORS:
            session.run(
                "CREATE (a:Author {id: $id, name: $name, h_index: $h_index})",
                author,
            )
            session.run(
                "MATCH (a:Author {id: $aid}), (i:Institution {id: $iid}) CREATE (a)-[:AFFILIATED_WITH]->(i)",
                {"aid": author["id"], "iid": author["institution"]},
            )

        print("Creating papers and relationships...")
        for paper in PAPERS:
            session.run(
                "CREATE (p:Paper {id: $id, title: $title, year: $year, abstract: $abstract, citations_count: $citations_count})",
                paper,
            )
            for author_id in paper["authors"]:
                session.run(
                    "MATCH (p:Paper {id: $pid}), (a:Author {id: $aid}) CREATE (p)-[:AUTHORED_BY]->(a)",
                    {"pid": paper["id"], "aid": author_id},
                )
            for topic_id in paper["topics"]:
                session.run(
                    "MATCH (p:Paper {id: $pid}), (t:Topic {id: $tid}) CREATE (p)-[:TAGGED_WITH]->(t)",
                    {"pid": paper["id"], "tid": topic_id},
                )
            for cited_id in paper["cites"]:
                session.run(
                    "MATCH (p:Paper {id: $pid}), (c:Paper {id: $cid}) CREATE (p)-[:CITES]->(c)",
                    {"pid": paper["id"], "cid": cited_id},
                )

        print("Creating collaboration relationships...")
        for a1, a2 in COLLABORATIONS:
            session.run(
                "MATCH (a:Author {id: $a1}), (b:Author {id: $a2}) MERGE (a)-[:COLLABORATES_WITH]-(b)",
                {"a1": a1, "a2": a2},
            )

        print("Creating indexes...")
        session.run("CREATE FULLTEXT INDEX search_index IF NOT EXISTS FOR (n:Paper|Author|Institution|Topic) ON EACH [n.title, n.name]")
        session.run("CREATE INDEX paper_id IF NOT EXISTS FOR (p:Paper) ON (p.id)")
        session.run("CREATE INDEX author_id IF NOT EXISTS FOR (a:Author) ON (a.id)")
        session.run("CREATE INDEX institution_id IF NOT EXISTS FOR (i:Institution) ON (i.id)")
        session.run("CREATE INDEX topic_id IF NOT EXISTS FOR (t:Topic) ON (t.id)")

        print("Seed complete!")
        counts = session.run(
            "MATCH (n) RETURN labels(n)[0] AS label, COUNT(n) AS count"
        )
        for record in counts:
            print(f"  {record['label']}: {record['count']}")

        rel_counts = session.run(
            "MATCH ()-[r]->() RETURN type(r) AS type, COUNT(r) AS count"
        )
        for record in rel_counts:
            print(f"  {record['type']}: {record['count']}")


def main():
    parser = argparse.ArgumentParser(description="Seed ResearchGraph database")
    parser.add_argument("--uri", default=os.getenv("COGNODB_URI", "bolt+s://localhost:7687"))
    parser.add_argument("--user", default=os.getenv("COGNODB_USER", "cognodb"))
    parser.add_argument("--password", default=os.getenv("COGNODB_PASSWORD", ""))
    args = parser.parse_args()

    print(f"Connecting to {args.uri}...")
    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    try:
        driver.verify_connectivity()
        seed_database(driver)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
