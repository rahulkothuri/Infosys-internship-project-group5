import pandas as pd
from fpdf import FPDF

# Load the CSV file
data = pd.read_csv('/home/rahul/Downloads/gpt-4.csv')

# Combine data and conversation fields (if necessary)
data['combined'] = data['data'] + "\n\n" + data['conversation']

# Create a PDF instance
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

# Loop through the rows and add to PDF
for index, row in data.iterrows():
    pdf.add_page()
    content = f"Case {index + 1}:\n\n{row['combined']}"
    pdf.multi_cell(0, 10, content)

# Save the PDF
pdf.output("dataset.pdf")

