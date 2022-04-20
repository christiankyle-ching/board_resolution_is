from django.utils import timezone
from django.core.management import call_command
from django.core.files.uploadedfile import InMemoryUploadedFile

from io import BytesIO
from PIL import Image

from fpdf import FPDF

import os
import shutil
import zipfile

# Default values
QUALITY = 85


def compress_image(img, custom_filename=None, max_px=None, force_jpeg=False, quality=QUALITY):
    orig_filename = os.path.splitext(img.name)
    fname = custom_filename or orig_filename

    # Containers
    img = Image.open(img)

    # Values
    image_format = "JPEG" if force_jpeg else img.format
    filename = f"{fname}.{image_format}"

    img_io = BytesIO()

    converted_img = Image.new(mode="RGBA", size=img.size, color="WHITE")
    converted_img.paste(img, (0, 0), img.convert("RGBA"))
    if max_px is not None:
        converted_img.thumbnail(
            (max_px, max_px), Image.ANTIALIAS)
    converted_img.convert("RGB").save(
        img_io, format=image_format, quality=quality)

    return InMemoryUploadedFile(img_io, None, filename,
                                f'image/{image_format.lower()}', img_io.tell(), None)


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
            self.image(img, h=self.eph)
        else:
            self.image(img, w=self.epw)

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


DUMPS_FOLDER = 'temp_dumps'
DUMPS_IMPORTS_FOLDER = 'temp_imports'


def app_db_export(app_name, media_path=None, format='json'):
    dump_id = f'dump-{timezone.now().timestamp()}'
    dump_folder = f'{DUMPS_FOLDER}/{dump_id}'

    os.makedirs(dump_folder, exist_ok=True)

    dump_zip_filepath = f'{dump_folder}/{dump_id}.zip'
    json_filename = 'db.json'
    json_filepath = f'{dump_folder}/{json_filename}'

    # Generate DB Dump from PSQL
    output = open(json_filepath, 'w')
    call_command('dumpdata', app_name,
                 format='json', indent=3, stdout=output)
    output.close()

    with zipfile.ZipFile(dump_zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipObj:
        # Write JSON
        zipObj.write(json_filepath, json_filename)

        # Write media/resolutions
        if media_path is not None:
            for folder, _, files in os.walk(media_path):
                for f in files:
                    filepath = os.path.join(folder, f)
                    zipObj.write(filepath, filepath)

    return dump_zip_filepath


def app_db_import(uploaded_zip, media_path=None):
    try:
        dump_id = f'import-{timezone.now().timestamp()}'
        dump_folder = f'{DUMPS_IMPORTS_FOLDER}/{dump_id}'
        json_filepath = f'{dump_folder}/db.json'

        os.makedirs(dump_folder, exist_ok=True)

        # Get uploaded file and write to system
        dump_zip_filepath = f'{dump_folder}/{uploaded_zip.name}'
        with open(dump_zip_filepath, 'wb+') as dest:
            for chunk in uploaded_zip.chunks():
                dest.write(chunk)

        # Extract ZIP
        with zipfile.ZipFile(dump_zip_filepath, 'r') as zipObj:
            zipObj.extractall(dump_folder)

        # WARN: Delete first to avoid unique constraints
        # Resolution.objects.delete()

        # Import rows to database first
        call_command('loaddata', json_filepath)

        # Then copy images if loaddata succeeded
        if media_path is not None:
            shutil.rmtree(media_path, ignore_errors=True)
            shutil.move(f'{dump_folder}/{media_path}',
                        media_path)

        # Clean by removing the folder
        shutil.rmtree(dump_folder)
    except Exception as e:
        raise e
