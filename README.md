# Igbo-Speech-Dataset
This is a project to include Igbo in the CommonVoice platform

## Setup (What I did)
1. Installed Rust Nightly.
2. To install [Rust Nightly](https://rustup.rs/), I used ran the following code:

```curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh ```
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
This led to the `text/` folder.

7. Scraped the sentences into a new file from the WikiExtractor output dir. Because I was going to create a blocklist, I created a full export with all Wikipedia sentences as explained [here](https://github.com/common-voice/cv-sentence-extractor#create-a-blocklist-based-on-less-common-words).
```
cd ../cv-sentence-extractor
cargo run --release -- extract -l ig -d xxxxxx/wikiextractor/wikiextractor/text/ --no_check >> wiki.ig.all.txt
```
This gave me the `wiki.ig.all.txt` file attached in this repo.

8. At this point, I proceeded to generate the `ig.toml` file by adapting from one of the languages in the existing pull requests (don't remember which).

9.  Then I used the cvtools scripts to generate a list of the word frequency:
```
cd  ..
git clone https://github.com/dabinat/cvtools/
cd cvtools
python3 ./word_usage.py -i ../cv-sentence-extractor/wiki.ig.all.txt >> word_usage.en.txt
```
10. Then i experimented with 80 and 20 as maximum frequency, before settling for 20 as it gave more sentences which were still accurate.
```
python3 ./word_usage.py -i ../cv-sentence-extractor/wiki.ig.all.txt --max-frequency 20 --show-words-only >> ../cv-sentence-extractor/src/rules/disallowed_words/ig.txt
```

11. Finally, I extracted the sentences, leading to the `wiki.ig.txt` file:
```
cd .. 
cd cv-sentence-extractor
cargo run --release -- extract-file -l ig -d ../wikiextractor/wikiextractor/text/ >> wiki.ig.txt
```
12. Last step for the review was to shufffle the `wiki.ig.txt` file (leading to `ig-shuffled.txt`) and take the first 300 sentences for review [here](https://docs.google.com/spreadsheets/d/1sjtQh2-0FG2juN3e9BnM3wRSvoICcXvqx7z7L_LuZos/edit?usp=sharing). This Spreadsheet was adapted from the [review for Swahili](https://docs.google.com/spreadsheets/d/1QJd4KLcRyhVcagLWQzknJ02-7JZOSU60h0WJ6EkvrUU/edit?usp=sharing).
