#!/usr/bin/env python
# coding: utf-8
#Created by: Dominic Bashford

import unittest
from unittest import mock
from extractor import FeatureExtractor

class TestStringMethods(unittest.TestCase):
    def test_mention_extraction(self):
        fe = FeatureExtractor()
        fe.message = "@john"
        actual = fe._FeatureExtractor__extract_features("@"," ")
        expected = ["john"]
        self.assertEqual(expected, actual)
        
    def test_link_extraction(self):
        fe = FeatureExtractor()
        fe.message = "https://espn.com"
        actual = fe._FeatureExtractor__extract_links()
        expected = [{"url": "https://espn.com", "title": "ESPN: Serving sports fans. Anytime. Anywhere."}]
        self.assertEqual(expected, actual)          
    
    @mock.patch.object(FeatureExtractor,"_FeatureExtractor__get_html_title", return_value = str("x" * 250))
    def test_title_length(self, __get_html_title):
        fe = FeatureExtractor()
        fe.message = "https"
        actual = fe._FeatureExtractor__extract_links()
        x_filler = "x" * 200
        expected = [{'url': 'https', 'title': x_filler}]
        self.assertEqual(expected, actual) 
        
    def test_emoticon_extraction(self):
        fe = FeatureExtractor()
        fe.message = "(smile)"
        actual = fe._FeatureExtractor__extract_features("(",")")
        expected = ["smile"]
        self.assertEqual(expected, actual)
    
    def test_emoticon_length(self):
        fe = FeatureExtractor()
        x_filler = "x" * 16
        fe.message = "("+x_filler+")"
        actual = fe._FeatureExtractor__extract_features("(",")",15)
        expected = []
        self.assertEqual(expected, actual)
        
    def test_multi_feature_extraction(self):
        fe = FeatureExtractor()
        actual = fe.extract_content("(smile) @john @jane (laugh)")
        expected = """{"emoticons": ["smile", "laugh"], "mentions": ["john", "jane"], "words": 1}"""
        self.assertEqual(expected, actual)

