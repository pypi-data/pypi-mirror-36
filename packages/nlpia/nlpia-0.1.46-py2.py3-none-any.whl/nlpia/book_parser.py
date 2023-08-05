import os
import sys
import glob
import re
import logging

from nlpia.constants import BOOK_PATH


logger = logging.getLogger(__name__)
BLOCK_DELIMITERS = dict([('--', 'natural'), ('==', 'natural'), ('__', 'natural'), ('**', 'natural'),
                         ('++', 'latex'), ('//', 'comment')])
BLOCK_DELIMITER_CHRS = ''.join([k[0] for k in BLOCK_DELIMITERS.keys()])
BLOCK_HEADERS = dict([('[tip]', 'natural'), ('[note]', 'natural'), ('[important]', 'natural'), ('[quote]', 'natural')])
BLOCK_HEADERS4 = dict([(k[:4], v) for k, v in BLOCK_HEADERS.items()])

CRE_BLOCK_DELIMITER = re.compile(r'^[' + BLOCK_DELIMITER_CHRS + r']{2,240}$')
HEADER_TYPES = [('source', 'code'), ('latex', 'latex'), ('template="glossary"', 'glossary'), ("template='glossary'", 'glossary')]
VALID_TAGS = set(['anchor', 'attribute', 'blank_line', 'block_header', 'caption', 'code', 'code_end', 'code_start', ] + 
                 [b for b in BLOCK_DELIMITERS.values()] + 
                 [b + '_start' for b in BLOCK_DELIMITERS.values()] + 
                 [b + '_end' for b in BLOCK_DELIMITERS.values()] + 
                 ['natural_heading{}'.format(i) for i in range(1, 6)] + 
                 ['image_link', 'natural', 'natural_end', 'natural_start', 'code_header'])
INCLUDE_TAGS = set(['natural', 'caption'] + ['natural_heading{}'.format(i) for i in range(1, 6)])


def get_lines(file_path=BOOK_PATH):
    r""" Retrieve text lines from the manuscript Chapter*.asc and Appendix*.asc files

    Args:
        file_path (str): Path to directory containing manuscript asciidoc files
        i.e.: /Users/cole-home/repos/nlpinaction/manuscript/ or nlpia.constants.BOOK_PATH

    Returns:
        list of lists of str, one list for each Chapter or Appendix

    >>> lines = get_lines(os.path.join(BOOK_PATH))
    >>> next(lines)
    ('.../src/nlpia/data/book/Appendix F -- Glossary.asc',
     ['= Glossary\n',
      '\n',
      "We've collected some ...
    """
    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, '*.asc')
        files = glob.glob(file_path)
    elif os.path.isfile(file_path):
        files = [file_path]
    elif '*' in file_path:
        if os.path.sep not in file_path:
            file_path = os.path.join(os.path.abspath(os.path.curdir), file_path)
        files = glob.glob(file_path)
    lines = []
    for file in files:
        with open(file, 'r') as f:
            lines.append(f.readlines())
    return zip(files, lines)


def tag_lines(lines):
    r""" Naively tags lines from manuscript with: code, natural, heading, etc.

    Returns:
        list of tuples  [(tag, line), ...]

    >> VALID_TAGS == {'anchor', 'attribute', 'blank_line', 'block_header', 'caption', 'code', 'code_end', 'code_start',
    ... 'comment', 'comment_end', 'comment_start',
    ... 'natural_heading1', 'natural_heading2', 'natural_heading3', 'natural_heading4', 'natural_heading5',
    ... 'image_link', 'natural', 'natural_end', 'natural_start', 'source_header'}
    True
    >>> tag_lines('|= Title| :chapter: 0|Hello|cruel world|==Heading Level 2| \t| [source,bash]|====|$ grep this|====|'.split('|'))
    [('blank_line', ''), ('natural_heading1', '= Title'), ('attribute', ':chapter: 0'), ('natural', 'Hello'),
     ('natural', 'cruel world'), ('natural_heading2', '==Heading Level 2'), ('blank_line', ''),
     ('code_header', '[source,bash]'), ('code_start', '===='), ('code', '$ grep this'), ('code_end', '===='),
     ('blank_line', '')]
    """
    current_block_type = None
    block_terminator = None
    block_start = None
    tagged_lines = []
    for idx, line in enumerate(lines):
        # print(current_block_type)
        # print(line)
        normalized_line = line.lower().strip().replace(" ", "")

        # [source,...] with or without any following "----" block delimiter
        # TODO: make this a regex that classifies among the different types (source, glossary, tip, etc)
        header_type = next((HEADER_TYPES[i] for i in range(len(HEADER_TYPES)) if
                            normalized_line.startswith('[') and normalized_line[1:].startswith(HEADER_TYPES[i][0])),
                           None)
        if header_type:
            current_block_type = header_type[1]
            block_start = idx
            tag = current_block_type + '_header'
            block_terminator = None
        # [note],[quote],[important],... etc with or without any following "====" block delimiter
        elif normalized_line[:4] in BLOCK_HEADERS4:
            current_block_type = BLOCK_HEADERS4[normalized_line[:4]]
            block_start = idx
            tag = 'block_header'  # BLOCK_HEADERS[normalized_line]
            block_terminator = None
        # # "==", "--", '__', '++' block delimiters below block type ([note], [source], or blank line)
        # elif current_block_type
        #     if idx == block_start + 1:
        #         if line.strip()[:2] in ('--', '==', '__', '**'):
        #             block_terminator = line.strip()
        #             tag = current_block_type + '_start'
        #         elif line.strip()[:2] == '++':
        #             block_terminator = line.strip()
        #             tag = current_block_type + '_start'
        #         # # this should only happen when there's a "bare" untyped block that has started
        #         # else:
        #         #     block_terminator = line.strip()
        #         #     tag = current_block_type
        #     elif:
        # bare block delimiters without a block type already defined?
        elif CRE_BLOCK_DELIMITER.match(normalized_line) and normalized_line[: 2] in BLOCK_DELIMITERS:
            if not idx or not block_start or not current_block_type or not block_terminator:
                current_block_type = (current_block_type or BLOCK_DELIMITERS[normalized_line[:2]])
                block_start = idx 
                tag = current_block_type + '_start'
                block_terminator = normalized_line
            else:
                tag = current_block_type + '_end'
                current_block_type = None
                block_terminator = None
                block_start = 0
        elif current_block_type and (line.rstrip() == block_terminator or 
                                     (not block_terminator and not normalized_line)):
            tag = current_block_type + '_end'
            current_block_type = None
            block_terminator = None
            block_start = None  # block header not allowed on line 0
        elif current_block_type:
            tag = current_block_type
        elif not normalized_line:
            tag = 'blank_line'
        elif normalized_line.startswith(r'//'):
            tag = 'comment'
        elif normalized_line.startswith(r':'):
            tag = 'attribute'
        elif normalized_line.startswith('='):
            tag = 'natural_heading'
            tag += str(len([c for c in normalized_line[:6].split()[0] if c == '=']))
        elif normalized_line.startswith('.'):
            tag = 'caption'
        elif normalized_line.startswith('image:'):
            tag = 'image_link'
        elif normalized_line.startswith('[['):
            tag = 'anchor'
        else:
            tag = 'natural'
            current_block_type = None

        tagged_lines.append((tag, line.strip()))

    return tagged_lines


def main(book_dir=os.path.curdir, include_tags=None, verbosity=1):
    r""" Parse all the asciidoc files in book_dir, returning a list of 2-tuples of lists of 2-tuples (tagged lines) 

    >>> main(BOOK_PATH, verbosity=0)
    [('...src/nlpia/data/book/Appendix F -- Glossary.asc',
      [('natural_heading1', '= Glossary'),
       ('blank_line', ''),
       ('natural',
        "We've collected some definitions ...
    >>> main(BOOK_PATH, include_tags='natural', verbosity=1)
    = Glossary
    We've collected some definitions of some common NLP and ML acronyms and terminology here.footnote:[Bill Wilson...
    at the university of New South Wales in Australia has a more complete one here:...
    https://www.cse.unsw.edu.au/~billw/nlpdict.html]...
    You can find some of the tools we used to generate this list in the `nlpia` python package at...
    ...
    >>> tagged_lines = main(BOOK_PATH, include_tags=['natural', 'blank'], verbosity=0)
    >>> tagged_lines = main(BOOK_PATH, include_tags=['natural', 'blank'], verbosity=1)
    = Glossary
    <BLANKLINE>
    We've collected some definitions of some common NLP and ML acronyms and terminology here.footnote:[...
    >>> tagged_lines = main(BOOK_PATH, include_tags='natural', verbosity=1)
    = Glossary
    We've collected some definitions of some common NLP and ML acronyms and terminology here.footnote:[...
    """
    if verbosity:
        logger.info('book_dir: {}'.format(book_dir))
        logger.info('include_tags: {}'.format(include_tags))
        logger.info('verbosity: {}'.format(verbosity))

    include_tags = [include_tags] if isinstance(include_tags, str) else include_tags
    include_tags = None if not include_tags else set([t.lower().strip() for t in include_tags])
    sections = [(filepath, tag_lines(lines)) for filepath, lines in get_lines(book_dir)]
    if verbosity > 0:
        for filepath, tagged_lines in sections:
            if verbosity > 1:
                print('=' * 75)
                print(filepath)
                print('-' * 75)
            for tagged_line in tagged_lines:
                if include_tags is None or tagged_line[0] in include_tags or \
                        any((tagged_line[0].startswith(t) for t in include_tags)):
                    if verbosity == 1:
                        print(tagged_line[1])
                    if verbosity > 1:
                        print(tagged_line)
                else:
                    logger.debug('skipping tag {} because not in {}'.format(tagged_line[0], include_tags))
            if verbosity > 1:
                print('=' * 79)
                print()
    return sections


if __name__ == '__main__':
    args = sys.argv[1:]
    book_dir = os.path.curdir
    if args:
        book_dir = args[0]
        args = args[1:]
    include_tags = INCLUDE_TAGS
    if args:
        try:
            verbosity = int(args[0])
            include_tags = args[1:] or include_tags
        except ValueError:
            verbosity = 1
            include_tags = args

    if include_tags and include_tags[0].strip().lower()[: 3] == 'all':
        include_tags = None

    # print('Parsing Chapters and Appendices in: ' + book_dir)
    # print('***PRINTING LINES WITH TAGS***: ' + str(include_tags))
    main(book_dir=book_dir, include_tags=include_tags, verbosity=verbosity)
