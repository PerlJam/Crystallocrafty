import math

def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

###input pdb file name
pdb_code = "1LYZ" ### edit this in quotes for the name of your .pdb file!
pdb_filename = pdb_code + '.pdb'


'''handle = open("ss.txt.tmp2", "rU")
    records = list(SeqIO.parse(handle, "fasta"))
    handle.close()
    
    ###pull out secondary structure and sequences
    for i in records:
    if pdb_code in i.id[:4]:
    if 'sequence' in i.id:
    sequence = i
    elif 'secstr' in i.id:
    secstr = i'''

with open('ss.txt.tmp2') as fp:
    for name, seq in read_fasta(fp):
        if pdb_code in name[1:5]:
            if 'sequence' in name:
                sequence = seq
            elif 'secstr' in name:
                secstr = seq

lengths_of_structures = []
structures_to_crochet = []
length = 0
secstr = secstr.replace('T', 'S')
secstr = secstr.replace('B', 'S')
secstr = secstr.replace('E', 'S')

#generating instructions
for r in range(len(secstr)):
    res = secstr[r]
    ### recording length, will have to anticipate the length of the structure
    if res == 'H':
        length = length + 1
    elif res == 'B':
        length = length + 2.5
    elif res == 'S':
        length = length + 2.5
    elif res == 'T':
        length = length + 2.5
    elif res == 'G':
        length = length + 1.3
    elif res == 'I':
        length = length + 0.7
    elif res == 'E':
        length = length + 2.5
    else:
        length = length + 2.5
    
    try:
        if secstr[r+1] != res:
            if res == 'H':
                structures_to_crochet.append( 'Helix' )
            elif res == 'B':
                structures_to_crochet.append( 'Beta-Bridge' )
            elif res == 'S':
                structures_to_crochet.append( 'Unordered' )
            elif res == 'T':
                structures_to_crochet.append( 'Turn' )
            elif res == 'G':
                structures_to_crochet.append( 'Three-Turn Helix' )
            elif res == 'I':
                structures_to_crochet.append( 'Five-Turn Helix' )
            elif res == 'E':
                structures_to_crochet.append( 'Random-Coil' )
            lengths_of_structures.append( math.ceil(length) )
            length = 0
    except:
        pass

output_filename = pdb_code + '_crochet_output.txt'
output = open(output_filename, 'w')

for instruction in range(len(lengths_of_structures)):
    try:
        output.write('Step %s: %s for %s stitches. \n' % ((instruction+1), structures_to_crochet[instruction], lengths_of_structures[instruction]))
    except:
        pass
output.write('This project will require ' + str(sum(lengths_of_structures)) + ' stitches.')

output.close()