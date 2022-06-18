# -*- coding: utf-8 -*-
"""Vestaboard Module

A lightweight wrapper for Vestaboard

Board - Class
Installable - Class
"""
import requests
from vestaboard.formatter import Formatter
import vestaboard.vbUrls as vbUrls
import warnings

class Board:
  def __init__(self, installable=False, apiKey=False, apiSecret=False, subscriptionId=False):
    """
    Returns an instance of Board().

    Keyword arguments:
    installable - an instance of installable()
    apiKey - your Vestaboard API Key
    apiSecret - your Vestaboard API Secret
    subscriptionId - your Subscription ID (this can be obtained for you by creating a new installable() instance)
    """
    if installable and not isinstance(installable, Installable):
      raise ValueError(f'Expected the first argument passed to be an instance of Installable, but instead got {type(installable)}. If you are not trying to pass an Installable, specify the name of the arguments, or pass "None" as the first argument.')

    if not installable:  #check for cred file
      if (not apiKey or not apiSecret or not subscriptionId):
        try:
          creds = get_creds()
          if (len(creds) == 3):
            self.apiKey = creds[0]
            self.apiSecret = creds[1]
            self.subscriptionId = creds[2]
          elif (len(creds) < 3 or len(creds) > 3):
            raise ValueError('Credentials have been saved, but one or more are missing. Create a new installable and pass in saveCredentials=True, or pass in all three parameters when initializing a new Board.')
        except FileNotFoundError:
          raise ValueError('You must create an installable first or save credentials by passing saveCredentials=True into installable().')
      else:
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.subscriptionId = subscriptionId
    else:
      self.apiKey = installable.apiKey
      self.apiSecret = installable.apiSecret
      self.subscriptionId = installable.subscriptionId or subscriptionId

  def post(self, text):
    headers = {
        "X-Vestaboard-Api-Key" : self.apiKey,
        "X-Vestaboard-Api-Secret" : self.apiSecret
    }
    finalText = Formatter()._standard(text)
    requests.post(vbUrls.post.format(self.subscriptionId), headers=headers, json=finalText)

  def raw(self, charList: list, pad=None):
    """
    Posts already-formatted characters to the board.

    Keyword arguments:

    `charList` - a list of character lists

    `pad` - adds padding when list or character lists is less than 6. Valid options are `top`, `bottom`, and `center`.
    """
    base_filler = [0] * 22
    filler_needed = 6 - len(charList)
    for i, row in enumerate(charList):
      if not isinstance(row, list):
        raise ValueError(f'Nested items must be lists, not {type(row)}.')
      if len(row) != 22:
        raise ValueError(f'Nested lists must be exactly 22 characters long. Element at {i} is {len(row)} characters long. Use the Formatter().convertLine() function if you need to add padding to your row.')
      for j, char in enumerate(row):
        if not isinstance(char, int):
          raise ValueError(f'Nested lists must contain numbers only - check row {i} char {j} (0 indexed)')
    if len(charList) > 6:
      # warnings.warn doesn't work with f strings
      warning_message = f'The Vestaboard API accepts only 6 lines of characters; you\'ve passed in {len(charList)}. Only the first 6 will be shown.'
      warnings.warn(warning_message)
      del charList[6:]
    elif len(charList) < 6:
      if pad == 'below':
        for i in range(filler_needed):
          charList.append(base_filler)
      elif pad == 'above':
        for i in range(filler_needed):
          charList.insert(0, base_filler)
      else:
        if pad == None:
          # warnings.warn doesn't work with f strings
          warning_message = f'you provided a list with length {len(charList)}, which has been centered vertically on the board by default. Either provide a list with length 6, or set the "pad" option to suppress this warning.'
          warnings.warn(warning_message)
        while len(charList) < 6:
          charList.append(base_filler)
          if len(charList) < 6:
            charList.insert(0, base_filler)
    headers = {
        "X-Vestaboard-Api-Key" : self.apiKey,
        "X-Vestaboard-Api-Secret" : self.apiSecret
    }
    finalText = Formatter()._raw(charList)
    requests.post(vbUrls.post.format(self.subscriptionId), headers=headers, json=finalText)

class Installable:
  def __init__(self, apiKey=False, apiSecret=False, getSubscription=True, saveCredentials=True):
    """
    Returns an instance of Installable()

    You can pass this into an instance of Board() as the first keyword argument.
    Keyword arguments:
    apiKey: String (required) - your Vestaboard API Key
    apiSecret: String (required) - your Vestaboard API Secret
    getSubscripion: Bool (optional, default True) - If you already have your subscription ID, you may pass False into this method

    saveCredentials: Bool (options, default True) - Choose whether or not to store your API keys in the home directory
    """
    self.apiKey = apiKey
    self.apiSecret = apiSecret
    self.saveCredentials = saveCredentials
    if not apiKey or not apiSecret:
      raise ValueError('Installables must have an apiKey and apiSecret parameter.')
    if saveCredentials and apiKey and apiSecret:
      with open('./credentials.txt', 'w') as cred:
        cred.write(apiKey + '\n')
        cred.write(apiSecret + '\n')
        cred.close()
    if getSubscription:
      self.subscriptionId = self.get_subscriptions(saveCredentials)[0]['_id']
    else:
      self.subscriptionId = False

  def get_subscriptions(self, save=True):
    if not self.apiKey or not self.apiSecret:
      raise ValueError('There are no keys set. Call Installable(apiKey= apiSecret=) with your installable keys.')
    headers = {
      'X-Vestaboard-Api-Key': self.apiKey,
      'X-Vestaboard-Api-Secret': self.apiSecret
    }
    response = requests.get(vbUrls.subscription, headers=headers)
    if self.saveCredentials or save and response.status_code == 200:
      with open('./credentials.txt', 'a') as cred:
        cred.write(response.json()['subscriptions'][0]['_id'] + '\n')
        cred.close()

    print('Subscription id(s):', response.json()['subscriptions'])
    return response.json()['subscriptions']

def get_creds():
    with open('./credentials.txt', 'r') as cred:
      creds = cred.read().splitlines()
      return creds
