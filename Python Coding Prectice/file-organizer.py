import os
import shutil

def organize(folder_path):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            ext = file.split(".")[-1].lower()
            ext_folder = os.path.join(folder_path, ext)

            if not os.path.exists(ext_folder):
                os.makedirs(ext_folder)

            shutil.move(file_path, os.path.join(ext_folder, file))

    print("Files organized successfully!")

if __name__ == "__main__":
    path = input("Enter folder path: ")
    organize(path)
