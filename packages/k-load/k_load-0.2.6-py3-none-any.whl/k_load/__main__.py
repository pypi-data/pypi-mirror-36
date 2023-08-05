import re
from . import extractors

def run(url, save_dir='.'):
    params={}
    params['url'] = url
    params['save_dir'] = save_dir
    if re.search('bilibili.com', url):
        obj = extractors.Bilibili(**params)
        
    elif re.search('kg.qq.com', url):
        obj = extractors.KSong(**params)

    else:
        raise NotImplemented("I'm so sorry, but this website is not supported now......")

    obj.parse()
    obj.download()

def console_entry():
    import argparse
    parser = argparse.ArgumentParser(description='Downloader')
    parser.add_argument('url', type=str, help='the url of the source, should appear like http://example.com/')
    args = parser.parse_args()
    run(args.url)
