import os.path
import random

SAMPLE_LIST = 'sigs.rand10k.out'
DB = '/home/ctbrown/scratch/cover/gtdb-rs202.genomic.k31.cover.zip'

SAMPLES = [ os.path.basename(x.strip()) for x in open(SAMPLE_LIST) ]
SAMPLES = [ x[:-4] if x.endswith('.sig') else x for x in SAMPLES]
#random.shuffle(SAMPLES)
#SAMPLES = SAMPLES[:10]

PATH = '/group/ctbrowngrp/irber/data/wort-data/wort-sra/sigs/'

print(f"{len(SAMPLES)} samples total loaded.")

rule all:
    input:
        expand('results/{sample}.gather.out', sample=SAMPLES),
        expand('results/{sample}.summary.csv', sample=SAMPLES),
        expand('results/{sample}.runinfo.csv', sample=SAMPLES)

rule summarize_sample:
    input:
        gather_out = 'results/{sample}.gather.out',
        gather_csv = 'results/{sample}.gather.csv',
    output:
        summary = 'results/{sample}.summary.csv',
        runinfo = 'results/{sample}.runinfo.csv',
    shell: """
        ./scripts/summarize-sample.py {wildcards.sample} {input.gather_out} \
            {input.gather_csv} -o {output.summary} -S {output.runinfo}
    """

rule gather:
    input:
        sig = PATH + '{sample}.sig',
        db = DB,
    output:
        out = 'results/{sample}.gather.out',
        csv = 'results/{sample}.gather.csv',
    params:
        scaled=100000,
    shell: """
        sourmash gather {input.sig} {input.db} --scaled={params.scaled} \
            -o {output.csv} > {output.out} || touch {output.csv}
    """

