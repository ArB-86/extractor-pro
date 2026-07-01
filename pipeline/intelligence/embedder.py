import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

class EmbeddingPipeline:
    def __init__(self):
        print("Loading Model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = []
        self.metadata = []

    def process(self, json_dir: Path):
        files = list(json_dir.glob("*.json"))
        if not files:
            print(f"Error: No JSON files found in {json_dir}")
            return
            
        for json_file in files:
            print(f"Embedding: {json_file.name}")
            with open(json_file, 'r') as f:
                try:
                    questions = json.load(f)
                    for q in questions:
                        # Fallback to 'question' if 'question_text' is missing
                        text = q.get('question_text', q.get('question', ''))
                        if not text: continue
                        
                        vec = self.model.encode(text)
                        self.embeddings.append(vec)
                        self.metadata.append(q)
                except json.JSONDecodeError:
                    continue
        
        self.embeddings = np.array(self.embeddings)
        print(f"Dataset indexed. Matrix shape: {self.embeddings.shape}")

if __name__ == "__main__":
    EmbeddingPipeline().process(Path("output/master_dataset"))
