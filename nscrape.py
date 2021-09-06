#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import sys

if __name__ == "__main__":
    try:
        try:
            if sys.argv[1] is not None:
                link = sys.argv[1]
        except:
            link = input("Link: ")
        if link.startswith("'") and link.endswith("'") or link.startswith('"') and link.endswith('"'):
            link = link[1:-1]
        if "/" not in link[-1]:
            link = link + "/"
        if not link.endswith("video"):
            link = link + "video"

        req = requests.get(link)
        bsoup = BeautifulSoup(req.text, "html.parser")

        channel_name = bsoup.find('h1', class_='channel_name').contents[0].text
        print("Filename: ", f"{channel_name}_urls.txt")

        pagination = bsoup.find('li', class_='pages').contents[1]
        last_page = int(pagination.contents[len(pagination)-2].text)
        print("Total Pages: ", last_page)
        total_videos = int(bsoup.find('span', class_='count').contents[1].text)
        print("Total Videos: ", total_videos)
        video_urls = []
        count = 0

        for i in range(1, int(last_page) + 1):
            print("\nPage: ", i)
            if i == 1:
                url_elements = bsoup.find_all('h6', class_='title')
            else:
                newUrl = f"{link}?&page={i}"
                req = requests.get(newUrl)
                bsoup = BeautifulSoup(req.text, "html.parser")
                url_elements = bsoup.find_all('h6', class_='title')
            num_urls = len(url_elements)

            for url_element in url_elements:
                # An empty h6 title tag is on every page so another option would be to just remove the last url_elements
                # itself on every page
                try:
                    url = url_element.find('a')['href']
                    print(url)
                    video_urls.append(url)
                    count = count + 1
                except TypeError:
                    # print("Extra tag, Skipping...")
                    continue
        with open(f'{channel_name}_urls.txt', 'w') as file:
            for url in video_urls:
                file.write(url + '\n')
        print(f"\nScraped {count}/{total_videos}")
    except KeyboardInterrupt as k:
        exit("\nKeyboardInterrupt\nExiting...")