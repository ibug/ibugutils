import OleFileIO_PL
import os.path
from glob import glob
from PIL import Image

def extract_images_from_folder(source_path, output_path):
    di3b_files = glob(os.path.join(source_path, '*.di3b'))
    skip_count = 0
    for di3b_file in di3b_files:
        output_file = os.path.join(output_path, 
                os.path.splitext(os.path.split(di3b_file)[1])[0]) + '.jpg'
        if os.path.isfile(output_file):
            skip_count += 1
            continue
        ole = OleFileIO_PL.OleFileIO(di3b_file)
        left_t = ole.openstream('pod1texture.jpg')
        right_t = ole.openstream('pod2texture.jpg')
        left_i = Image.open(left_t)
        right_i = Image.open(right_t)
        full_i = Image.new(right_i.mode, 
                (right_i.size[0] * 2, right_i.size[1]))
        full_i.paste(left_i, (0,0))
        full_i.paste(right_i, (1200,0))
        full_i_small = full_i.resize((1200, 800))
        full_i_small.save(output_file, format="JPEG", quality=42, 
                optimize=True, progressive=True)
    if skip_count:
        print '{0} frames skipped.'.format(skip_count)


def extract_all_textures_from_ibug_structured_recordings(source_path, output_path):
    for potential_subject in os.listdir(source_path):
        full_ps = os.path.join(source_path, potential_subject)
        if os.path.isdir(full_ps) and 'DI4D' in os.listdir(full_ps):
            output_subject = os.path.join(output_path, potential_subject)
            if not os.path.isdir(output_subject):
                os.mkdir(output_subject)
            full_ps_di4d = os.path.join(full_ps, 'DI4D')
            for session in os.listdir(full_ps_di4d):
                full_session = os.path.join(full_ps_di4d, session)
                print full_session
                if os.path.isdir(full_session):
                    output_session = os.path.join(output_subject, session)
                    if not os.path.isdir(output_session):
                        os.mkdir(output_session)
                    print 'extracting images from session {0}'.format(full_session)
                    extract_images_from_folder(
                            os.path.join(full_session, 'frames'), output_session)

if __name__ is '__main__':    
    source_path = '/vol/hercules/iBUG4D/'
    output_path = '/vol/hercules/iBUG4Dexports/'
    extract_all_textures_from_ibug_structured_recordings(source_path, output_path)
