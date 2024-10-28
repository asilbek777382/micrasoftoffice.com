import os

def decrypt_file(file_path):
    key = 13
    with open(file_path, 'rb') as file:
        content = file.read()

    decrypted_content = bytearray()
    for byte in content:
        decrypted_content.append(byte ^ key)

    original_file_path = file_path.replace('.encrypted', '')
    with open(original_file_path, 'wb') as original_file:
        original_file.write(decrypted_content)

    print(f"{file_path} shifrdan chiqarildi va {original_file_path} ga saqlandi.")

    os.remove(file_path)
    print(f"Shifrlangan fayl {file_path} o'chirildi.")

def decrypt_all_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.encrypted'):
                file_path = os.path.join(root, filename)
                decrypt_file(file_path)

def main():
    target_folder = '/root/Desktop/yangi'

    if os.path.exists(target_folder):
        decrypt_all_files_in_folder(target_folder)
    else:
        print("Papka topilmadi.")

if __name__ == "__main__":
    main()
