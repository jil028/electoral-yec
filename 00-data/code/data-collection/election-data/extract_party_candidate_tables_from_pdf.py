# import libraries
import tabula
from tabula import read_pdf
from tabula import convert_into

# load the files
table_file = 'enter the path to the pdf file'
output_csv = 'enter the name of the output file'
# save as csv 
df = convert_into(table_file, output_csv, output_format = 'csv', lattice = True, stream = False, pages = 'all')
