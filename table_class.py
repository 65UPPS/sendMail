from create_table_fpdf2 import PDF
from app import data_table_base

data = [data_table_base.columns.values.tolist()] + data_table_base.values.tolist()

pdf = PDF()

pdf.add_font('Roboto', '', r'assets\font\Roboto-Bold.ttf', uni=True)

pdf.add_page()
pdf.set_font('Roboto', '', 16)

# pdf.ln()

# pdf.create_table(table_data=data, title='1. Показатели оперативного реагирования', cell_width=[30, 22, 22, 22, 25], x_start=25, align_data='C')


pdf.create_table(table_data=data, title="I'm in the middle", cell_width=[30, 22, 22, 22, 25], x_start='C',
                 align_data='C')
# pdf.ln()


pdf.output('table_class.pdf')
