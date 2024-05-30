import os
import numpy as np
import wave
import array
from tqdm.contrib import tzip

def get_file_list(dir_path:str, ext:str='.wav') -> list:
    """
    指定したディレクトリ内の任意の拡張子のファイルをリストアップ

    Parameters
    ----------
    dir_path(str):ディレクトリのパス
    ext(str):拡張子

    Returns
    -------
    list[str]
    """
    if os.path.isdir(dir_path):
        return [f'{dir_path}/{file_path}' for file_path in os.listdir(dir_path) if os.path.splitext(file_path)[1] == ext]
    else:
        return [dir_path]
def make_dir(path:str)->None:
    """
    目的のディレクトリを作成(ファイル名が含まれる場合,親ディレクトリを作成)

    Parameters
    ----------
    path(str):作成するディレクトリのパス

    Returns
    -------
    None
    """
    """ 作成するディレクトリが存在するかどうかを確認する """
    _, ext = os.path.splitext(path) # dir_pathの拡張子を取得
    if len(ext) == 0:   # ディレクトリのみ場合
        os.makedirs(path, exist_ok=True)
    elif not (ext) == 0:    # ファイル名を含む場合
        os.makedirs(os.path.dirname(path), exist_ok=True)

def load_wav(wave_path:str)->tuple:
    """
    音声ファイルの読み込み

    Parameters
    ----------
    wav_path(str):パス

    Returns
    -------

    """
    with wave.open(wave_path, "r") as wav:
        prm = wav.getparams()   # パラメータオブジェクト
        wave_data = wav.readframes(wav.getnframes())    # 音声データの読み込み(バイナリ形式)
        wave_data = np.frombuffer(wave_data, dtype=np.int16)    # 振幅に変換
        # wave_data = wave_data / np.iinfo(np.int16).max  # 最大値で正規化
        wave_data = wave_data.astype(np.float64)
        # if not prm.framerate == sample_rate:    # wavファイルのサンプリング周波数が任意のサンプリング周波数と違う場合
        #     prm.amplitude = resample(np.astype(np.float64), prm.framerate, sample_rate)  # サンプリング周波数をあわせる
    # print(f'prm:{prm}')
    return wave_data, prm

def save_wav(out_path:str, wav_data:list, prm:object, sample_rate:int=16000)->None:
    """
    wav_dataの保存

    Parameters
    ----------
    out_path(str):出力パス
    wav_data(list[float]):音源データ
    prm(object):音源データのパラメータ
    sample_rate(int):サンプリング周波数

    Returns
    -------
    None
    """
    # wav_file = wave.Wave_write(out_path)
    # wav_file.setparams(prm)
    # wav_file.setframerate(sample_rate)
    # #wav_file.writeframes(array.array('h', wav.astype(np.int16)).tostring())
    # wav_file.writeframes(array.array('h', wav_data.astype(np.int16)).tobytes())
    # wav_file.close()

    # print(f'out_path:{out_path}')
    make_dir(path=out_path)
    with wave.open(out_path, "wb") as wave_file:    # ファイルオープン
        wave_file.setparams(prm)    # パラメータのセット
        # wave_file.setframerate(sample_rate) # サンプリング周波数の上書き
        wave_file.writeframes(array.array('h', wav_data.astype(np.int16)).tobytes())    # データの書き込み

def padding_data(clean_path, noise_path):

    # 音声の読み込み
    clean_data, clean_prm = load_wav(clean_path)   # cleanの読み込み
    noise_data, noise_prm = load_wav(noise_path)   # noisyの読み込み
    # print(f'clean:{len(clean_data)}')
    # print(f'noise:{len(noise_data)}')

    # 長い音声長に合わせる
    if len(clean_data) > len(noise_data):
        noise_pad = np.zeros(len(clean_data))
        noise_pad[:len(noise_data)] = noise_data
        save_wav(noise_path, wav_data=noise_pad, prm=clean_prm) # 書き込み
        # print(f'noise:{len(noise_pad)}')
    else:
        clean_pad = np.zeros(len(noise_data))
        clean_pad[:len(clean_data)] = clean_data
        save_wav(clean_path, wav_data=clean_pad, prm=noise_prm) # 書き込み
        # print(f'clean:{len(clean_pad)}')


if __name__ == '__main__':
    clean_dir = 'C:\\Users\\kataoka-lab\\Desktop\\sound_data\\mix_data\\subset_DEMAND_hoth_0000dB_0.5sec_1ch\\clean\\'
    noise_dir = 'C:\\Users\\kataoka-lab\\Desktop\\sound_data\\mix_data\\subset_DEMAND_hoth_0000dB_0.5sec_1ch\\noisy\\'

    clean_list = get_file_list(clean_dir)
    noise_list = get_file_list(noise_dir)

    for clean_path, noise_path in tzip(clean_list, noise_list):
        padding_data(clean_path, noise_path)