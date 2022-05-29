import re
import os
from datetime import datetime
import pandas as pd
import argparse

parser = argparse.ArgumentParser(prog="File parser.", description='Input file to process. Run command e.g. python x.py file_name.md', usage='%(prog)s [options]')
parser.add_argument('-f','--filename', help='e.g. file_name.md', required=True)
args = vars(parser.parse_args())
fname     = args['filename']  

file = open(fname, "r")
raw  = file.read().split('any Twitter client.', 1)[-1]
data = os.linesep.join([s for s in raw.splitlines() if s])

def get_date(input):
  out = datetime.strptime(input, '%d %B %Y')
  return(out)

def get_url(raw):
  out = re.search('\((.*)\)\:', raw).group(1)
  return(out)

def get_id(url):
  out = re.sub('.*status/', '', url)
  out = re.search('\d+',out).group(0)
  return(out)

def get_text(raw):
  out = re.search('\)\:\s(.*)',raw).group(1)
  return(out)

df = pd.DataFrame(data.splitlines(), columns=['raw'])
df['date'] = df['raw'].str.extract('\[(\s?\d+\s+[A-z]+\s+\d+)\]')
df['date'] = df['date'].apply(get_date)
df['url'] = df['raw'].apply(get_url)
df['id'] = df['url'].apply(get_id)
df['text'] = df['raw'].apply(get_text)
df['deleted'] = df['url'].map(lambda x: False if '[live]' in str(x) else True)
df = df.drop(['raw'], axis=1)

deleted = df[df['deleted']==True]

print(len(df['text']))
print(len(deleted['text']))

df.to_csv(fname+'-all-archived-tweets.csv', index=False)
deleted.to_csv(fname+'-deleted-tweets.csv', index=False)