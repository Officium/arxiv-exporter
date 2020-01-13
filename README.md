# arxiv-exporter [![Python 3.6](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-370/)

Alerts by Google Scholar may miss some papers published by [arXiv](http://arxiv.org/).
This repo provides a simple python script to follow these papers.
One can schedule the script to send the result to your mailbox.

## Requirements
```bash
pip install feedparser --upgrade
```

## Usage
Modify `authors` file to list authors you want to follow. 
For papers with primary category cs.AI or cs.LG in the past seven days, 
the following code will generate an HTML containing the title, authors, abstract and PDF link for each filtered paper. 
```bash
python run.py --past_days 7 --primary_categories cs.AI cs.LG
```
