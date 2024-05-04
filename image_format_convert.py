import argparse
from PIL import Image
import os
import logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

SUPPORTED_FORMATS = {
    "bmp": "BMP",
    "dib": "BMP",
    "eps": "EPS",
    "gif": "GIF",
    "im": "IM",
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "jpe": "JPEG",
    "pcd": "PCD",
    "pcx": "PCX",
    "png": "PNG",
    "pbm": "PPM",
    "pgm": "PPM",
    "ppm": "PPM",
    "psd": "PSD",
    "tif": "TIFF",
    "tiff": "TIFF",
    "xbm": "XBM",
    "xpm": "XPM",
    "webp": "WEBP",
    "ico": "ICO",
    "cur": "CUR",
    "tga": "TGA",
}


def convert(base_dir, file_name, target_format="jpeg"):
    if all(not item for item in [base_dir, file_name]):
        logging.error("No target file/path got")
        return

    file_full_path = ""
    # if no file name assigned, just input the full file path as base path, we will separate it into [base_dir] & [file_name]
    if not file_name and base_dir and '.' in base_dir:
        file_full_path = base_dir
        base_dir, file_name = os.path.split(file_full_path)
    elif base_dir and file_name:
        file_full_path = os.path.join(base_dir, file_name)
    else:
        logging.error("No legally file path found")
        return

    if not os.path.exists(file_full_path):
        logging.error(f"No base file found: {file_full_path}")
        return

    file_name_core, extension = os.path.splitext(file_name)
    extension = extension[1:]  # remove leading dot
    if not extension:
        logging.error(f"Illegal file found: {file_name} from path: {file_full_path}")
        return

    if extension.lower() == target_format:
        print(f"No need to do format convert")
        return

    img = Image.open(file_full_path)
    target_file_path = os.path.join(base_dir, f"{file_name_core}.{target_format}")
    target_file_type = SUPPORTED_FORMATS.get(target_format.lower())
    if target_file_type is None:
        logging.error(f"Unsupported file type: {extension}")
        return

    img.save(target_file_path, target_file_type)
    print(f"Saved img into: [{target_file_path}] converted from [{file_full_path}]")


def main():
    parser = argparse.ArgumentParser(description='Convert images.')
    parser.add_argument('-d', '--base_dir', help='The base directory of the image file.', required=True)
    parser.add_argument('-f', '--file_name', help='The name of the image file to convert.', required=False)
    parser.add_argument('-t', '--target_format', default='jpeg', choices=SUPPORTED_FORMATS.keys(),
                        help='The target format to convert to.')
    args = parser.parse_args()

    convert(args.base_dir, args.file_name, args.target_format)


if __name__ == "__main__":
    main()
