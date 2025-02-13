import textwrap
from uuid import uuid4
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime

def generate_certificate(name, type_, percentage):
    img = Image.open("image_template/template_ui.jpg")

    draw = ImageDraw.Draw(img)

    font_large = ImageFont.truetype("/mnt/c/Windows/Fonts/arial.ttf", 50)
    font_midium = ImageFont.truetype("/mnt/c/Windows/Fonts/arial.ttf", 30)
    font_small = ImageFont.truetype("/mnt/c/Windows/Fonts/arial.ttf", 20)

    if percentage >= 90:
        medal_image_path = Image.open('medals/gold.png').resize((120, 120), Image.Resampling.LANCZOS)
        img.paste(im=medal_image_path, box=(600, 270), mask=medal_image_path)
    elif 80 <= percentage < 90:
        medal_image_path = Image.open('medals/silver.png').resize((120, 120), Image.Resampling.LANCZOS)
        img.paste(im=medal_image_path, box=(600, 270), mask=medal_image_path)
    elif 70 <= percentage < 80:
        medal_image_path = Image.open('medals/bronze.png').resize((120, 120), Image.Resampling.LANCZOS)
        img.paste(im=medal_image_path, box=(600, 270), mask=medal_image_path)
    else:
        medal_image_path = None

    y_coordinate = 70
    draw.text(
        xy=(80, y_coordinate),
        text="Certificate of Completion",
        fill='white',
        font=font_large,
        stroke_width=0.5
    )

    y_coordinate += 160
    draw.text(
        xy=(80, y_coordinate),
        text="This certificate is proudly presented to",
        fill='white',
        font=font_midium,
    )

    y_coordinate += 80
    draw.text(
        xy=(80, y_coordinate),
        text=name,
        fill='white',
        font=font_large,
        stroke_width=0.5
    )

    value = f'for demonstrating knowledge and skill by successfully completing the {type_} Quiz with a score of {percentage}%'
    wrapper = textwrap.TextWrapper(width=50)
    word_list = wrapper.wrap(text=value)
    y_coordinate += 100
    for element in word_list:
        draw.text(
            xy=(80, y_coordinate),
            text=element,
            font=font_midium,
            fill='white'
        )
        y_coordinate += 40

    y_coordinate+=80
    draw.line(xy=(80, y_coordinate, 700, y_coordinate), fill='white', width=2)

    y_coordinate+=20
    now = datetime.now()
    date_time = now.strftime('%d %B %Y, %H:%M:%S')
    draw.text(
        xy=(80, y_coordinate),
        text=f"Awarded on: {date_time}",
        fill='white',
        font=font_small,
    )

    y_coordinate+=40
    draw.text(
        xy=(80, y_coordinate),
        now = datetime.now(),
        date_time = now.strftime('%d %B %Y, %H:%M:%S'),
        text="Certified by: Quizify",
        fill='white',
        font=font_small,
    )

    y_coordinate+=40
    draw.text(
        xy=(80, y_coordinate),
        now = datetime.now(),
        date_time = now.strftime('%d %B %Y, %H:%M:%S'),
        text='"Keep learning, keep growing."',
        fill='white',
        font=font_small,
    )

    img.save(f'output/sample-output-{uuid4()}.jpg')

if __name__ == "__main__":
    generate_certificate(
        name="test",
        type_="python",
        percentage=70
    )
