from fpdf import FPDF

text = """
Artificial Intelligence is a branch of computer science that focuses on creating intelligent machines.

Machine Learning allows systems to learn from data without explicit programming.

Deep Learning uses neural networks with multiple layers.

RAG combines retrieval and generation for better AI responses.

Python is widely used in AI and data science.

Streamlit helps build quick ML web apps.
"""

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for line in text.split("\n"):
    pdf.cell(200, 10, txt=line, ln=True)

pdf.output("sample.pdf")

print("PDF created successfully!")