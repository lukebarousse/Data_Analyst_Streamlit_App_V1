import streamlit as st
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

class Title(object):
    """"
    Update title and favicon of each page
    ⚠️ IMPORTANT: Must call page_config() as first function in script 
    """
    def __init__(self):

        self.img = "images/luke_Favicon.png"
    
    def page_config(self, title):
        self.title = title
        st.set_page_config(page_title=self.title, page_icon=self.img)

class Footer:
    """"
    Creates a clickable footer image with link
    source: https://discuss.streamlit.io/t/st-footer/6447
    """

    def __init__(self):
        self.url = "https://serpapi.com/"
        self.img = "https://github.com/lukebarousse/Data_Analyst_Streamlit_App_V1/raw/main/images/SerpApi_V2.png"

    def image(self, src_as_string, **style):
        return img(src=src_as_string, style=styles(**style))

    def link(self, link, text, **style):
        return a(_href=link, _target="_blank", style=styles(**style))(text)

    def layout(self, *args):
        style = """
        <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stApp { bottom: 0px; }
        </style>
        """

        style_div = styles(
            position="fixed",
            right=0,
            bottom=0,
            margin=px(0, 100, 0, 0),
            text_align="center",
            opacity=1,
        )

        body = p()
        foot = div(
            style=style_div
        )(
            body
        )

        st.markdown(style, unsafe_allow_html=True)
        for arg in args:
            if isinstance(arg, str):
                body(arg)
            elif isinstance(arg, HtmlElement):
                body(arg)
        st.markdown(str(foot), unsafe_allow_html=True)

    def footer(self):
        myargs = [
            self.link(self.url, self.image(self.img,)),
        ]
        self.layout(*myargs)

