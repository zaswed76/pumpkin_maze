

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)
elements = []
data= [ ["x  ", "=", "30"],
["y  ", "=", "50"],
["x-y", "=", "-20" ] ]
t=Table(data)
elements.append(t)
# write the document to disk
doc.build(elements)