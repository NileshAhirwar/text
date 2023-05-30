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


def question_audio(txt):
    tts = gTTS(txt, lang='en',tld = "co.in")
    prompt_response_speech = "question.mp3"
    tts.save(prompt_response_speech)
    audio = Audio(prompt_response_speech, autoplay=True)
    return (audio)

st.set_page_config(
    page_title="Hello",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"

)
st.success("❤️Welocom To Trainee Panel!❤️")


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
                st.write('this QB does not exits'+QB_name,e)
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
    st.session_state.questions = list(df['Questions'])

if 'answers' not in st.session_state :
    st.session_state.answers = {}


# st.write(df[].to_dict())

if 'old_rec' not in st.session_state:
    st.session_state.old_rec = ''

info_placeholder = st.empty()
q_placeholder = st.empty()
a_placeholder = st.empty()
speak_placeholder = st.empty()
question_audio_placeholder = st.empty()
if 'idx' not in st.session_state:
    st.session_state.idx = 0


st.session_state.audio_data = audio_recorder(energy_threshold=100, pause_threshold=100,icon_name='phone',icon_size='1x',key = 1)
q_placeholder.text('Current Question: '+st.session_state.questions[st.session_state.idx])


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


# if audio_bytes:
if st.session_state.idx < len(st.session_state.questions):
    q_placeholder.text('Current Question: '+st.session_state.questions[st.session_state.idx])

if 'btn_txt' not in st.session_state:
    st.session_state.btn_txt = 'Next'

if 'submit_pressed' not in st.session_state:
    st.session_state.submit_pressed = False

info_placeholder.text('Question No. '+str((st.session_state.idx)+1)+' out of '+str(len(df)))

next_btn_state = False
submit_btn_state = False

if ((st.session_state.idx)+1) >= len(df):
    st.session_state.stars = st_star_rating("Rate your response againest ideal Answer", maxValue=5, defaultValue=st.session_state.stars)
    st.session_state.feedback = st.text_input('Feedback (optional)')
    st.session_state.btn_txt = 'Submit'
    next_btn_state = True
elif ((st.session_state.idx)+1) < len(df):
    st.session_state.btn_txt = 'Next'
    submit_btn_state = True

if st.button("Next",disabled=next_btn_state):
    question_audio_placeholder.text = ''
    if st.session_state.idx < (len(st.session_state.questions)-1):
        st.session_state.idx+=1
    info_placeholder.text('Question No. '+str((st.session_state.idx)+1)+' out of '+str(len(df)))
    q_placeholder.text('Current Question: '+st.session_state.questions[st.session_state.idx])
    with question_audio_placeholder.container():
        st.write(question_audio(st.session_state.questions[st.session_state.idx]))
    # st.write(rn())
    
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
        st.write(q,a,s,id,player_email,st.session_state.QB_name)
        answer_df = pd.DataFrame({'ID':[str(id)],'QB':[str(st.session_state.QB_name)],'Email':[str(player_email)],'Question':[str(q)],'Answer':[str(a)],'Ideal Answer':[str(ia)],'Stars':[str(s)],'Feedback':[str(f)]})
        temp_dfs.append(answer_df)
        # answer_df = pd.DataFrame({'QB_NAME': [QB_name], 'Question': [st.session_state.questions], 'Answer': [st.session_state.answers],'Ratings':[stars],"Email":[player_email]})
    main_df = pd.concat(temp_dfs, axis=0).fillna('0')
    google_sheet_action('1C0i6OaBYxdf-6jhlWTsMHk4FSkEd_oGEKzUJ63mvBj8','Answers!A:G','append',main_df,False)
    reset()

if not st.session_state.submit_pressed:
    st.write("Here are your answers:")
    st.write(st.session_state.answers)
