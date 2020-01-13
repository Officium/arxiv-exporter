import argparse
import re
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode

import feedparser


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) Chrome/76.0.3809.100'
}


def get_response(url):
    """Request url and parse result"""
    while True:
        response = feedparser.parse(url, request_headers=headers)
        if int(response.get('status')) == 200:
            return [entry for entry in response['entries'] if entry.get('title')]
        time.sleep(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--past_days', type=int, default=7)
    parser.add_argument('--batch_size', type=int, default=100, help='max_results per request')
    parser.add_argument('--primary_categories', nargs='+', default=['cs.LG', 'stat.ML'])

    option = parser.parse_args()
    categories = set(option.primary_categories)
    date_start = (datetime.now() - timedelta(days=option.past_days)).strftime('%Y-%m-%d')
    date_end = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    authors = []
    with open('authors', encoding='utf8') as f:
        for line in f:
            authors.append('(' + line.strip() + ')')
    authors_pattern = re.compile(('|'.join(authors)).encode('unicode-escape').decode(), re.IGNORECASE)

    results = []
    start = 0
    n = 0
    done = False
    while not done:
        batch_url = 'http://export.arxiv.org/api/query?' + urlencode({
            "search_query": ' OR '.join('cat:{}'.format(cat) for cat in categories),
            "start": start,
            "max_results": option.batch_size,
            "sortBy": 'lastUpdatedDate',
            "sortOrder": 'descending'
        })
        print(n, batch_url)
        for result in get_response(batch_url):
            date = result['updated'][:10]
            if date > date_end:  # today
                continue
            if date < date_start:  # out-of-date
                done = True
                break
            if result['arxiv_primary_category']['term'] in categories:
                authors = r';'.join(d['name'] for d in result['authors'])
                if re.match(authors_pattern, authors):
                    n += 1
                    title = '{}. '.format(n) + result['title'].rstrip('\n')
                    pdf_url = result['id']
                    summary = result['summary'].rstrip('\n')
                    for link in result['links']:
                        if link.get('title') == 'pdf':
                            result['pdf_url'] = link['href']
                    results.append(
                        '\n<p><B>{}</B> <a href="{}">Link</a></p>\n<p>{}</p>\n<p>{}</p>\n'
                        .format(title, result['pdf_url'], authors, summary))
        start += option.batch_size
        time.sleep(5)

    mail_msg = ''.join(results)
    with open('{}~{}.html'.format(date_start, date_end), 'w') as f:
        f.write(mail_msg)
