import os
import csv
from PIL import ImageDraw, Image, ImageFont

# Load data from CSV into a dictionary
def load_data_from_csv(csv_file):
    data = {}
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data[row[0]] = {'Name': row[0], 'Cost': row[1], 'Description': row[2]}
    return data

# Draw card data onto card image
def draw_card_data(card_data, card_image, name_pos, desc_pos, name_font, desc_font, image_pos):
    draw = ImageDraw.Draw(card_image)
    draw.text(name_pos, card_data['Name'], fill="white", font=name_font, anchor="mm")
    description_lines = card_data['Description'].split('[NEW]')
    vertical_pos = desc_pos[1]
    for line in description_lines:
        draw.text((desc_pos[0], vertical_pos), line, fill="white", font=desc_font, anchor="ma")
        vertical_pos += 25
    draw.text(CostPos, card_data["Cost"], fill="white", font=desc_font, anchor="ma")
    image = Image.open("Artwork/" + card_data["Name"] + ".png").convert("RGBA")
    card_image.paste(image, image_pos, mask=image)
    
    return card_image


# Load font
def load_font(font_path, font_size):
    return ImageFont.truetype(font_path, font_size)

# Example values
NamePos = (639, 135)
DescPos = (639, 980)
CostPos = (639, 1160)
ImagePos = (308, 245)
FontPath = "Font.ttf"  # Replace with the path to your font file
NameSize = 50
DescriptionSize = 30

# Load card data from CSV
csv_file = 'cards.csv'
card_data = load_data_from_csv(csv_file)

# Load font
name_font = load_font(FontPath, NameSize)
description_font = load_font(FontPath, DescriptionSize)

# Load card image
card_image_path = "Cardback.png"
card_image = Image.open(card_image_path)

# Draw card data onto card image and save as individual images
for card_name, data in card_data.items():
    card = draw_card_data(data, card_image.copy(), NamePos, DescPos, name_font, description_font, ImagePos)
    card.save(f"Output/{card_name}.png", format="PNG")