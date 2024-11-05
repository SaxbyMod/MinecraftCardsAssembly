import os
import csv
from PIL import ImageDraw, Image, ImageFont

# Load data from CSV into a dictionary
def load_data_from_csv(csv_file):
    if not os.path.exists(csv_file):
        print(f"CSV file '{csv_file}' not found!")
        return {}
    
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {row['Name']: row for row in reader}
        if not data:
            print(f"No data found in CSV file '{csv_file}'!")
        return data

# Wrap text when it exceeds a given width
def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, current_line = [], []
    current_width = 0
    space_width = draw.textbbox((0, 0), " ", font=font)[2]

    for word in words:
        word_width = draw.textbbox((0, 0), word, font=font)[2]
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + (space_width if current_line else 0)
        else:
            lines.append(' '.join(current_line))
            current_line, current_width = [word], word_width

    if current_line:
        lines.append(' '.join(current_line))

    return lines

# Draw card data onto card image
def draw_card_data(card_data, card_image, name_pos, desc_pos, cost_pos, name_font, desc_font, image_pos):
    draw = ImageDraw.Draw(card_image)

    # Draw name
    draw.text(name_pos, card_data['Name'], fill="white", font=name_font, anchor="mm")

    # Wrap and draw description
    vertical_pos = desc_pos[1]
    for block in card_data['Description'].split('[NEW]'):
        for line in wrap_text(block, desc_font, 654, draw):
            draw.text((desc_pos[0], vertical_pos), line, fill="white", font=desc_font, anchor="ma")
            vertical_pos += 25

    # Draw cost
    draw.text(cost_pos, card_data['Cost'], fill="white", font=desc_font, anchor="ma")

    # Paste artwork
    artwork_path = f"Artwork/{card_data['Name']}.png"
    if os.path.exists(artwork_path):
        image = Image.open(artwork_path).convert("RGBA")
        card_image.paste(image, image_pos, mask=image)
    else:
        print(f"Artwork for {card_data['Name']} not found at {artwork_path}.")

    return card_image

# Load font once to avoid redundant loading
def load_fonts(font_path, name_size, desc_size):
    if not os.path.exists(font_path):
        print(f"Font file '{font_path}' not found!")
        return None, None
    return ImageFont.truetype(font_path, name_size), ImageFont.truetype(font_path, desc_size)

# Example values
NamePos = (639, 135)
DescPos = (639, 980)
CostPos = (639, 1160)
ImagePos = (308, 245)
FontPath = "Font.ttf"  # Make sure the path to the font file is correct
NameSize = 50
DescriptionSize = 30

# Load data from CSV
csv_file = 'cards.csv'
card_data = load_data_from_csv(csv_file)
if not card_data:
    print("No card data found, exiting.")
    exit()

# Load fonts once
name_font, description_font = load_fonts(FontPath, NameSize, DescriptionSize)
if not name_font or not description_font:
    print("Fonts could not be loaded, exiting.")
    exit()

# Load card image
card_image_path = "Cardback.png"
if not os.path.exists(card_image_path):
    print(f"Card image '{card_image_path}' not found, exiting.")
    exit()

card_image = Image.open(card_image_path)

# Ensure output directory exists
os.makedirs("Output", exist_ok=True)

# Process each card and save it
for card_name, data in card_data.items():
    try:
        card = draw_card_data(data, card_image.copy(), NamePos, DescPos, CostPos, name_font, description_font, ImagePos)
        output_path = f"Output/{card_name}.png"
        card.save(output_path, format="PNG")
        print(f"{card_name} completed successfully.")
    except Exception as e:
        print(f"Error processing {card_name}: {e}")
