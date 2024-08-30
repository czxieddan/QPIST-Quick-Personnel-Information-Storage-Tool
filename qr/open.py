import os
import random
import string
import qrcode
import subprocess

def generate_unique_string(existing_strings, length=32):
    while True:
        new_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if new_string not in existing_strings:
            return new_string

def read_existing_strings(directory):
    if not os.path.exists(directory):
        return set()
    return {name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))}

def save_qr_code(data, path):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(path)

def open_folder(path):
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS, Linux
        subprocess.call(['open', path])

def main():
    base_dir = 'mumbers'
    os.makedirs(base_dir, exist_ok=True)
    
    existing_strings = read_existing_strings(base_dir)
    
    action = input("请输入 '1' 生成新字符串，或输入 '2' 打开已有字符串对应的文件夹: ")
    
    if action == '1':
        new_string = generate_unique_string(existing_strings)
        new_dir = os.path.join(base_dir, new_string)
        os.makedirs(new_dir)
        
        qr_code_path = os.path.join(new_dir, f'{new_string}.png')
        save_qr_code(new_string, qr_code_path)
        
        print(f'生成新目录: {new_dir}')
        print(f'二维码保存于: {qr_code_path}')
    elif action == '2':
        existing_string = input("请输入已有的32位字符串: ")
        if existing_string in existing_strings:
            folder_path = os.path.join(base_dir, existing_string)
            open_folder(folder_path)
            print(f'已打开文件夹: {folder_path}')
        else:
            print("输入的字符串不存在。")
    else:
        print("无效的输入。")

if __name__ == '__main__':
    main()