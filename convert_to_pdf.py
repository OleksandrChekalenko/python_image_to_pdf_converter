from PIL import Image
import os
import re

def delete_files_not_matching_pattern(folder):
    pattern = re.compile(r'.*_\d{1,3}\.jpg$')
    
    # Отримати список всіх файлів у папці
    all_files = os.listdir(folder)
    initial_count = len(all_files)
    
    # Фільтрувати файли, які відповідають патерну
    matching_files = [file for file in all_files if pattern.match(file)]
    final_count = len(matching_files)
    
    # Видалити файли, які не відповідають патерну
    for file_name in all_files:
        if not pattern.match(file_name):
            file_path = os.path.join(folder, file_name)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    
    print(f"Initial file count: {initial_count}")
    print(f"Final file count: {final_count}")

def extract_last_digits(filename):
    # Знайти всі цифри в імені файлу
    digits = re.findall(r'\d+', filename)
    if digits:
        # Взяти останні до трьох цифр з останньої знайденої групи цифр
        return digits[-1][-3:]
    return None

def rename_files_in_folder(folder):
    for file_name in os.listdir(folder):
        if file_name.lower().endswith(('.jpg')):
            # Отримати останні до трьох цифр з імені файлу
            last_digits = extract_last_digits(file_name)
            if last_digits:
                # Створити нове ім'я файлу
                new_file_name = f"{last_digits}.jpg"
                old_file_path = os.path.join(folder, file_name)
                new_file_path = os.path.join(folder, new_file_name)
                
                try:
                    # Перейменувати файл
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} -> {new_file_path}")
                except Exception as e:
                    print(f"Failed to rename {old_file_path}: {e}")

def extract_last_two_digits(filename):
    # Знайти всі цифри в імені файлу
    digits = re.findall(r'\d+', filename)
    if digits:
        # Взяти останні дві цифри з останньої знайденої групи цифр
        return int(digits[-1][-3:])
    return -1

def create_pdf(image_folder, output_pdf, quality=100):
    image_list = []
    
    # Отримати список файлів у папці та відсортувати їх за останніми двома цифрами в імені
    files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.jpg'))]
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
output_pdf = 'rename.pdf'

delete_files_not_matching_pattern(image_folder)
rename_files_in_folder(image_folder)
create_pdf(image_folder, output_pdf)
