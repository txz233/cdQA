import os
import wget
import requests
from github import Github


def download_squad_assets():
    squad_urls = [
        'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json',
        'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json',
    ]

    for squad_url in squad_urls:
        wget.download(url=squad_url, out='data')

    wget.download(
        url='https://raw.githubusercontent.com/allenai/bi-att-flow/master/squad/evaluate-v1.1.py')


def download_releases_assets():
    g = Github()

    repo = g.get_repo('cdqa-suite/cdQA')

    headers = {
        'Accept': 'application/octet-stream'
    }

    # download models
    models = ['bert_qa_vGPU',
              'bert_qa_vCPU']

    for model in models:
        print('Downloading: {}'.format(model))
        release = repo.get_release(model)
        assets = release.get_assets()

        for asset in assets:
            print(asset.name, asset.url)
            if (os.path.splitext(asset.name)[1] == '.bin') or (os.path.splitext(asset.name)[1] == '.joblib') or (asset.name == 'bert_config.json'):
                directory = 'models'
                if not os.path.exists(directory):
                    os.makedirs(directory)
            else:
                directory = 'logs'
                if not os.path.exists(directory):
                    os.makedirs(directory)
            response = requests.get(asset.url, headers=headers)
            if not os.path.exists(os.path.join(directory, release.tag_name)):
                os.makedirs(os.path.join(directory, release.tag_name))
            with open(os.path.join(directory, release.tag_name, asset.name), 'wb') as handle:
                for block in response.iter_content(1024):
                    handle.write(block)

    # download datasets
    release = repo.get_release('bnpp_newsroom_v1.1')
    assets = release.get_assets()

    for asset in assets:
        response = requests.get(asset.url, headers=headers)
        directory = 'data'
        if not os.path.exists(os.path.join(directory, release.tag_name)):
            os.makedirs(os.path.join(directory, release.tag_name))
        with open(os.path.join(directory, release.tag_name, asset.name), 'wb') as handle:
            for block in response.iter_content(1024):
                handle.write(block)


if __name__ == '__main__':
    directory = 'data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    download_squad_assets()
    download_releases_assets()
