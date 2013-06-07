import OleFileIO_PL
import os.path
from glob import glob
from PIL import Image

def extract_images_from_folder(source_path, output_path):
    di3b_files = glob(os.path.join(source_path, '*.di3b'))
    print di3b_files
    for di3b_file in di3b_files:
        ole = OleFileIO_PL.OleFileIO(di3b_file)
        preview = ole.openstream('preview.bmp')
        left_t = ole.openstream('pod1texture.jpg')
        right_t = ole.openstream('pod2texture.jpg')
        left_i = Image.open(left_t)
        right_i = Image.open(right_t)
        full_i = Image.new(right_i.mode, (right_i.size[0] * 2, right_i.size[1]))
        full_i.paste(left_i, (0,0))
        full_i.paste(right_i, (1200,0))
        full_i_small = full_i.resize((1200, 800))
        full_i_small.save(os.path.join(output_path, os.path.splitext(os.path.split(di3b_file)[1])[0] + 'L.jpg'), 
                format="JPEG", quality=42, optimize=True, progressive=True)

source_path = '/vol/export/hercules/iBUG4D/'
output_path = '/vol/export/hercules/iBUG4Dexports/'


