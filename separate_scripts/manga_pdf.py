from PIL import Image
import os
import re

def extract_last_two_digits(filename):
    # Знайти всі цифри в імені файлу
    digits = re.findall(r'\d+', filename)
    if digits:
        # Взяти останні дві цифри з останньої знайденої групи цифр
        return int(digits[-1][-2:])
    return -1

def create_pdf(image_folder, output_pdf, quality=100):
    image_list = []
    
    # Отримати список файлів у папці та відсортувати їх за останніми двома цифрами в імені
    files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.jpg', '.jpeg'))]
    sorted_files = sorted(files, key=extract_last_two_digits)
    
    for file_name in sorted_files:
        file_path = os.path.join(image_folder, file_name)
        try:
            image = Image.open(file_path)
            image_list.append(image.convert('RGB'))
        except Exception as e:
            print(f"Failed to open image {file_path}: {e}")

    if image_list:
        try:
            image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:], quality=quality)
            print(f"PDF created successfully: {output_pdf}")
        except Exception as e:
            print(f"Failed to create PDF: {e}")
    else:
        print("No images found to create PDF.")

# Використання
image_folder = 'images'
output_pdf = 'output.pdf'

create_pdf(image_folder, output_pdf)
