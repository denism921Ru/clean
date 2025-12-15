{\rtf1\ansi\ansicpg1251\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # sheets_client.py\
import gspread\
from google.oauth2.service_account import Credentials\
from config import SERVICE_ACCOUNT_FILE, SPREADSHEET_NAME\
\
def get_sheets():\
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]\
    creds = Credentials.from_service_account_file(\
        SERVICE_ACCOUNT_FILE, scopes=scopes\
    )\
    client = gspread.authorize(creds)\
    spreadsheet = client.open(SPREADSHEET_NAME)\
    return \{\
        "reports": spreadsheet.worksheet("\uc0\u1054 \u1090 \u1095 \u1105 \u1090 \u1099 "),\
        "problems": spreadsheet.worksheet("\uc0\u1055 \u1088 \u1086 \u1073 \u1083 \u1077 \u1084 \u1099 "),\
        "replacements": spreadsheet.worksheet("\uc0\u1047 \u1072 \u1084 \u1077 \u1085 \u1072  / \u1047 \u1072 \u1082 \u1091 \u1087 \u1082 \u1072 "),\
    \}\
}