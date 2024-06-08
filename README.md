## Description
Convert arxiv research papers into kindle format that can be read from KoReader as well as Google Play Books (browser only), which enables features such as saving and syncing highlights, bookmarks and much more!

![demo.gif](assets%2Fdemo.gif)

## Getting Started
```bash
git clone https://github.com/projektjoe/arxiv2kindle
cd arxiv2kindle
pip3 install -r requirements.txt
python3 main.py https://arxiv.org/abs/1706.03762
```
## Features
1. Works on any device that supports KoReader.
2. Parses title and author properly.
3. Handles references.
4. Handles SVGs.
5. Handles Math (LaTex) equations.

## Limitations
1. Does not work on Kindle devices yet, since the kindle software does not support parsing of advanced objects (such as LateX equations)
2. Performs conversion based on ar5iv (LateXML) and therefore new papers wont work (needs a week or two for the paper to be processed)
3. Tables are sometimes not very well formatted.
