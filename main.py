from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import os
import time
from urllib.parse import urljoin
import re
import pandas as pd

def convert_token_type(tokens):
    # str -> int
    result = []
    for token in tokens:
        try:
            result.append(float(token))
        except:
            pass
    return result

def parse_lines(lines):
    parsed_lines = []
    for line in lines:
        try:
            tokens = re.split(" +", line)
            tokens = convert_token_type(tokens)
            if len(tokens) != 0:
                parsed_lines.append(tokens)
            # print("d:{}, {}".format(int(tokens[0]), tokens[1:]))
        except:
            pass
    return parsed_lines

def append_df(df, lines, colnames, y, m):
    for line in lines:
        try:
            index = []
            index.append("{}/{}/{}".format(str(y), str(m).zfill(2), str(int(line[0])).zfill(2)))
            index.append(line[-3])
            index.append(line[-2])
            index.append(line[-1])
            df_temp = pd.DataFrame([index], columns=colnames)
            df = pd.concat([df, df_temp], axis=0)
        except:
            pass
    return df

def main():
    y = 2017
    col_names = [
        "yyyy/mm/dd",
        "g", 
        "f",
        "R"
    ]
    sunspots_df = pd.DataFrame()
    for i in range(7):
        url = "https://solarwww.mtk.nao.ac.jp/mitaka_solar/sunspots/number/mtkdaily{}.txt".format(y+i)
        res = req.urlopen(url)
        body = str(BeautifulSoup(res, "html.parser"))
        blocks_split_token = " --------------------------------------------------------------------"
        blocks = body.split(blocks_split_token)

        for m, block in enumerate(blocks[:-1]):
            lines = block.splitlines()[7:-3]
            parsed_lines = parse_lines(lines)
            sunspots_df = append_df(sunspots_df, parsed_lines, col_names, y+i, m+1)
    
    print(sunspots_df)
    sunspots_df.to_csv("sunspots_2017_2023.csv")

if __name__ == "__main__":
    main()
