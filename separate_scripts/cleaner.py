import os
import re

def delete_files_not_matching_pattern(folder):
    pattern = re.compile(r'.*_\d{2}\.jpg$')
    
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

# Використання
image_folder = 'images'

delete_files_not_matching_pattern(image_folder)
