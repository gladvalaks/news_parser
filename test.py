import sys
import requests
import pygame
import os
import pprint

def get_post(num):
    req = 'https://api.vk.com/method/wall.get'
    response = requests.get('https://api.vk.com/method/wall.get?owner_id=-112510789&count=20&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
    text = response.json()['response']['items'][num]['text']
    return text
