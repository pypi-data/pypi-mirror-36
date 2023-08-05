# -*- coding: utf-8 -*-

"""
Python page object patter realization for selenium library.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pagium.page import Page, PageElement, WebElement
from pagium.webdriver import Remote, Chrome, Firefox, PhantomJS, Opera, Safari


__version__ = '0.0.5'


__all__ = [
    'By',
    'Page',
    'PageElement',
    'WebElement',
    'Remote',
    'Chrome',
    'Firefox',
    'PhantomJS',
    'Opera',
    'Safari',
    'Keys',
]
