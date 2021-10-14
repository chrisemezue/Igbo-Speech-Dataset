# Igbo-Speech-Dataset
This is a project to include Igbo in the CommonVoice platform

## Setup (What I did)
1. Installed Rust Nightly (follow the instructions and customize the install to select the nightly channel)
2. Installed pip3 in case it's not installed on your system already

3. Cloned this repo:
```bash
git clone https://github.com/Common-Voice/cv-sentence-extractor.git
```

4. ### Wikipedia extraction
I downloaded the wikipedia extractor 
```bash
git clone https://github.com/attardi/wikiextractor.git
```
5. Then I downloaded the [Igbo Wikipedia back-dump](https://dumps.wikimedia.org/igwiki/20211001/) and selected the one with `pages-articles-multistream` in its name -- [here](https://dumps.wikimedia.org/igwiki/20211001/igwiki-20211001-pages-articles-multistream.xml.bz2)
```
bzip2 -d igwiki-20211001-pages-articles-multistream.xml.bz2
```
6. Used WikiExtractor to extract the dump 
```
cd wikiextractor
python3 WikiExtractor.py --json xxxxxxx/igwiki-20211001-pages-articles-multistream.xml
```
7. Scraped the sentences into a new file from the WikiExtractor output dir 
```
cd ../cv-sentence-extractor
cargo run --release -- extract -l en -d xxxxxx/wikiextractor/wikiextractor/text/ --no_check >> wiki.ig.all.txt
```
8. At this point, I proceeded to generate the `ig.toml` file by adapting from one of the languages in the pull requests (don't remember which).
9.  ### Created a blocklist based on less common words
