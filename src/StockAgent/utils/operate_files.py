import os, shutil
from datetime import datetime

def create_directory(dir_path, is_empty=False):
    if os.path.exists(dir_path):
        if is_empty:
            try:
                shutil.rmtree(dir_path)
                print(f"All contents in the directory '{dir_path}' have been removed successfully")
            except OSError as e:
                print(f"Remove {dir_path} Error: : {e.strerror}")
        else:
            return

    try:
        os.makedirs(dir_path)
    except OSError as e:
        print(f"Recreate {dir_path} Error: : {e.strerror}")

    return

def walk_directory(directory, callback):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            callback(file_path)

    return

def extract_filename(filename, with_suffix = False):

    if not os.path.exists(filename):
        return ''

    if not with_suffix:
        return os.path.splitext(os.path.basename(filename))[0]
    else:
        return os.path.basename(filename)

def process_file(path):
    print(f'Processing file: {path}')

import os

def get_latest_file(directory, suffix='.csv'):
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    files = [f for f in files if os.path.isfile(f) if f.endswith(suffix)]
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def check_installed_font():
    # List of fonts to search for
    target_fonts = ['PingFang SC', 'Songti SC', 'STHeiti', 'Heiti SC']

    import matplotlib.font_manager as fm

    # Get all system fonts
    available_fonts = set(f.name for f in fm.fontManager.ttflist)

    # Check which ones exist
    for font in target_fonts:
        if font in available_fonts:
            print(f'✅ Installed: {font}')
        else:
            print(f'❌ Not Found: {font}')

def check_whether_files_created_today(filename):

    if not os.path.exists(filename):
        return  False

    # Get the creation time of the file
    creation_time = os.path.getctime(filename)
    creation_date = datetime.fromtimestamp(creation_time)
    today = datetime.today()

    if creation_date.date() == today.date():
        return True
    else:
        return False

if __name__ == '__main__':
    walk_directory("../etf/dataset", process_file)