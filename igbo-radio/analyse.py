import re
import os,json
from langdetect import detect
from random import sample
from tqdm import tqdm


def is_contained(aut,text):
    texts=set([t.strip().lower() for t in text.split(' ')])
    auts = set([t.strip().lower() for t in aut.split(' ')])
    if len(auts.intersection(texts))==len(auts):
        return True
    else:
        return False

def cleanhtml(raw_html):
    # https://stackoverflow.com/a/12982689/11814682
    #cleanr = re.compile('<.*?>')
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def fast_detect_lang(s,num=3):
    cands = [a for a in s.split(' ') if remove_all(a).strip()!='']
    ids = [i for i in range(len(cands))]
    if ids!=[]:
        if len(cands)<=num:
            num = len(cands)-1
        val = sample(ids,num)
        try:
            lang_detected = [detect(cands[v]) for v in val]
        except Exception:
            return '_undefined'
        en = len([l for l in lang_detected if l=='en'])
        not_en = len([l for l in lang_detected if l!='en'])
        if en > not_en:
            #It is a largely English sentence
            return 'en'
        else:
            #It is of another language....hopefully Igbo
            return 'other'
    else:
        return '_undefined_'
 
 

def remove_all(w):
    w= re.sub(r'[\․●□•◆▪©!"■#€$%&\(\)\*\+/:,;<=>?@,\[\]^_`‘→{|}~«»”“]+','',w,flags=re.UNICODE)
    w=re.sub(r"[']+",'',w)
    w=w.strip()
    return w


def is_valid(w):
    w = remove_all(w)
    if len(w.split(' '))>=1:
        if len(w.split(' '))<=15:
            if not re.search(r'[A-Z][A-Z]+',w): #No abbreviations
                if not re.search(r'[A-Z]+\.*[A-Z]',w):
                    if not re.search(r'[0-9]+',w): # No numbers
                        try:
                            if fast_detect_lang(w)=='other':
                                return True
                        except Exception as e:
                            raise Exception(f'Error with {w} \n {e}')
    
    return False

def remove_bu(w):
    w=re.sub(r'^bụ ','',w,flags=re.UNICODE)
    return w


def preprocess_ig(w):
    w= w.strip()
    w=cleanhtml(w)
    #w = re.sub(r"^[;@#?!&$]+\", " ", w)   
    w= re.sub(r'^[\․●□•◆▪©!"■#€$%&\(\)\*\+/:<=>?@,\[\]^_`‘→{|}~«»”“]','',w,flags=re.UNICODE)
    w=re.sub(r'[\.\.]+','.',w,flags=re.UNICODE)
    w=re.sub(r'[■]','',w,flags=re.UNICODE)
    return w
 
def get_sent(sent,discarded,d,aa,split=False): 
    if split:
        #igs = [preprocess_ig(wr) for wr in d.split('.') if wr.strip()!=''] 
        igs = [preprocess_ig(wr) for wr in d.split(';') ]
        igs = [w.split('. ') for w in igs]
        
        #For comma
        igs = [w for m in igs for w in m]
        igs = [w.split(',') for w in igs]
        igs = [preprocess_ig(w) for m in igs for w in m]
    else:
        igs = [preprocess_ig(d)]
    for ig_ in igs:
        if ig_ and len(ig_)>0:
            if is_valid(ig_):
                if ig_ not in sent and len([d for d in [a not in ig_ for a in aa] if d==True])==len(aa):
                    sent.append(remove_bu(ig_))
            else:
                discarded.append(ig_)
                
    return sent,discarded


with open('../commonvoice_igbo_radio/commonvoice_igbo_radio/spiders/igboRadioCV.json','r',encoding='utf8') as f:
    data = json.load(f)
 
all_authors = list(set([ig['author'].strip() for ig in data ] ))
sentences = [] 
discarded=[]
with tqdm(total=len(data)) as pbar:  
    for ig in data:
        
        if not is_contained(ig['author'].strip(),ig['text']):
          
            
            sentences,discarded = get_sent(sentences,discarded,ig['text'],all_authors,split=True)
            sentences,discarded = get_sent(sentences,discarded,ig['title'],all_authors)
        pbar.update(1)

print(f'Got {len(sentences)} sentences')
  
  
with open('./igbo_radio_sentences_clean.txt','w+',encoding='utf8') as output:
    for s in sentences:
        output.write(s.strip()+'\n')
    
with open('discarded.txt','w+',encoding='utf8') as output:
    for s in discarded:
        output.write(s.strip()+'\n')
print('ALL DONE')

   