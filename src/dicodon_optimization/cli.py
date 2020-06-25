import click
from . import fasta


@click.group()
def main():
    pass


@main.command(help="Build a dicodon usage frequency table from a cDNA fasta file")
@click.argument("cdna_fasta_filename", type=click.File("r"))
@click.argument("output_filename", type=click.File("w"))
def build_table(cdna_fasta_filename, output_filename):
    seqs = cdna_fasta_filename.read()
    seqs = fasta.fasta_to_dict(seqs)
    print(seqs)


@main.command(help="Optimize sequences according to dicodon usage frequency")
@click.argument("input_fasta_filename", type=click.File("r"))
@click.argument("dicodon_frequency_table_filename", type=click.File("r"))
@click.argument("output_filename", type=click.File("r"))
def optimize_sequences(
    input_fasta_filename, dicodon_frequency_table_filename, output_filename
):
    pass


if __name__ == "__main__":
    main()
