import pickle as pkl
import re
import pandas as pd
import glob

reg_file = re.compile('.*/(?P<subject>[0-9]+)_(?P<session>[0-9]+)_.*\_outputDict\.pkl')

reg_button = re.compile('trial trial(?P<run>[0-9]+) event (?P<key>[a-z0-9]) at (?P<onset>[0-9]+\.[0-9]+)')

fns = glob.glob('../data/*.pkl')

df = []
for fn in fns:
    with open(fn, 'rb') as f:
        data = pkl.load(f)['eventArray']
        meta_info = reg_file.match(fn).groupdict()

        for run in data:
            for event in run:
                event=str(event)
                
                if reg_button.match(event):
                    d = reg_button.match(event).groupdict()
                    d.update(meta_info)

                    df.append(d)


df = pd.DataFrame(df)

df.to_csv('../data/behavior.tsv', sep='\t', index=False)
