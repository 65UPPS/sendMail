DB_HOST = 'ec2-54-74-14-109.eu-west-1.compute.amazonaws.com'
DB_NAME = "de0fglpocdb2up"
DB_USER = "jgpjdpqktnjurl"
DB_PASS = "479cbe7cb2935b6151a1145e1bce96e7575bcecfd5d581ea214210358d1b0172"

from fpdf import FPDF
from datetime import datetime, timedelta
import psycopg2.extras
import pandas as pd
from create_table_fpdf2 import PDF

with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT fire_brigate, "
        "SUM(with_pump) AS with_pump,"
        "SUM(without_pump) AS without_pump,"
        "SUM(speedo_in - speedo_out) AS mileage,S"
        "UM(actual_expense) AS actual_expense "
        "FROM dataset "
        "WHERE date_out = ('today'::date- interval '1 day')"
        "GROUP BY fire_brigate;")
    data_table = cur.fetchall()

    cur.execute("SET timezone = 'Asia/Sakhalin';")

data_table_base = pd.DataFrame(data_table, columns=['отряд', 'Работа с насосом', 'Работа без насоса', 'Пробег',
                                                    'Фактический расход'])
data_table_base = data_table_base.astype(
    {"Работа с насосом": str, "Работа без насоса": str, "Пробег": str, "Фактический расход": str})

now = (datetime.now().date() - timedelta(days=1)).strftime("%d.%m.%Y")

title = f'ОПЕРАТИВНАЯ ОБСТАНОВКА за {now}'

data = [data_table_base.columns.values.tolist()] + data_table_base.values.tolist()

#
# class PDF(FPDF):
#     def header(self):
#         # logo
#         self.image('logo.png', 10, 8, 25)
#         # font
#         self.set_font('Roboto', '', 16)
#         # title
#         self.cell(0, 20, f'{title} на {now}', border=False, ln=1, align='C')
#         # self break
#         self.ln(20)
#
#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Roboto', '', 10)
#         self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')


# create pdf object
# Layout ('P', 'L')
# Unit ('mm', 'cm', 'in')
# Format ('A3', 'A4' (default), 'A5', 'letter', 'legal', (100,150))

pdf = PDF('P', 'mm', 'Letter')

pdf.add_font('Bernard MT', '', r'C:\Windows\Fonts\BERNHC.TTF', uni=True)

pdf.add_font('Roboto', '', r'assets\font\Roboto-Bold.ttf', uni=True)

# get total page numbers
pdf.alias_nb_pages()

# Set auto page break
pdf.set_auto_page_break(auto=True, margin=15)

# Add a page
pdf.add_page()

# fonts ('times', 'courier', 'helvetica', 'symbol', 'zpfdingbats')
# "B" (bold), 'U' (underline), 'I' (italics)
pdf.set_font('Roboto', '', 16)

# Add text
# w = width
# h = height
# txt = my text
# ln (0 False; 1 True - move cursor down to next line)

pdf.cell(40, 10, f'1. Оперативное реагирование подразделений', ln=1)
pdf.cell(40, 20, f'1.1 Показатели работы пожарной техники', ln=1)
pdf.create_table(table_data=data, cell_width=[30, 22, 22, 22, 25], x_start='C', align_data='C')

line_height = pdf.font_size * 1.7
col_width = pdf.epw / 6  # distribute content evenly
for row in data:
    for datum in row:
        pdf.multi_cell(col_width, line_height, datum, align ='C', border=1, ln=3, max_line_height=pdf.font_size)
    pdf.ln(line_height)



pdf.output('pdf_1.pdf')
