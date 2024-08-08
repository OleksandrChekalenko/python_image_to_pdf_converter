import os
import re

def extract_last_two_digits(filename):
    # Знайти всі цифри в імені файлу
    digits = re.findall(r'\d+', filename)
    if digits:
        # Взяти останні дві цифри з останньої знайденої групи цифр
        return digits[-1][-2:]
    return None

def rename_files_in_folder(folder):
    for file_name in os.listdir(folder):
        if file_name.lower().endswith(('.jpg', '.jpeg')):
            # Отримати останні дві цифри з імені файлу
            last_two_digits = extract_last_two_digits(file_name)
            if last_two_digits:
                # Створити нове ім'я файлу
                new_file_name = f"{last_two_digits}.jpg"
                old_file_path = os.path.join(folder, file_name)
                new_file_path = os.path.join(folder, new_file_name)
                
                try:
                    # Перейменувати файл
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} -> {new_file_path}")
                except Exception as e:
                    print(f"Failed to rename {old_file_path}: {e}")

# Використання
image_folder = 'images'

rename_files_in_folder(image_folder)
