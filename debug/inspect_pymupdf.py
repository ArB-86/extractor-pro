import fitz

pdf = "/home/jiitcah.05/nlp_research_module/datasets/raw_docs/kemh1dd/kemh106.pdf"

doc = fitz.open(pdf)

page = doc[4]      # Exercise 6.1 page

d = page.get_text("dict")

for i, block in enumerate(d["blocks"]):
    print("=" * 80)
    print("BLOCK", i)

    for line in block.get("lines", []):

        print()

        for span in line.get("spans", []):

            print(
                span["text"],
                "|",
                span["font"],
                "|",
                span["size"],
                "|",
                span["flags"],
            )
