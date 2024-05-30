import os
from tqdm.contrib import tzip

def get_file_name(path:str)->str:
    """ 入力されたpathのファイル名のみを出力

    :param path: 分割するパス
    :return: 入力されたパスのファイル名
    """
    return os.path.splitext(os.path.basename(path))[0]

def get_file_list(dir_path:str, ext:str)->list:
    """ 任意のディレクトリ内に存在する任意の拡張子のファイルのパスをリストアップする

    :param dir_path: 探索するディレクトリのパス
    :param ext: 探索対象の拡張子
    :return: ファイルパスのリスト
    """
    if os.path.isdir(dir_path):
        return [f'{dir_path}/{file_path}' for file_path in os.listdir(dir_path) if os.path.splitext(file_path)[1] == ext]
    else:
        return [dir_path]

def main(dir_path:str, out_path:str, ext:str=".wav")->list:
    path_list = get_file_list(dir_path, ext)    # パスリストの作成
    # print(path_list)

    filename_list = [get_file_name(path) for path in path_list] # ファイル名のリストを作成

    for file_name, path in tzip(filename_list, path_list):
        """ テキストへの書き出し """
        with open(out_path, 'a') as f:
            f.write(f'{file_name}|{path}\n')

if __name__ == '__main__':
    dir_path = 'C:\\Users\\kataoka-lab\\Desktop\\sound_data\\mix_data\\subset_DEMAND_hoth_0000dB_0.5sec_1ch\\train\\clean'
    out_path = 'C:\\Users\\kataoka-lab\\Desktop\\sound_data\\mix_data\\subset_DEMAND_hoth_0000dB_0.5sec_1ch\\train.txt'

    f = open(out_path, 'w')
    f.close()

    main(dir_path, out_path)


