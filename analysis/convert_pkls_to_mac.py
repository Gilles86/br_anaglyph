import pickle as pkl
import glob 

fns = glob.glob('../data/*.pkl')


for fn in fns:
    with open(fn, 'rb') as infile:
        content = infile.read()

    with open(fn, 'wb') as output:
        for line in content.splitlines():
            output.write(line + str.encode('\n'))

