import os
import requests
from tqdm import tqdm, trange

# Set model to download: 124M, 335M or 774M
model_name = "124M"

# From ./gpt_2.py
# Copied here due to import errors
def download_file_with_progress(url_base, sub_dir, model_name, file_name):
    """General utility for incrementally downloading files from the internet
    with progress bar
    from url_base / sub_dir / filename
    to local file system sub_dir / filename

    Parameters
    ----------
    file_name : str
        name of file to get e.g. "hparams.json"
    sub_dir: str
        subdirectory inside which to get and copy locally eg. "models/124M"
        no trailing slash
    url_base : str
        Start of URL location specifying server and any base directories no
        trailing slash
        e.g. "https://storage.googleapis.com/gpt-2"
    """

    # set to download 1MB at a time. This could be much larger with no issue
    DOWNLOAD_CHUNK_SIZE = 1024 * 1024
    r = requests.get(url_base + "/models/" + model_name + "/" + file_name, stream=True)
    with open(os.path.join(sub_dir, file_name), 'wb') as f:
        file_size = int(r.headers["content-length"])
        with tqdm(ncols=100, desc="Fetching " + file_name,
                  total=file_size, unit_scale=True) as pbar:
            for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                f.write(chunk)
                pbar.update(DOWNLOAD_CHUNK_SIZE)

def download_gpt2(model_dir='models', model_name='124M'):
    """Downloads the GPT-2 model into the current directory
    from Google Cloud Storage.

    Parameters
    ----------
    model_dir : str
        parent directory of model to download

    model_name : str
        name of the GPT-2 model to download.
        As of 22 May 2019 one of "124M" or "355M" but may later include other
        model sizes

    Adapted from https://github.com/openai/gpt-2/blob/master/download_model.py
    """

    # create the <model_dir>/<model_name> subdirectory if not present
    sub_dir = os.path.join(model_dir, model_name)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    sub_dir = sub_dir.replace('\\', '/')  # needed for Windows

    for file_name in ['checkpoint', 'encoder.json', 'hparams.json',
                      'model.ckpt.data-00000-of-00001', 'model.ckpt.index',
                      'model.ckpt.meta', 'vocab.bpe']:
        download_file_with_progress(url_base="https://openaipublic.blob.core.windows.net/gpt-2",
                                    sub_dir=sub_dir,
                                    model_name=model_name,
                                    file_name=file_name)

# Download the model - should only need to run this once
# Saves the model in a 'models' folder
download_gpt2(model_name=model_name)