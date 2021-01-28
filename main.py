from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import mainthread
from kivy.logger import Logger

import threading

import requests

KV = '''
MDBoxLayout:
    orientation: "vertical"
    padding: "48dp"
    spacing: "40dp"
    
    MDGridLayout:
        size_hint: 1, .1
        cols: 3
        MDTextField:
            size: .8, 1
            hint_text: "URL"
            text: "https://www.google.com"
            id: url_text_field
        MDIconButton:
            icon: "delete-sweep"
            on_release: app.on_clear_url(root)
        MDRaisedButton:
            text: "Fetch"
            on_release: app.on_fetch(root.ids.url_text_field.text)
    ScrollView:
        size_hint: 1, .9
        MDGridLayout:
            adaptive_height: True
            cols: 1
            MDTextField:
                adaptive_height: True
                
                text_hint: "HTML response goes here"
                id: html_txt_field
'''

def on_http_request(**kwargs):
    url = kwargs["url"]
    app = kwargs["app"]
    Logger.info(f"APP: Retrieving from {url}")
    s = requests.get(url)
    Logger.info("App: Connected")
    app.update_html(s.text)
    s.close()

class Example(MDApp):
    
    def on_clear_url(self, root):
        root.ids.url_text_field.text = ""
    
    def build(self):
        return Builder.load_string(KV)
    
    def on_fetch(self, url):
        threading.Thread(target=on_http_request, kwargs={
            "url": url,
            "app": self
        }).start()
    
    @mainthread
    def update_html(self, html):
        self.root.ids.html_txt_field.text = html

Example().run()
