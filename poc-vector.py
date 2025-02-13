import svgwrite
from datetime import datetime
import textwrap
from uuid import uuid4

def generate_certificate(name, type_, percentage):
    dwg = svgwrite.Drawing(f'output/sample-output-{uuid4()}.svg', profile='full', size=("800px", "600px"))

    dwg.add(dwg.rect(insert=(0, 0), size=("800px", "600px"), fill='#1E1E1E'))

    font_family = 'Arial, sans-serif'

    dwg.add(dwg.rect(insert=(40, 40), size=("720px", "520px"), stroke='gold', stroke_width=5, fill='none'))
    dwg.add(dwg.rect(insert=(50, 50), size=("700px", "500px"), stroke='white', stroke_width=2, fill='none'))

    if percentage >= 90:
        medal_image_path = 'medals/gold.png'
    elif 80 <= percentage < 90:
        medal_image_path = 'medals/silver.png'
    elif 70 <= percentage < 80:
        medal_image_path = 'medals/bronze.png'
    else:
        medal_image_path = None

    if medal_image_path:
        dwg.add(dwg.image(medal_image_path, insert=(650, 100), size=("120px", "120px")))

    y_coordinate = 100
    dwg.add(dwg.text("Certificate of Completion", insert=(100, y_coordinate), fill='gold', font_size='50px', font_family=font_family, font_weight='bold'))

    y_coordinate += 150
    dwg.add(dwg.text("This certificate is proudly presented to", insert=(100, y_coordinate), fill='white', font_size='30px', font_family=font_family, font_style='italic'))

    y_coordinate += 80
    dwg.add(dwg.text(name, insert=(100, y_coordinate), fill='gold', font_size='50px', font_family=font_family, font_weight='bold'))

    value = f'for demonstrating knowledge and skill by successfully completing the {type_} Quiz with a score of {percentage}%'
    wrapper = textwrap.TextWrapper(width=50)
    word_list = wrapper.wrap(text=value)
    y_coordinate += 100
    for element in word_list:
        dwg.add(dwg.text(element, insert=(100, y_coordinate), fill='white', font_size='30px', font_family=font_family))
        y_coordinate += 40

    y_coordinate += 80

    line_y = y_coordinate
    dwg.add(dwg.line(start=(100, line_y), end=(700, line_y), stroke='white', stroke_width=2))

    y_coordinate += 20
    now = datetime.now()
    date_time = now.strftime('%d %B %Y, %H:%M:%S')
    dwg.add(dwg.text(f"Awarded on: {date_time}", insert=(100, y_coordinate), fill='white', font_size='20px', font_family=font_family))

    y_coordinate += 40
    dwg.add(dwg.text("Certified by: Quizify", insert=(100, y_coordinate), fill='white', font_size='20px', font_family=font_family, font_weight='bold'))

    y_coordinate += 40
    dwg.add(dwg.text('"Keep learning, keep growing."', insert=(100, y_coordinate), fill='white', font_size='20px', font_family=font_family, font_style='italic'))

    dwg.save()

if __name__ == "__main__":
    generate_certificate(
        name="test",
        type_="python",
        percentage=70
    )
