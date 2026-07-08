from pipeline.vision.figure_extractor import FigureExtractor

pdf = "/home/jiitcah.05/nlp_research_module/datasets/exemplar_raw/10th_maths/jeep208.pdf"

figs = FigureExtractor().extract(
    pdf,
    "output/figures"
)

print(len(figs))

for f in figs[:10]:
    print(f)