import os
import re
from glob import glob
from tqdm import tqdm

raw_txt_dir = "RawTXTs"
txt_dir = "TXTs/"
txt_paths = glob(os.path.join(raw_txt_dir, "*", "*.txt"))
keywords = (
    "release",
    "released",
    "public",
    "publicly",
    "github",
    "gitlab",
    "huggingface co ",
    "osf io ",
    "open source",
    "accessible",
)


def replace_non_letters_with_spaces(input_string):
    # Replace non-letter characters with spaces
    result_string = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ]", " ", input_string)
    return result_string


def get_keyword_paras(txt):
    out_txt = ""
    txt = txt.replace("\r\n", "\n")
    paras = txt.split(".\n")
    for para in paras:
        proc_para = replace_non_letters_with_spaces(para.lower())
        proc_para_split = proc_para.split()
        if any(
            keyword in (proc_para_split if keyword.count(" ") == 0 else proc_para)
            for keyword in keywords
        ):
            out_txt += para + "\n----------------------\n\n"
    return out_txt


for path in tqdm(txt_paths):
    with open(path, "r", encoding="utf-8") as fp:
        txt = fp.read()
    out_txt = get_keyword_paras(txt)
    if out_txt:
        txt_path = path.replace("RawTXTs", "TXTs")
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        with open(txt_path, "w", encoding="utf-8") as fp:
            fp.write(out_txt)
