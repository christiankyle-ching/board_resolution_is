from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from fpdf import FPDF

# Default values
MAX_RESOLUTION_PX = 2048
QUALITY = 85
FORMAT = "JPEG"


def compress_image(img, filename="image", image_format=FORMAT, quality=QUALITY, max_resolution=MAX_RESOLUTION_PX):
    filename = f"{filename}.{image_format}"

    # Containers
    compressed_img = Image.open(img)
    compressed_io = BytesIO()

    # Resize using thumbnail
    compressed_img.thumbnail(
        (max_resolution, max_resolution), resample=Image.ANTIALIAS)

    # If JPEG, we can't handle Alpha (RGBA)
    if image_format in ['JPEG']:
        compressed_img = compressed_img.convert('RGB')

    compressed_img.save(compressed_io, format=image_format, quality=quality)

    return InMemoryUploadedFile(compressed_io, None, filename,
                                f'image/{image_format.lower()}', compressed_io.tell(), None)


def get_highest_length_in_list(arr):
    max_length = 0

    for s in arr:
        if len(s) > max_length:
            max_length = len(s)

    return max_length


class PDFWithImageAndLabel(FPDF):
    def add_image(self, path):
        img = Image.open(path)
        width, height = img.size

        # Set background of image to white
        img_with_bg = Image.new("RGBA", img.size, "WHITE")
        img_with_bg.paste(img, (0, 0), img)
        img_with_bg = img_with_bg.convert('RGB')

        # Assuming ppi is 96
        # 96 pixels in 1 inch
        # 1 px = 0.0104166...
        inch_per_px = 0.0104167
        width_in, height_in = width * inch_per_px, height * inch_per_px

        # Scale converted size down to fit width
        scale_factor = self.epw / width_in
        width_in, height_in = width_in * scale_factor, height_in * scale_factor

        # If converted height is still taller than eph, then fit height, else fit width
        if height_in > self.eph:
            self.image(img_with_bg, h=self.eph)
        else:
            self.image(img_with_bg, w=self.epw)

    def add_lines_of_text(self, lines, font_size=11, line_height=1.5, font_family="helvetica", font_style="B", text_color=(255,), pos=(1, -2), bg_color=(0,), padding=6):
        self.set_font(font_family, font_style, font_size)

        self.set_text_color(*text_color)
        self.set_fill_color(*bg_color)

        self.set_xy(*pos)

        height = self.font_size * line_height
        width = self.get_string_width(
            "M"*(get_highest_length_in_list(lines) + padding))

        # For padding only
        self.cell(width, height / 2, "", 0, ln=2, fill=True)

        # Write each line
        for line in lines:
            self.cell(
                width, height, f"{' '*(padding//2)}{line}{' '*(padding//2)}", 0, ln=2, fill=True)

        # For padding only
        self.cell(width, height / 2, "", 0, ln=2, fill=True)
