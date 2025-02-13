import textwrap
from fpdf import FPDF
from datetime import datetime

def generate_certificate(name, type_, percentage):
    pdf = FPDF(orientation='landscape', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    pdf.image("image_template/template_ui.jpg", x=0, y=0, w=297, h=210)

    font_large = 45
    font_medium = 25
    font_small = 15

    if percentage >= 90:
        medal_image_path = 'medals/gold.png'
    elif 80 <= percentage < 90:
        medal_image_path = 'medals/silver.png'
    elif 70 <= percentage < 80:
        medal_image_path = 'medals/bronze.png'
    else:
        medal_image_path = None

    if medal_image_path:
        pdf.image(medal_image_path, x=200, y=50, w=40, h=40)

    y_coordinate = 35

    pdf.set_xy(20, y_coordinate)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", size=font_large)
    pdf.cell(w=0, h=10, txt='Certificate of Completion', align='L')

    y_coordinate += 30
    pdf.set_xy(20, y_coordinate)
    pdf.set_font("Arial", size=font_medium)
    pdf.cell(w=0, h=10, txt="This certificate is proudly presented to", align='L')

    y_coordinate += 20
    pdf.set_xy(20, y_coordinate)
    pdf.set_font("Arial", size=font_large)
    pdf.cell(w=0, h=10, txt=name, align='L')

    value = f'for demonstrating knowledge and skill by successfully completing the {type_} Quiz with a score of {percentage}%.'
    wrapper = textwrap.TextWrapper(width=55)
    word_list = wrapper.wrap(text=value)

    y_coordinate += 20
    for element in word_list:
        pdf.set_xy(20, y_coordinate)
        pdf.set_font("Arial", size=font_medium)
        pdf.cell(w=0, h=10, txt=element, align='L')
        y_coordinate += 10

    y_coordinate += 20
    pdf.set_xy(20, y_coordinate)
    pdf.set_font("Arial", size=font_small)
    pdf.cell(w=0, h=10, txt="______________________________________________", align='L')

    y_coordinate += 10
    now = datetime.now()
    date_time = now.strftime('%d %B %Y, %H:%M:%S')
    pdf.set_xy(20, y_coordinate)
    pdf.cell(w=0, h=10, txt=f"Awarded on: {date_time}", align='L')

    y_coordinate += 10
    pdf.set_xy(20, y_coordinate)
    pdf.set_font("Arial", size=font_small)
    pdf.cell(w=0, h=10, txt="Certified by: Quizify", align='L')

    y_coordinate += 10
    pdf.set_xy(20, y_coordinate)
    pdf.cell(w=0, h=10, txt='"Keep learning, keep growing."', align='L')

    pdf.output('output/sample-output-poc1.pdf')

if __name__ == "__main__":
    generate_certificate(
        name="test",
        type_="python",
        percentage=70
    )
