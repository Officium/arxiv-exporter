# arxiv-exporter [![Python 3.6](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-370/)

Export filtered [arXiv](http://arxiv.org/) papers.

You can wrap this repo with a scheduler to send the result to your mailbox.

## Requirements
```bash
pip install feedparser --upgrade
```

## Usage
For papers with primary category cs.AI or cs.LG in the past seven days, the following code will generate an HTML containing the title, authors, abstract and PDF link for each filtered paper. 
```bash
python run.py --past_days 7 --primary_categories cs.AI cs.LG
```
