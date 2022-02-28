#! /usr/bin/env python
import sys
import argparse
import pandas as pd
import csv
import pickle

import requests

TRACE_DATA_URL = 'https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term={dataset}'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('sample')
    p.add_argument('gather_out')
    p.add_argument('gather_csv')
    p.add_argument('-o', '--output', required=True)
    p.add_argument('-S', '--save-run-info', required=True)
    args = p.parse_args()

    info_d = dict(sample=args.sample)

    print(f"retrieving trace info for {args.sample} from NCBI...")
    rawdata = requests.get(TRACE_DATA_URL.format(dataset=args.sample)).content.decode("utf-8")
    data = list(csv.DictReader(rawdata.splitlines(), delimiter=","))
    assert len(data) >= 1
    print(f"...got {len(data)} rows.")

    with open(args.save_run_info, 'w', newline='') as fp:
        w = csv.DictWriter(fp, fieldnames=data[0].keys())
        w.writeheader()
        for row in data:
            w.writerow(row)

    try:
        gather_df = pd.read_csv(args.gather_csv)
        info_d['n_matches'] = len(gather_df)
    except pd.errors.EmptyDataError:
        info_d['n_matches'] = 0

    with open(args.gather_out, 'rt') as fp:
        data = fp.read()
        if not len(data):
            p_weighted_covered = 0
        else:
            data = data.splitlines()
            line = data[-2]
            text = 'the recovered matches hit '
            assert line.startswith(text)
            line = line[len(text):].split('%')[0]
            p_weighted_covered = float(line)

        info_d['p_weighted_covered'] = p_weighted_covered

    with open(args.output, 'w', newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=info_d.keys())
        w.writeheader()
        w.writerow(info_d)


if __name__ == '__main__':
    sys.exit(main())
