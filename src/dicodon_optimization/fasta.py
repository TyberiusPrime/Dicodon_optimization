import re


def parse_fasta_to_dict(fasta):
    """Parse a fasta file into a dictionary of name -> sequence"""
    if not fasta.startswith(">"):
        raise ValueError("Input did not start with '>', not  a valid Fasta file")
    result = {}
    for block in fasta.split(">"):
        block = block.strip()
        if block:
            new_line_pos = block.find("\n")
            name = block[:new_line_pos]
            sequence_plus_whitespace = block[new_line_pos:]
            sequence = re.sub("\s+", "", sequence_plus_whitespace).lower()
            result[name] = sequence
    return result


def dict_to_fasta(fastaDict, filehandle, doWrap=80, doUpper=True):
    """Writes a Fasta file from a dictionary of
    keys: sequences. If the filename ends with '.gz',
    the output is gzipped.
    Wraps if doWrap is set (at position 80)"""
    genToFasta(fastaDict.items(), filehandle, doWrap, doUpper)


def wrappedIterator(width):
    def inner(text):
        i = 0
        length = len(text)
        while i < length:
            yield text[i : i + width]
            i += width

    return inner


def genToFasta(gen, filehandle, doWrap=80, doUpper=True):
    """Take a generator creating (key, sequence) tuples,
    write it to a file. Wraps if doWrap is set.
    @doUpper may be True, then call .upper, it may be False
    then call .lower, or it may be anything else - then keep them as they are.
    """
    for key, value in gen:
        if hasattr(key, "encode"):
            key = key.encode("utf-8")
        if hasattr(value, "encode"):
            value = value.encode("utf-8")
        filehandle.write(b">" + key + b"\n")
        if doWrap:
            it = wrappedIterator(doWrap)
            for line in it(value):
                print(line)
                if doUpper:
                    filehandle.write(line.upper() + b"\n")
                elif doUpper is False:
                    filehandle.write(line.lower() + b"\n")
                else:
                    filehandle.write(line + b"\n")
        else:
            filehandle.write(value + b"\n")
