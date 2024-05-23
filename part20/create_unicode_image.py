from PIL import Image, ImageDraw, ImageFont

# Unicode character U+30EDE
unicode_char = "𰻞"

# Create an image with white background
image = Image.new("RGB", (200, 200), "white")
draw = ImageDraw.Draw(image)

# Load a font
font_path = "path_to_your_font/NotoSansCJKjp-Regular.otf"
font = ImageFont.truetype(font_path, 150)

# Draw the Unicode character onto the image
draw.text((10, 10), unicode_char, font=font, fill="black")

# Save the image
image.save("unicode_char.png")
