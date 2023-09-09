import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
import os
import sys
import io
from tqdm import tqdm

init()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

def validator():
    username = input('Input Username: ')
    url = 'https://github.com/CallMeDimas?tab=followers'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        checker = soup.find('span', class_='Link--secondary')
        text = checker.text
        if checker.text.lower() == username.lower():
            return checker.text
        else:
            print(f'{Fore.RED}[ ERROR ] - You Can`t Use This Program{Fore.RESET}')
            print('[---------------------------------------------]')
            print('    [INFO] How To Use This Program')
            print('    1. Follow My Github Pages')
            print('    2. Visit: https://github.com/CallMeDimas/')
            print('    3. Follow The Account')
            print('    4. Paste Your Github Username Here''')
            print('[---------------------------------------------]')
            return None

banner = f'''
███████╗ █████╗  ██████╗███████╗██████╗  ██████╗ ██╗    ██╗███╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║    ██║████╗  ██║
█████╗  ███████║██║     █████╗  ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔══╝  ██╔══██║██║     ██╔══╝  ██║  ██║██║   ██║██║███╗██║██║╚██╗██║
██║     ██║  ██║╚██████╗███████╗██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
'''

validated_username = validator()
if validated_username:
    Credit = f'''
    [---------------------------------------------]
    [ NAME     - FACEDOWN                         ]
    [ ABOUT    - Facebook Video Downloader Tools  ]
    [ AUTHOR   - https://github.com/CallMeDimas/  ]
    [ VERSION  - V.1.0.0                          ]
    [---------------------------------------------]

    [ INFO ]   - Welcome User {validated_username}
    [ INFO ]   - Thank You For Following My Github...
    '''
def print_with_banner(text: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.LIGHTBLUE_EX, banner, Fore.RESET)
    print(Credit)
    print(text)

def download_facebook_video(down_url: str):
    url = 'https://fdown.net/download.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    data = {'URLz': down_url}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        download = soup.find('a', id='hdlink')
        href = download['href']
        video_id = down_url.split('/')[-2]
        filename = f"{video_id}.mp4"
        video_response = requests.get(href, stream=True)
        if video_response.status_code == 200:
            total_size_in_bytes= int(video_response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(filename, 'wb') as f:
                for data in video_response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print_with_banner(f"{Fore.RED}[ERROR]{Fore.RESET} - Something went wrong")
            else:
                print_with_banner(f'{Fore.LIGHTGREEN_EX}[SUCCESS]{Fore.RESET} - Video downloaded successfully as {filename}')
        else:
            print_with_banner(f"{Fore.RED}[ERROR]{Fore.RESET} - Video download failed with status code: {video_response.status_code}")
    else:
        print_with_banner(f"{Fore.RED}[ERROR]{Fore.RESET} - Request failed with status code: {response.status_code}")

if __name__ == '__main__':
    if validated_username:
        while True:
            print_with_banner('')
            down_url = input(f'{Fore.LIGHTBLUE_EX}[INPUT]{Fore.RESET} - Facebook Video URL or type STOP to exit: ')
            if down_url.lower() == 'stop':
                print(f'{Fore.LIGHTGREEN_EX}[STOPPING]{Fore.RESET} - Thank You For Using This Program')
                break
            download_facebook_video(down_url)
