import os
import shutil

def organize_fonts(source_directory):
    # Create the required folders if they don't exist
    normal_folder = os.path.join(source_directory, 'normal')
    bold_folder = os.path.join(source_directory, 'bold')
    italic_folder = os.path.join(source_directory, 'italic')
    italic_bold_folder = os.path.join(source_directory, 'italic_bold')

    if not os.path.exists(normal_folder):
        os.mkdir(normal_folder)
    if not os.path.exists(bold_folder):
        os.mkdir(bold_folder)
    if not os.path.exists(italic_folder):
        os.mkdir(italic_folder)
    if not os.path.exists(italic_bold_folder):
        os.mkdir(italic_bold_folder)

    # List all font files in the source directory
    for font_file in os.listdir(source_directory):
        if font_file.endswith('.ttf'):
            font_path = os.path.join(source_directory, font_file)
            # Check if the font is italic
            if 'italic' in font_file.lower() and any(weight in font_file for weight in ['100', '200', '300', '400', '500', '600', '700', '800', '900']):
                shutil.move(font_path, italic_bold_folder)
            # Check if the font is bold (by weight)
            elif any(weight in font_file for weight in ['100', '200', '300', '400', '500', '600', '700', '800', '900']):
                shutil.move(font_path, bold_folder)
            # Check if the font is italic
            elif 'italic' in font_file.lower():
                shutil.move(font_path, italic_folder)
            # Otherwise, move to the normal folder
            else:
                shutil.move(font_path, normal_folder)
        elif font_file.endswith('.otf'):
            #Delete non-font files
            os.remove(os.path.join(source_directory, font_file))

# Usage
# organize_fonts('/path_to_your_fonts_directory')
organize_fonts('data/fonts')