#!/usr/bin/python
import streamlit as st
import pandas as pd
import openai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import json
import os
import time
import gc
import random
import speech_recognition as sr
from streamlit_star_rating import st_star_rating
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
from IPython.display import Audio
import base64

from email_validator import validate_email, EmailNotValidError

def vallid_email(email):
    try:
        validate_email(email, check_deliverability=False)
        return True
    except:
        return False

st.set_page_config(
    page_title="Hello",
    page_icon="https://www.squadstack.com/",
    layout="wide",
    initial_sidebar_state="collapsed"

)


def question_audio(txt):
    tts = gTTS(txt, lang='en',tld = "co.in")
    prompt_response_speech = "question.mp3"
    tts.save(prompt_response_speech)
    audio = Audio(prompt_response_speech, autoplay=True)
    return (audio)

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)
render_svg("""<svg width="216" height="48" viewBox="0 0 216 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M47.7131 36.9859L47.8066 36.8722L47.9001 36.7397L48.0123 36.5503C48.0123 36.5503 48.0123 36.5503 48.0123 36.4556V36.2851C48.0317 36.1089 48.0317 35.931 48.0123 35.7548V24.3909C48.0214 24.2901 48.0214 24.1886 48.0123 24.0878C48.021 24.0505 48.021 24.0115 48.0123 23.9742C47.9463 23.5539 47.7425 23.1684 47.4338 22.8798C47.1251 22.5912 46.7294 22.4163 46.3105 22.3832C45.5805 22.3496 44.8612 22.5701 44.2722 23.0083C38.662 25.8303 33.0519 28.6902 27.5353 31.5501C26.4588 32.173 25.2406 32.5006 24.0009 32.5006C22.7612 32.5006 21.5429 32.173 20.4665 31.5501C14.9873 28.5766 9.73242 25.9629 4.21578 23.1408L3.76697 22.9325V12.364C3.76449 11.8617 3.56509 11.381 3.21264 11.0276C2.86018 10.6741 2.38354 10.477 1.88758 10.4795C1.39161 10.482 0.916939 10.684 0.567991 11.0409C0.219043 11.3979 0.024399 11.8807 0.0268789 12.383L0.195183 24.2015C0.177098 24.3714 0.177098 24.5429 0.195183 24.7128C0.30509 25.1493 0.547021 25.54 0.8871 25.8303C1.27873 26.1598 1.71283 26.4338 2.17743 26.6447C7.78757 29.5425 13.1359 32.3267 18.7647 35.1108C20.4857 36.0468 22.4231 36.4981 24.3749 36.4177C25.7407 36.503 27.1024 36.1943 28.302 35.5275C33.7064 32.8002 39.0547 30.0539 44.4405 27.3265V34.4101L44.1226 34.5616C38.5124 37.3836 32.9023 40.2435 27.3857 43.1035C26.3543 43.7088 25.1835 44.0275 23.9915 44.0275C22.7996 44.0275 21.6287 43.7088 20.5974 43.1035C14.9872 40.1488 9.26491 37.251 3.54257 34.3532C2.73845 33.9366 1.99043 33.5388 1.11151 34.0881C0.828461 34.2457 0.588184 34.4716 0.41197 34.7458C0.235756 35.02 0.129048 35.334 0.101305 35.6599C0.0735622 35.9858 0.125641 36.3137 0.252924 36.6144C0.380208 36.915 0.578766 37.1793 0.830999 37.3836C1.24742 37.7018 1.70727 37.957 2.19613 38.1412C7.89977 41.039 13.6782 43.9368 19.4006 46.8157C20.7923 47.6597 22.3993 48.0682 24.0196 47.99C25.6303 48.0675 27.2303 47.687 28.6386 46.8914L46.1048 38.0844C46.5417 37.848 46.9661 37.5888 47.3765 37.3079L47.5074 37.2132L47.7131 36.9859Z" fill="#39CEA0"></path><path d="M27.8904 23.6143L45.9176 14.4663C46.3907 14.2634 46.8268 13.9818 47.208 13.633C47.4399 13.4867 47.6312 13.283 47.7638 13.0411C47.8964 12.7992 47.966 12.527 47.966 12.2504C47.966 11.9737 47.8964 11.7015 47.7638 11.4596C47.6312 11.2177 47.4399 11.014 47.208 10.8677C46.7396 10.5216 46.2385 10.2234 45.7119 9.97757C39.8587 7.02294 33.9493 4.06832 28.0774 1.03794C26.8239 0.356579 25.4233 0 24.0007 0C22.578 0 21.1775 0.356579 19.924 1.03794L2.32686 9.92075C1.95005 10.0934 1.58737 10.2961 1.24223 10.5268C-0.384712 11.5685 -0.328611 12.8754 1.24223 13.9739C1.57062 14.2057 1.91426 14.4145 2.27075 14.5989C8.1801 17.5535 14.1081 20.5839 20.0175 23.6143C21.2001 24.3555 22.5632 24.7482 23.9539 24.7482C25.3447 24.7482 26.7078 24.3555 27.8904 23.6143Z" fill="#162447"></path><path d="M75.4922 5.70852C75.402 4.86496 75.0221 4.20815 74.3524 3.73807C73.6892 3.26799 72.8263 3.03296 71.7638 3.03296C71.0168 3.03296 70.3761 3.14564 69.8416 3.37102C69.3072 3.5964 68.8983 3.90227 68.6149 4.28864C68.3316 4.675 68.1867 5.1161 68.1803 5.61193C68.1803 6.02405 68.2736 6.38144 68.4604 6.68409C68.6536 6.98674 68.9144 7.24432 69.2428 7.45682C69.5712 7.66288 69.935 7.83674 70.3342 7.97841C70.7335 8.12008 71.1359 8.23921 71.5416 8.3358L73.3962 8.79943C74.1431 8.9733 74.8611 9.20833 75.5502 9.50455C76.2456 9.80076 76.867 10.1742 77.4144 10.625C77.9681 11.0758 78.406 11.6199 78.728 12.2574C79.05 12.8949 79.2109 13.6419 79.2109 14.4983C79.2109 15.6574 78.9147 16.678 78.3223 17.5602C77.7299 18.436 76.8734 19.1218 75.753 19.6176C74.639 20.107 73.2899 20.3517 71.7058 20.3517C70.1668 20.3517 68.8306 20.1134 67.6973 19.6369C66.5704 19.1604 65.6882 18.465 65.0507 17.5506C64.4197 16.6362 64.0784 15.5222 64.0269 14.2085H67.5524C67.6039 14.8975 67.8164 15.4706 68.1899 15.9278C68.5634 16.385 69.0496 16.7263 69.6484 16.9517C70.2538 17.1771 70.9299 17.2898 71.6769 17.2898C72.456 17.2898 73.1386 17.1739 73.7246 16.942C74.317 16.7038 74.7806 16.3754 75.1155 15.9568C75.4503 15.5318 75.621 15.036 75.6274 14.4693C75.621 13.9542 75.4697 13.5292 75.1734 13.1943C74.8772 12.853 74.4619 12.5697 73.9274 12.3443C73.3994 12.1125 72.7812 11.9064 72.0729 11.7261L69.8223 11.1466C68.1931 10.728 66.9053 10.0938 65.9587 9.24375C65.0185 8.38731 64.5484 7.25076 64.5484 5.83409C64.5484 4.66856 64.864 3.64792 65.495 2.77216C66.1325 1.8964 66.9986 1.21705 68.0933 0.734091C69.188 0.244697 70.4276 0 71.8121 0C73.2159 0 74.4458 0.244697 75.5019 0.734091C76.5644 1.21705 77.3983 1.88996 78.0036 2.75284C78.6089 3.60928 78.9212 4.59451 78.9405 5.70852H75.4922Z" fill="#162447"></path><path d="M91.5533 25.6159V17.7148H91.4084C91.2281 18.0754 90.9673 18.4585 90.626 18.8642C90.2848 19.2635 89.834 19.6047 89.2738 19.8881C88.7135 20.1714 88.0084 20.3131 87.1584 20.3131C85.9929 20.3131 84.9497 20.0136 84.0289 19.4148C83.108 18.8159 82.3804 17.9466 81.8459 16.8068C81.3115 15.667 81.0442 14.2826 81.0442 12.6534C81.0442 11.0049 81.3147 9.61402 81.8556 8.48068C82.4029 7.34091 83.1402 6.48125 84.0675 5.90171C84.9948 5.31572 86.0283 5.02273 87.1681 5.02273C88.0374 5.02273 88.7522 5.17083 89.3124 5.46705C89.8726 5.75682 90.317 6.10777 90.6454 6.51989C90.9738 6.92557 91.2281 7.30871 91.4084 7.66932H91.6209V5.21591H95.0596V25.6159H91.5533ZM88.134 17.4443C88.8745 17.4443 89.5056 17.2447 90.0272 16.8455C90.5488 16.4398 90.9448 15.8763 91.2152 15.1551C91.4857 14.4339 91.6209 13.5936 91.6209 12.6341C91.6209 11.6746 91.4857 10.8407 91.2152 10.1324C90.9512 9.42405 90.5584 8.87349 90.0368 8.48068C89.5217 8.08788 88.8874 7.89148 88.134 7.89148C87.3548 7.89148 86.7045 8.09432 86.1829 8.5C85.6613 8.90568 85.2685 9.46591 85.0045 10.1807C84.7404 10.8955 84.6084 11.7133 84.6084 12.6341C84.6084 13.5614 84.7404 14.3888 85.0045 15.1165C85.2749 15.8377 85.6709 16.4076 86.1925 16.8261C86.7206 17.2383 87.3677 17.4443 88.134 17.4443Z" fill="#162447"></path><path d="M107.511 13.8125V5.21591H111.007V20.0523H107.617V17.4153H107.462C107.127 18.246 106.577 18.9254 105.811 19.4534C105.051 19.9814 104.114 20.2455 103 20.2455C102.027 20.2455 101.168 20.0297 100.421 19.5983C99.6803 19.1604 99.1007 18.5261 98.6822 17.6955C98.2636 16.8583 98.0543 15.8474 98.0543 14.6625V5.21591H101.551V14.1216C101.551 15.0617 101.809 15.8087 102.324 16.3625C102.839 16.9163 103.515 17.1932 104.352 17.1932C104.867 17.1932 105.366 17.0676 105.849 16.8165C106.332 16.5653 106.728 16.1919 107.037 15.696C107.353 15.1938 107.511 14.5659 107.511 13.8125Z" fill="#162447"></path><path d="M118.274 20.3517C117.334 20.3517 116.487 20.1843 115.733 19.8494C114.986 19.5081 114.394 19.0059 113.956 18.3426C113.525 17.6794 113.309 16.8616 113.309 15.8892C113.309 15.0521 113.463 14.3598 113.773 13.8125C114.082 13.2652 114.503 12.8273 115.038 12.4989C115.572 12.1705 116.174 11.9225 116.844 11.7551C117.52 11.5813 118.219 11.4557 118.94 11.3784C119.81 11.2883 120.515 11.2078 121.056 11.1369C121.596 11.0597 121.989 10.9438 122.234 10.7892C122.485 10.6282 122.611 10.3803 122.611 10.0455V9.9875C122.611 9.25985 122.395 8.6964 121.963 8.29716C121.532 7.89792 120.911 7.6983 120.099 7.6983C119.243 7.6983 118.563 7.88504 118.061 8.25852C117.565 8.63201 117.231 9.07311 117.057 9.58182L113.792 9.11818C114.049 8.21667 114.474 7.46326 115.067 6.85795C115.659 6.24621 116.384 5.78902 117.24 5.48636C118.097 5.17727 119.043 5.02273 120.08 5.02273C120.795 5.02273 121.506 5.10644 122.215 5.27386C122.923 5.44129 123.57 5.71818 124.156 6.10455C124.742 6.48447 125.212 7.00284 125.566 7.65966C125.927 8.31648 126.107 9.1375 126.107 10.1227V20.0523H122.746V18.0142H122.63C122.417 18.4263 122.118 18.8127 121.732 19.1733C121.352 19.5275 120.872 19.814 120.292 20.033C119.719 20.2455 119.046 20.3517 118.274 20.3517ZM119.182 17.7824C119.884 17.7824 120.492 17.6439 121.007 17.367C121.522 17.0837 121.918 16.7102 122.195 16.2466C122.479 15.783 122.62 15.2775 122.62 14.7301V12.9818C122.511 13.072 122.324 13.1557 122.06 13.233C121.802 13.3102 121.513 13.3778 121.191 13.4358C120.869 13.4938 120.55 13.5453 120.235 13.5903C119.919 13.6354 119.645 13.6741 119.413 13.7063C118.892 13.7771 118.425 13.893 118.013 14.054C117.601 14.215 117.276 14.4403 117.037 14.7301C116.799 15.0134 116.68 15.3805 116.68 15.8313C116.68 16.4752 116.915 16.9614 117.385 17.2898C117.855 17.6182 118.454 17.7824 119.182 17.7824Z" fill="#162447"></path><path d="M134.53 20.3131C133.365 20.3131 132.322 20.0136 131.401 19.4148C130.48 18.8159 129.752 17.9466 129.218 16.8068C128.683 15.667 128.416 14.2826 128.416 12.6534C128.416 11.0049 128.687 9.61402 129.228 8.48068C129.775 7.34091 130.512 6.48125 131.44 5.90171C132.367 5.31572 133.4 5.02273 134.54 5.02273C135.409 5.02273 136.124 5.17083 136.684 5.46705C137.245 5.75682 137.689 6.10777 138.017 6.51989C138.346 6.92557 138.6 7.30871 138.78 7.66932H138.925V0.270455H142.432V20.0523H138.993V17.7148H138.78C138.6 18.0754 138.339 18.4585 137.998 18.8642C137.657 19.2635 137.206 19.6047 136.646 19.8881C136.086 20.1714 135.38 20.3131 134.53 20.3131ZM135.506 17.4443C136.247 17.4443 136.878 17.2447 137.399 16.8455C137.921 16.4398 138.317 15.8763 138.587 15.1551C138.858 14.4339 138.993 13.5936 138.993 12.6341C138.993 11.6746 138.858 10.8407 138.587 10.1324C138.323 9.42405 137.93 8.87349 137.409 8.48068C136.894 8.08788 136.259 7.89148 135.506 7.89148C134.727 7.89148 134.076 8.09432 133.555 8.5C133.033 8.90568 132.64 9.46591 132.376 10.1807C132.112 10.8955 131.98 11.7133 131.98 12.6341C131.98 13.5614 132.112 14.3888 132.376 15.1165C132.647 15.8377 133.043 16.4076 133.565 16.8261C134.093 17.2383 134.74 17.4443 135.506 17.4443Z" fill="#162447"></path><path d="M156.464 5.70852C156.374 4.86496 155.994 4.20815 155.324 3.73807C154.661 3.26799 153.798 3.03296 152.736 3.03296C151.989 3.03296 151.348 3.14564 150.814 3.37102C150.279 3.5964 149.87 3.90227 149.587 4.28864C149.304 4.675 149.159 5.1161 149.152 5.61193C149.152 6.02405 149.246 6.38144 149.432 6.68409C149.626 6.98674 149.886 7.24432 150.215 7.45682C150.543 7.66288 150.907 7.83674 151.306 7.97841C151.706 8.12008 152.108 8.23921 152.514 8.3358L154.368 8.79943C155.115 8.9733 155.833 9.20833 156.522 9.50455C157.218 9.80076 157.839 10.1742 158.386 10.625C158.94 11.0758 159.378 11.6199 159.7 12.2574C160.022 12.8949 160.183 13.6419 160.183 14.4983C160.183 15.6574 159.887 16.678 159.294 17.5602C158.702 18.436 157.846 19.1218 156.725 19.6176C155.611 20.107 154.262 20.3517 152.678 20.3517C151.139 20.3517 149.803 20.1134 148.669 19.6369C147.542 19.1604 146.66 18.465 146.023 17.5506C145.392 16.6362 145.05 15.5222 144.999 14.2085H148.524C148.576 14.8975 148.789 15.4706 149.162 15.9278C149.535 16.385 150.022 16.7263 150.621 16.9517C151.226 17.1771 151.902 17.2898 152.649 17.2898C153.428 17.2898 154.111 17.1739 154.697 16.942C155.289 16.7038 155.753 16.3754 156.088 15.9568C156.422 15.5318 156.593 15.036 156.599 14.4693C156.593 13.9542 156.442 13.5292 156.146 13.1943C155.849 12.853 155.434 12.5697 154.899 12.3443C154.371 12.1125 153.753 11.9064 153.045 11.7261L150.794 11.1466C149.165 10.728 147.877 10.0938 146.931 9.24375C145.991 8.38731 145.521 7.25076 145.521 5.83409C145.521 4.66856 145.836 3.64792 146.467 2.77216C147.105 1.8964 147.971 1.21705 149.065 0.734091C150.16 0.244697 151.4 0 152.784 0C154.188 0 155.418 0.244697 156.474 0.734091C157.536 1.21705 158.37 1.88996 158.976 2.75284C159.581 3.60928 159.893 4.59451 159.913 5.70852H156.464Z" fill="#162447"></path><path d="M170.033 5.21591V7.92045H161.504V5.21591H170.033ZM163.61 1.66136H167.107V15.5898C167.107 16.0599 167.177 16.4205 167.319 16.6716C167.467 16.9163 167.66 17.0837 167.899 17.1739C168.137 17.264 168.401 17.3091 168.691 17.3091C168.91 17.3091 169.109 17.293 169.29 17.2608C169.476 17.2286 169.618 17.1996 169.715 17.1739L170.304 19.9074C170.117 19.9718 169.85 20.0426 169.502 20.1199C169.161 20.1972 168.742 20.2422 168.246 20.2551C167.371 20.2809 166.582 20.1489 165.88 19.8591C165.178 19.5629 164.621 19.1057 164.209 18.4875C163.803 17.8693 163.604 17.0966 163.61 16.1693V1.66136Z" fill="#162447"></path><path d="M176.629 20.3517C175.688 20.3517 174.842 20.1843 174.088 19.8494C173.341 19.5081 172.749 19.0059 172.311 18.3426C171.879 17.6794 171.664 16.8616 171.664 15.8892C171.664 15.0521 171.818 14.3598 172.127 13.8125C172.436 13.2652 172.858 12.8273 173.393 12.4989C173.927 12.1705 174.529 11.9225 175.199 11.7551C175.875 11.5813 176.574 11.4557 177.295 11.3784C178.164 11.2883 178.869 11.2078 179.41 11.1369C179.951 11.0597 180.344 10.9438 180.589 10.7892C180.84 10.6282 180.965 10.3803 180.965 10.0455V9.9875C180.965 9.25985 180.75 8.6964 180.318 8.29716C179.887 7.89792 179.265 7.6983 178.454 7.6983C177.598 7.6983 176.918 7.88504 176.416 8.25852C175.92 8.63201 175.585 9.07311 175.411 9.58182L172.147 9.11818C172.404 8.21667 172.829 7.46326 173.422 6.85795C174.014 6.24621 174.739 5.78902 175.595 5.48636C176.451 5.17727 177.398 5.02273 178.435 5.02273C179.15 5.02273 179.861 5.10644 180.569 5.27386C181.278 5.44129 181.925 5.71818 182.511 6.10455C183.097 6.48447 183.567 7.00284 183.921 7.65966C184.282 8.31648 184.462 9.1375 184.462 10.1227V20.0523H181.101V18.0142H180.985C180.772 18.4263 180.473 18.8127 180.086 19.1733C179.707 19.5275 179.227 19.814 178.647 20.033C178.074 20.2455 177.401 20.3517 176.629 20.3517ZM177.536 17.7824C178.238 17.7824 178.847 17.6439 179.362 17.367C179.877 17.0837 180.273 16.7102 180.55 16.2466C180.833 15.783 180.975 15.2775 180.975 14.7301V12.9818C180.866 13.072 180.679 13.1557 180.415 13.233C180.157 13.3102 179.868 13.3778 179.546 13.4358C179.224 13.4938 178.905 13.5453 178.589 13.5903C178.274 13.6354 178 13.6741 177.768 13.7063C177.247 13.7771 176.78 13.893 176.368 14.054C175.956 14.215 175.63 14.4403 175.392 14.7301C175.154 15.0134 175.035 15.3805 175.035 15.8313C175.035 16.4752 175.27 16.9614 175.74 17.2898C176.21 17.6182 176.809 17.7824 177.536 17.7824Z" fill="#162447"></path><path d="M193.851 20.342C192.37 20.342 191.098 20.0169 190.036 19.3665C188.98 18.7161 188.165 17.8178 187.592 16.6716C187.025 15.5189 186.742 14.1924 186.742 12.692C186.742 11.1852 187.032 9.85549 187.611 8.70284C188.191 7.54375 189.009 6.64224 190.065 5.9983C191.127 5.34792 192.383 5.02273 193.832 5.02273C195.036 5.02273 196.102 5.24489 197.029 5.68921C197.963 6.12708 198.706 6.74849 199.26 7.55341C199.814 8.3519 200.13 9.28561 200.207 10.3545H196.865C196.73 9.63977 196.408 9.04413 195.899 8.56761C195.397 8.08466 194.724 7.84318 193.88 7.84318C193.165 7.84318 192.538 8.03636 191.997 8.42273C191.456 8.80265 191.034 9.35 190.731 10.0648C190.435 10.7795 190.287 11.636 190.287 12.6341C190.287 13.6451 190.435 14.5144 190.731 15.242C191.027 15.9633 191.443 16.5203 191.977 16.9131C192.518 17.2994 193.152 17.4926 193.88 17.4926C194.395 17.4926 194.856 17.396 195.261 17.2028C195.674 17.0032 196.018 16.7167 196.295 16.3432C196.572 15.9697 196.762 15.5157 196.865 14.9813H200.207C200.123 16.0309 199.814 16.9614 199.28 17.7727C198.745 18.5777 198.017 19.2087 197.097 19.6659C196.176 20.1167 195.094 20.342 193.851 20.342Z" fill="#162447"></path><path d="M205.667 15.3966L205.657 11.1756H206.218L211.55 5.21591H215.635L209.077 12.5182H208.352L205.667 15.3966ZM202.48 20.0523V0.270455H205.976V20.0523H202.48ZM211.791 20.0523L206.961 13.3006L209.318 10.8375L215.973 20.0523H211.791Z" fill="#162447"></path><path d="M64.0269 47.3614V32.8159H69.2115C70.3431 32.8159 71.2806 33.0219 72.024 33.4338C72.7674 33.8457 73.3237 34.4092 73.693 35.1242C74.0624 35.8344 74.247 36.6346 74.247 37.5247C74.247 38.4196 74.06 39.2245 73.6859 39.9395C73.3166 40.6497 72.7579 41.2132 72.0098 41.6298C71.2664 42.0418 70.3313 42.2477 69.2044 42.2477H65.6391V40.3869H69.0055C69.7205 40.3869 70.3005 40.2638 70.7456 40.0176C71.1907 39.7667 71.5174 39.4258 71.7257 38.9949C71.9341 38.564 72.0382 38.074 72.0382 37.5247C72.0382 36.9755 71.9341 36.4878 71.7257 36.0617C71.5174 35.6355 71.1883 35.3017 70.7385 35.0602C70.2934 34.8188 69.7063 34.698 68.9771 34.698H66.2215V47.3614H64.0269Z" fill="#48526D"></path><path d="M79.7264 47.6029C79.0351 47.6029 78.4101 47.475 77.8514 47.2193C77.2927 46.9589 76.85 46.5825 76.5233 46.0901C76.2013 45.5976 76.0403 44.9939 76.0403 44.279C76.0403 43.6635 76.1587 43.1568 76.3955 42.7591C76.6322 42.3614 76.9518 42.0465 77.3543 41.8145C77.7567 41.5825 78.2065 41.4073 78.7037 41.2889C79.2009 41.1706 79.7075 41.0806 80.2236 41.019C80.877 40.9433 81.4073 40.8817 81.8145 40.8344C82.2217 40.7823 82.5176 40.6994 82.7023 40.5858C82.8869 40.4722 82.9793 40.2875 82.9793 40.0318V39.9821C82.9793 39.3618 82.8041 38.8813 82.4537 38.5404C82.1081 38.1994 81.592 38.029 80.9054 38.029C80.1904 38.029 79.627 38.1876 79.2151 38.5048C78.8079 38.8173 78.5261 39.1654 78.3699 39.5489L76.3742 39.0943C76.6109 38.4314 76.9565 37.8964 77.4111 37.4892C77.8704 37.0773 78.3983 36.779 78.9949 36.5943C79.5915 36.4049 80.2189 36.3102 80.877 36.3102C81.3126 36.3102 81.7743 36.3623 82.2619 36.4665C82.7544 36.5659 83.2136 36.7506 83.6398 37.0205C84.0707 37.2903 84.4234 37.6762 84.698 38.1781C84.9726 38.6753 85.11 39.3216 85.11 40.1171V47.3614H83.0361V45.8699H82.9509C82.8136 46.1445 82.6076 46.4144 82.333 46.6796C82.0583 46.9447 81.7056 47.1649 81.2747 47.3401C80.8439 47.5153 80.3278 47.6029 79.7264 47.6029ZM80.1881 45.8983C80.7752 45.8983 81.2771 45.7823 81.6938 45.5503C82.1152 45.3183 82.4348 45.0153 82.6526 44.6412C82.8751 44.2624 82.9864 43.8576 82.9864 43.4267V42.0205C82.9106 42.0962 82.7638 42.1672 82.546 42.2335C82.333 42.2951 82.0891 42.3495 81.8145 42.3969C81.5399 42.4395 81.2724 42.4797 81.0119 42.5176C80.7515 42.5508 80.5337 42.5792 80.3585 42.6029C79.9466 42.6549 79.5702 42.7425 79.2293 42.8656C78.8931 42.9887 78.6232 43.1663 78.4196 43.3983C78.2207 43.6256 78.1213 43.9286 78.1213 44.3074C78.1213 44.833 78.3154 45.2307 78.7037 45.5006C79.092 45.7657 79.5868 45.8983 80.1881 45.8983Z" fill="#48526D"></path><path d="M87.9384 47.3614V36.4523H89.991V38.1852H90.1046C90.3035 37.5981 90.6539 37.1365 91.1558 36.8003C91.6624 36.4594 92.2353 36.2889 92.8745 36.2889C93.0071 36.2889 93.1633 36.2937 93.3433 36.3031C93.5279 36.3126 93.6723 36.3244 93.7765 36.3386V38.3699C93.6913 38.3462 93.5398 38.3202 93.322 38.2918C93.1042 38.2586 92.8863 38.2421 92.6685 38.2421C92.1667 38.2421 91.7192 38.3486 91.3262 38.5617C90.938 38.77 90.6302 39.0612 90.4029 39.4352C90.1756 39.8046 90.062 40.226 90.062 40.6994V47.3614H87.9384Z" fill="#48526D"></path><path d="M101.351 36.4523V38.1568H95.3923V36.4523H101.351ZM96.9903 33.8386H99.1139V44.1582C99.1139 44.5702 99.1754 44.8803 99.2985 45.0886C99.4216 45.2922 99.5802 45.4319 99.7744 45.5077C99.9732 45.5787 100.189 45.6142 100.421 45.6142C100.591 45.6142 100.74 45.6024 100.868 45.5787C100.996 45.555 101.095 45.5361 101.166 45.5219L101.55 47.2761C101.427 47.3235 101.252 47.3708 101.024 47.4182C100.797 47.4703 100.513 47.4987 100.172 47.5034C99.6134 47.5129 99.0926 47.4135 98.6096 47.2051C98.1266 46.9968 97.736 46.6748 97.4377 46.2392C97.1394 45.8036 96.9903 45.2567 96.9903 44.5986V33.8386Z" fill="#48526D"></path><path d="M105.824 40.8841V47.3614H103.7V36.4523H105.739V38.2279H105.873C106.124 37.6502 106.517 37.1862 107.052 36.8358C107.592 36.4854 108.272 36.3102 109.091 36.3102C109.834 36.3102 110.485 36.4665 111.044 36.779C111.603 37.0868 112.036 37.546 112.344 38.1568C112.651 38.7676 112.805 39.5228 112.805 40.4225V47.3614H110.682V40.6781C110.682 39.8874 110.476 39.2695 110.064 38.8244C109.652 38.3746 109.086 38.1497 108.366 38.1497C107.874 38.1497 107.436 38.2563 107.052 38.4693C106.674 38.6824 106.373 38.9949 106.15 39.4068C105.933 39.814 105.824 40.3064 105.824 40.8841Z" fill="#48526D"></path><path d="M120.355 47.5815C119.28 47.5815 118.355 47.3519 117.578 46.8926C116.806 46.4286 116.21 45.7776 115.788 44.9395C115.372 44.0967 115.163 43.1095 115.163 41.9779C115.163 40.8604 115.372 39.8756 115.788 39.0233C116.21 38.171 116.797 37.5058 117.55 37.0276C118.307 36.5493 119.193 36.3102 120.206 36.3102C120.821 36.3102 121.418 36.412 121.996 36.6156C122.573 36.8192 123.092 37.1388 123.551 37.5744C124.01 38.01 124.373 38.5759 124.638 39.2719C124.903 39.9632 125.035 40.8036 125.035 41.7932V42.546H116.364V40.9551H122.954C122.954 40.3964 122.841 39.9016 122.614 39.4707C122.386 39.0351 122.067 38.6919 121.655 38.4409C121.248 38.19 120.769 38.0645 120.22 38.0645C119.623 38.0645 119.103 38.2113 118.658 38.5048C118.217 38.7937 117.876 39.1725 117.635 39.6412C117.398 40.1052 117.28 40.6095 117.28 41.154V42.3969C117.28 43.1261 117.408 43.7463 117.663 44.2577C117.924 44.769 118.286 45.1597 118.75 45.4296C119.214 45.6947 119.756 45.8273 120.376 45.8273C120.779 45.8273 121.146 45.7705 121.477 45.6568C121.809 45.5385 122.095 45.3633 122.337 45.1313C122.578 44.8993 122.763 44.6128 122.89 44.2719L124.9 44.6341C124.739 45.226 124.451 45.7444 124.034 46.1895C123.622 46.6298 123.104 46.9731 122.479 47.2193C121.858 47.4608 121.15 47.5815 120.355 47.5815Z" fill="#48526D"></path><path d="M127.392 47.3614V36.4523H129.444V38.1852H129.558C129.757 37.5981 130.107 37.1365 130.609 36.8003C131.116 36.4594 131.688 36.2889 132.328 36.2889C132.46 36.2889 132.616 36.2937 132.796 36.3031C132.981 36.3126 133.125 36.3244 133.23 36.3386V38.3699C133.144 38.3462 132.993 38.3202 132.775 38.2918C132.557 38.2586 132.339 38.2421 132.122 38.2421C131.62 38.2421 131.172 38.3486 130.779 38.5617C130.391 38.77 130.083 39.0612 129.856 39.4352C129.629 39.8046 129.515 40.226 129.515 40.6994V47.3614H127.392Z" fill="#48526D"></path><path d="M143.242 39.1156L141.317 39.4565C141.237 39.2103 141.109 38.976 140.934 38.7534C140.763 38.5309 140.531 38.3486 140.238 38.2065C139.944 38.0645 139.577 37.9935 139.137 37.9935C138.536 37.9935 138.034 38.1284 137.631 38.3983C137.229 38.6635 137.028 39.0067 137.028 39.4281C137.028 39.7927 137.163 40.0863 137.432 40.3088C137.702 40.5314 138.138 40.7136 138.739 40.8557L140.472 41.2534C141.476 41.4854 142.224 41.8429 142.716 42.3259C143.209 42.8088 143.455 43.4362 143.455 44.208C143.455 44.8614 143.266 45.4438 142.887 45.9551C142.513 46.4618 141.99 46.8595 141.317 47.1483C140.65 47.4371 139.876 47.5815 138.995 47.5815C137.773 47.5815 136.777 47.3211 136.005 46.8003C135.233 46.2747 134.76 45.529 134.584 44.5631L136.637 44.2506C136.765 44.7856 137.028 45.1904 137.425 45.4651C137.823 45.735 138.341 45.8699 138.981 45.8699C139.677 45.8699 140.233 45.7255 140.65 45.4367C141.066 45.1431 141.275 44.7856 141.275 44.3642C141.275 44.0233 141.147 43.7368 140.891 43.5048C140.64 43.2728 140.254 43.0976 139.734 42.9793L137.887 42.5744C136.869 42.3424 136.116 41.9731 135.628 41.4665C135.145 40.9599 134.904 40.3183 134.904 39.5418C134.904 38.8978 135.084 38.3344 135.444 37.8514C135.804 37.3685 136.301 36.9921 136.935 36.7222C137.57 36.4475 138.297 36.3102 139.116 36.3102C140.295 36.3102 141.223 36.5659 141.9 37.0773C142.577 37.5839 143.024 38.2634 143.242 39.1156Z" fill="#48526D"></path></svg>""")
st.title('Practice Playgound')



if 'QB_name' not in st.session_state:
    st.session_state.QB_name = ''

player_email = st.text_input("Agent Email")

key_col1, key_col2, key_col3 = st.columns(3)

with key_col2:
    token_businessbot = st.text_input("KEY2")
with key_col3:
    creds_businessbot = st.text_input("KEY3")


@st.cache_data
def google_creds_login():
    json_obj = json.loads(token_businessbot)
    with open('token_businessbot.json', 'w') as outfile:
        json.dump(json_obj, outfile)

    json_obj = json.loads(creds_businessbot)
    with open('creds_businessbot.json', 'w') as outfile:
        json.dump(json_obj, outfile)

    SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
    try:
        creds = None
        if os.path.exists('token_businessbot.json'):
            print("Credentials Reading...")
            creds = Credentials.from_authorized_user_file('token_businessbot.json', SCOPES)
            print("Reading Done.")
        if not creds:
            print("Credentials Creating...")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('creds_businessbot.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('creds_businessbot.json', 'w') as token:
                token.write(creds.to_json())
            print("Creating Done.")
        return creds
    except Exception as e:
        print("There is an Exception in googleSheetCredsLogin Function:", e)

creds = google_creds_login()

@st.cache_data
def google_sheet_action_sub(SPREADSHEET_ID, RANGE_NAME, action, df=None, columns=False):
    if action == 'read':
        print("Google Sheet Reading...")
        service = build('sheets', 'v4', credentials=creds)
        final_df = pd.DataFrame(service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute().get('values', []))
        if columns:
            final_df.rename(columns=final_df.iloc[0], inplace=True)
            final_df.drop(final_df.index[0], inplace=True)
        return final_df

    elif action == 'clear':
        body = {}
        print("Google Sheet Deleting...")
        service = build('sheets', 'v4', credentials=creds)
        result = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, body=body).execute()
        return result

    elif action == 'sheet_name':
        # Check if the sheet exists
        service = build('sheets', 'v4', credentials=creds)
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_titles = [sheet['properties']['title'] for sheet in sheet_metadata['sheets'] if sheet['properties']['title'] != 'Answers']
        return sheet_titles
    
    elif action == 'write':
        # Check if the sheet exists
        service = build('sheets', 'v4', credentials=creds)
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_titles = [sheet['properties']['title'] for sheet in sheet_metadata['sheets']]
        
        sheet_name = RANGE_NAME.split('!')[0]
        if sheet_name not in sheet_titles:
            # Create the sheet if it doesn't exist
            requests = [ { 'addSheet': { 'properties': { 'title': sheet_name } } } ]
            service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={'requests': requests}).execute()
        if columns:
            row_df = pd.DataFrame([pd.Series([str(i) for i in df.columns])])
            row_df.columns = df.columns

            df = pd.concat([row_df, df], ignore_index=True)
            df = df.fillna("")
        values = df.values.tolist()
        body = {"values": values}
        print("Google Sheet Writing...")
        service = build('sheets', 'v4', credentials=creds)
        result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption='USER_ENTERED', body=body).execute()
        return result

    elif action == 'append':
        if columns:
            row_df = pd.DataFrame([pd.Series([str(i) for i in df.columns])])
            row_df.columns = df.columns
            df = pd.concat([row_df, df], ignore_index=True)
            df = df.fillna("")
        values = df.values.tolist()
        body = {"values": values}
        print("Google Sheet Writing...")
        service = build('sheets', 'v4', credentials=creds)
        result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption='USER_ENTERED', body=body).execute()
        return result

    else:
        print("Incorrect action. Must be read|write|append|clear.")
        return 0


@st.cache_data
def google_sheet_action(SPREADSHEET_ID, RANGE_NAME, action, df=None, columns=False):
    retry = 0
    while retry < 5:
        try:
            return google_sheet_action_sub(SPREADSHEET_ID, RANGE_NAME, action, df, columns)
        except Exception as e:
            if (('Unable to parse range:' in str(e)) or (('indexer is out-of-bounds' in str(e)))):
                st.write('this QB does not exits'+st.session_state.QB_name,e)
                return pd.DataFrame()
            print(e)
            retry += 1
            time.sleep(30)

@st.cache_data
def get_df(QB_name):
    try:
        return google_sheet_action('1C0i6OaBYxdf-6jhlWTsMHk4FSkEd_oGEKzUJ63mvBj8',st.session_state.QB_name+'!A:C','read',columns=True)
    except Exception as e:
        st.write(e)
        return pd.DataFrame()
    

sheet_name = google_sheet_action('1C0i6OaBYxdf-6jhlWTsMHk4FSkEd_oGEKzUJ63mvBj8',st.session_state.QB_name+'!A:C','sheet_name',columns=True)

def reset():
    for key in st.session_state.keys():
        del st.session_state[key]

with key_col1:
    st.session_state.QB_name = st.selectbox("QB Name",sheet_name,on_change=reset)

df = get_df(st.session_state.QB_name)

def rn():
    return random.randint(0, 9999999999999999999999999999999)


if 'questions' not in st.session_state:
    all_questions = list(df['Questions'])
    random_questions = random.sample(all_questions, k=4)
    st.session_state.questions = random_questions

if 'answers' not in st.session_state :
    st.session_state.answers = {}

def psude():
    pass

if 'old_rec' not in st.session_state:
    st.session_state.old_rec = ''

if 'Start' not in st.session_state:
    st.session_state.Start = False

if (not st.session_state.Start) and st.button('Start Practice'):
    if vallid_email(player_email) == False:
        st.warning('Invalid email. Please enter a valid email address.')
    elif str(token_businessbot) == '' or str(creds_businessbot) == '':
        st.warning('Please enter valid token and credentials for the practice.')
    elif str(st.session_state.QB_name) == '':
        st.warning('Please enter the name of the QB.')
    else:
        st.session_state.Start = True
        psude()

st.divider()

if st.session_state.Start:
    info_placeholder = st.empty()
    q_placeholder = st.empty()
    a_placeholder = st.empty()
    speak_placeholder = st.empty()
    question_audio_placeholder = st.empty()
    if 'idx' not in st.session_state:
        st.session_state.idx = 0



    next_btn_state = False
    submit_btn_state = False

    info_placeholder.subheader('Question No. '+str((st.session_state.idx)+1)+' out of '+str(len(st.session_state.questions)))


    if ((st.session_state.idx)+1) >= len(st.session_state.questions):
        st.write(st.session_state.answers)
        st.session_state.stars = st_star_rating("Rate your response againest ideal Answer", maxValue=5, defaultValue=st.session_state.stars)
        st.session_state.feedback = st.text_input('Feedback (optional)')
        st.session_state.btn_txt = 'Submit'
        next_btn_state = True
    elif ((st.session_state.idx)+1) < len(st.session_state.questions):
        st.session_state.btn_txt = 'Next'
        submit_btn_state = True

    if not next_btn_state:
        st.session_state.audio_data = audio_recorder(energy_threshold=100, pause_threshold=100,icon_name='microphone',icon_size='3x',key = 1)
        q_placeholder.text('Current Question: '+st.session_state.questions[st.session_state.idx])
        a_placeholder.subheader('Your Answer')
    else:
        q_placeholder.text('')
        info_placeholder.text('')
    st.caption('Click the mic to start/stop recording. You can record any number of times, give your best effort!')
    if st.session_state.audio_data and str(st.session_state.audio_data)!= st.session_state.old_rec:
        audio_file_path = "temp_audio.wav"
        with open(audio_file_path, "wb") as f:
            f.write(st.session_state.audio_data)
        
        st.audio(audio_file_path, format="audio/wav")
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)
            try:
                transcription = r.recognize_google(audio)
            except sr.UnknownValueError:
                transcription = "Unable to transcribe audio."
        st.write(transcription)
        # if st.session_state.idx < len(st.session_state.questions):
        ele = st.session_state.questions[st.session_state.idx]
        
        q_placeholder.text('Current Question: '+ele)
        st.session_state.answers[ele] = {'Your answer':transcription,"Ideal Answser":df.iloc[st.session_state.idx,1]}    
        st.session_state.old_rec = str(st.session_state.audio_data)


    if 'stars' not in st.session_state:
        st.session_state.stars = 0


    if st.session_state.idx < len(st.session_state.questions):
        q_placeholder.text('Current Question: '+st.session_state.questions[st.session_state.idx])

    if 'btn_txt' not in st.session_state:
        st.session_state.btn_txt = 'Next Question'

    if 'submit_pressed' not in st.session_state:
        st.session_state.submit_pressed = False

    st.divider()
    if not next_btn_state:
        if st.button("Next Question",disabled=next_btn_state):
            question_audio_placeholder.text = ''
            if st.session_state.idx < (len(st.session_state.questions)-1):
                st.session_state.idx+=1
            info_placeholder.subheader('Question No. '+str((st.session_state.idx)+1)+' out of '+str(len(st.session_state.questions)))
            q_placeholder.text('Current Question: '+st.session_state.questions[st.session_state.idx])
            with question_audio_placeholder.container():
                st.write(question_audio(st.session_state.questions[st.session_state.idx]))
            # st.write(rn())


    if not submit_btn_state:
        st.success("That's it, please share your feedback above. To attempted a new QB just select and different QB from QB dropdown. and to reattempt, refresh the page.")
        if st.button("Submit",disabled=submit_btn_state):
            st.session_state.submit_pressed = True
            id = rn()
            temp_dfs = []
            main_df = pd.DataFrame()
            for i in st.session_state.answers:
                q = i
                a = st.session_state.answers[i]['Your answer']
                ia = st.session_state.answers[i]['Ideal Answser']
                s = st.session_state.stars
                f = st.session_state.feedback
                # st.write(q,a,s,id,player_email,st.session_state.QB_name)
                answer_df = pd.DataFrame({'ID':[str(id)],'QB':[str(st.session_state.QB_name)],'Email':[str(player_email)],'Question':[str(q)],'Answer':[str(a)],'Ideal Answer':[str(ia)],'Stars':[str(s)],'Feedback':[str(f)]})
                temp_dfs.append(answer_df)
                # answer_df = pd.DataFrame({'QB_NAME': [QB_name], 'Question': [st.session_state.questions], 'Answer': [st.session_state.answers],'Ratings':[stars],"Email":[player_email]})
            try:
                main_df = pd.concat(temp_dfs, axis=0).fillna('0')
                google_sheet_action('1C0i6OaBYxdf-6jhlWTsMHk4FSkEd_oGEKzUJ63mvBj8','Answers!A:G','append',main_df,False)
                st.success('Answers have been logged')
            except:
                st.warning("Answers can't be logged [No questions were answers]")


    if not st.session_state.submit_pressed:
        pass
        # st.write("Here are your answers:")
        # st.write(st.session_state.answers)
    else:
        reset()
