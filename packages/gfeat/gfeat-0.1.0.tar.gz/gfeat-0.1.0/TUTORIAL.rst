========
Tutorial
========

GFGenome
--------
To work with either custom files or with Ensembl genomes, a user needs a GFGenome object::

    from gfeat.genome import GFGenome
    # working with custom files
    gfData = GFGenome(reference_name,
                      annotation_name,
                      gtf_path_or_url=gtf,
                      transcript_fasta_paths_or_urls=fasta,
                      )
    # working with an Ensembl genome, e.g. Ensembl release 75
    from pyensembl.ensembl_release import EnsemblRelease
    gfData = GFGenome(copy_genome=EnsemblRelease(75))

Firstly, it is possible to get different genome features using a GFGenome object, i.e. consensus Kozak sequence,
Kozak matrix, consensus stop codon context, stop codon context matrix, codon pair bias and nucleobase mutation table.
Example for the consensus Kozak sequence::

    # digit representation of the Kozak sequence
    gfData.get_consensus_Kozak_seq()
    # its letter representation
    gfData.get_consensus_Kozak_seq(seq=True)

Furthermore, it is possible to get transcripts for this genome through different parameters::

    # to get a GFtranscript object by its id
    gfTranscript = gfData.gftranscript_by_id("ENST00000304391")
    # if you need a pyensembl.transcript object, please use transcript_by_id
    gfData.transcript_by_id("ENST00000304391")
    # NOTE that all other functions return GFtranscript objects, e.g.
    gfData.transcripts(22, "+")

GFTranscript
------------
Let us reuse a GFTranscript object which we got in the previous part of the tutorial::

    gfTranscript = gfData.gftranscript_by_id("ENST00000304391")

One can get the following properties for a transcript: codon counts, 3'UTR motif counts, 5'UTR motif counts,
codon usage, Gs and Cs percentage, Kozak sequence, stop codon context and codon pairs frequency. Example for the
Kozak sequence::

    gfTranscript.get_Kozak_seq()

Example for codon pairs frequency::

    gfTranscript.get_codon_pairs_frequency()

FivePrimeUTRSeq
---------------
The special feature of *gfeat* is that its users can work with 5'UTR region more thorough. This is achieved through FivePrimeUTRSeq
class. Its object contains a list of all 5' UTR sequences with and without introns for this creature, their intervals,
respective transcripts, sequences and intervals of exons. To create a FivePrimeUTRSeq object one needs a GFGenome or
pyensembl.Genome object. Optionally, the user can choose whether to reverse-complement the sequences, specify a contig
and a strand::

    ds = FivePrimeUTRSeq(gfData, False, 22, '+')

UpstreamAUG
-----------
In addition, one can find all start codons (AUGs) for a specified 5'UTR sequence, check whether it is in frame with the
canonical start and has a corresponding stop codon. For this purpose, use an UpstreamAUG object::

    # creating a model to score AUGs
    model = UpstreamAUG(True, True)
    # getting the following data about AUGs: their position and type (e.g. in-frame with
    # a corresponding stop codon). The data will be appended to the passed dictionary
    model.predict_on_sample_with_stop_pandas(fivePrimeUTR_seq, dictionary, '-', fivePrimeUTR_start_position)

Auxiliary functions
-------------------
To make the *gfeat*'s usage easier, it provides some auxiliary functions. The first of them is
VCFMutator.mutate_sequence(interval, fasta=None, seq_whole=None). It takes an interval, Fasta file or a
sequence and a VCF file and returns all possible mutated sequences and the positions of the mutations. An example of its
usage::

    # creating a VCFMutator object
    mutator = VCFMutator(False, True, vcf_file, True)
    # getting a list of tuples [(DNA string, variant ids, reference nucleobases, altered nucleobases), ...]
    # consisting of a DNA sequence, positions of variants that were substituted, their reference
    # nucleobases and altered nucleobases.
    # In addition the number of mutations is displayed
    e, m = mutator.mutate_sequence(interval, False, seq)

There are many different ways how VCFMutator.mutate_sequence(interval, fasta=None, seq_whole=None) function can be used.
Please refer to the specification and the code for more information; or contact the lead developers directly.

The second important auxiliary function is VCFMutator.mutate_codon_context(intervals, seqs, column_names). It allows the
user to get a table with positions of variants and their types (heterozygous or homozygous) in the given intervals for
the given sequences. Let us reuse the VCFMutator from the previous example, then we have::

    # a line from GFGenome.get_nucleobase_mutation_table(), therefore the intervals and sequences
    # which are used here are intervals and sequences for Kozak sequence and stop codon context
    df_nucleobases_line = mutator.mutate_codon_context([Interval_Kozak, Interval_stop],
                                                       [Kozak_seq, stop_codon_context], ["K_", "S_"])

The other 2 functions are reverse_complement(dna) and PCA_with_standard_sample_deviation_scaling(df, n_comp=2), and they can be found in the module
named utils.
