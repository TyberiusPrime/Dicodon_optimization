import click
import json
from . import fasta, dicodon_optimization


@click.group()
def main():
    pass


@main.command(help="Build a dicodon usage frequency table from a cDNA fasta file")
@click.argument("cdna_fasta_filename", type=click.File("r"))
@click.argument("output_filename", type=click.File("w"))
@click.option("--format", type=click.Choice(["json", "tab"], case_sensitive=True))
def build_table(cdna_fasta_filename, output_filename, format):
    seqs = cdna_fasta_filename.read()
    seqs = fasta.parse_fasta_to_dict(seqs)
    freqs = dicodon_optimization.dicodon_score_dict_from_sequences(seqs.values())
    if format == "json":
        freqs = {"-".join(k): v for (k, v) in freqs.items()}
        output_filename.write(json.dumps(freqs, indent=4))
    else:
        for ((a, b), c) in freqs.items():
            output_filename.write(f"{a.upper()}{b.upper()}\t{c:.2f}\n")
    print(f"calculated frequency table, stored in {output_filename.name}")


@main.command(help="Optimize sequences according to dicodon usage frequency")
@click.argument("input_fasta_filename", type=click.File("r"))
@click.argument("dicodon_frequency_table_filename", type=click.File("r"))
@click.argument("output_filename", type=click.File("wb"))
def optimize_sequences(
    input_fasta_filename, dicodon_frequency_table_filename, output_filename
):
    freqs = json.load(dicodon_frequency_table_filename)
    freqs = {tuple(k.split("-")): v for (k, v) in freqs.items()}
    input = fasta.parse_fasta_to_dict(input_fasta_filename.read())
    output = {}
    for k, v in input.items():
        output_name = f"{k} optimized with {dicodon_frequency_table_filename.name}"
        aa = dicodon_optimization.translate_to_aa(v)
        optimized = dicodon_optimization.optimize_dicodon_usage(aa, freqs)
        output[output_name] = optimized[0]
    fasta.dict_to_fasta(output, output_filename)
    pass


if __name__ == "__main__":
    main()
