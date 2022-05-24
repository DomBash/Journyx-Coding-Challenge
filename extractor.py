#!/usr/bin/env python
# coding: utf-8
#Created by: Dominic Bashford
#Challenge given by: Journyx

import json
from urllib.request import Request, urlopen
import math
import sys

class FeatureExtractor:
    """A class to extract features from a message of type string.
    
    Attributes
    ----------
    message -- String to be parsed for features. Feature substrings will be deleted from this variable.
    message_original -- String to hold input message. Feature substrings will NOT be deleted from this variable.
        
    Methods
    -------
    extract_content(message) -- Returns a JSON string of all features extracted from the message.
    """
    
    def __init__(self):
        self.message = None
        self.message_original = None
        
    def extract_content(self, message):
        """Returns a JSON string of all features extracted from the message.
        
        Keyword Arguments
        ----------
        self -- This object.
        message -- String to be parsed for features. Features will be deleted from this variable.
            
        Returns
        -------
        json_content -- String that is JSON formatted.
        """
        
        self.message = message
        self.message_original = message
        content = {}
        
        emoticons = self.__extract_features("(",")", 15)
        mentions = self.__extract_features("@", " ")
        links = self.__extract_links()       
        
        words = len(" ".join(self.message.split()).split(" "))

        if emoticons:
            content["emoticons"] = emoticons
        if mentions:
            content["mentions"] = mentions
        if links:
            content["links"] = links

        content["words"] = words

        json_content = json.dumps(content)

        return json_content
    
    def __extract_features(self, delimeter_start, delimeter_end, max_length = math.inf):
        """Returns a list of features. Features are found using start and end delimeters."""
        features = []
        features_split = self.message.split(delimeter_start)
        num_features = len(features_split) - 1

        for i in range(num_features): 
            feature = features_split[i + 1].split(delimeter_end)[0]

            if len(feature) <= max_length:
                features.append(feature)
                self.message = self.message.replace(delimeter_start + feature + delimeter_end, "")

        return features

    def __extract_links(self):
        """Returns a list of url and title key value pairs. URLs are found "http" as delimiter."""
        links = []
        links_split = self.message.split("http")
        num_links = len(links_split) - 1

        for i in range(num_links):
            url = "http" + links_split[i + 1].split(' ')[0]
            title = self.__get_html_title(url).replace("&amp;", "&")[:200]
            links.append({"url": url, "title": title})
            self.message = self.message.replace(url, "")

        return links
    
    def __get_html_title(self, url):
        """Returns a string for the HTML title of the given URL"""
        try:
            request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(request).read()
            title = str(webpage).split("<title>")[1].split("</title>")[0]
        except:
            print("Title could not be retrieved.")
            title = "No title could be retrieved"

        return title

def main(argv):
    message = ' '.join(sys.argv[1:])
    fe = FeatureExtractor()
    json_content = fe.extract_content(message)
    return json_content

if __name__ == "__main__":
    print(main(sys.argv))

