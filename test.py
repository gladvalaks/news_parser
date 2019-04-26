import sys
import requests
import pygame
import os
import pprint

def get_post(num, group):
    if group == 1:
        req = 'https://api.vk.com/method/wall.get'
        response = requests.get('https://api.vk.com/method/wall.get?owner_id=-112510789&count=20&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
        text = response.json()['response']['items'][num]['text']
    if group == 2:
        req = 'https://api.vk.com/method/wall.get'
        response = requests.get('https://api.vk.com/method/wall.get?owner_id=-29534144&count=20&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
        text = response.json()['response']['items'][num]['text']
    if group == 3:
        req = 'https://api.vk.com/method/wall.get'
        response = requests.get('https://api.vk.com/method/wall.get?owner_id=-145037861&count=20&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
        text = response.json()['response']['items'][num]['text']
    return text
