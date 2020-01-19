# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 21:08:56 2020

@author: evan
"""
from __future__ import print_function
import datetime
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTableWidget\
    , QHBoxLayout, QVBoxLayout, QCalendarWidget, QLineEdit, QDateEdit, QTimeEdit, QSizePolicy,\
        QFileDialog, QListWidget
        

from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QDoubleValidator

import datetime
import datefinder
import tabula

class gui(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.masterlayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        
        self.upload = QPushButton('Select Course Outlines')
        self.upload.clicked.connect(self.fileupload)
        
        self.list = QListWidget()
        
        self.hlayout.addWidget(self.list)
        # self.hlayout.addWidget(self.upload)
        
        self.export = QPushButton('Export')
        self.export.clicked.connect(self.tostrings)
        
        self.masterlayout.addLayout(self.hlayout)
        self.masterlayout.addWidget(self.upload)
        self.masterlayout.addWidget(self.export)
        
        self.setLayout(self.masterlayout)
        
    def fileupload(self):
        self.fileexp = browse(self)
        self.fileexp.openFileNameDialog()
        
    def tostrings(self):
        count = self.list.count()
        self.paths = []
        for i in range(count):
            self.paths.append(self.list.item(i).text())
        # self.mine()
        for path in self.paths:
            #if (path.split('.'[0])and path.split('/'[-1] == path)
            #    print("The file you are trying to create has already been made. ")
            df = tabula.convert_into(path, path.split('.')[0] + 'output.csv', pages= 'all')
        main()

    
    def mine(self):
        self.dict = {}
        for path in self.paths: 
            if path.endswith('.pdf'):
                filename = path.split('/')[-1]
                course = filename.split('.')[0]
                
                self.dict[course] = pdfmine.pdfminer(path)
        print(self.dict)
        #self.finddate()
    
    def finddate(self):
        for course in self.dict:
            matches = datefinder.find_dates(self.dict[course])
            for match in matches:
                print(match)
      
class browse(QMainWindow):
    def __init__(self, parent = None):
        super(browse, self).__init__(parent)
        self.title = 'Browse'
        self.width = 640
        self.height = 480
        self.exp = QFileDialog()
        self.setWindowTitle(self.title)
    
    def openFileNameDialog(self):
       options = self.exp.Options()
       options |= self.exp.DontUseNativeDialog
       fileName, _ = self.exp.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
       if fileName:
           ex.list.addItem(fileName)
           self.destroy()
    


    

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
 

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    mEvent = {
  'summary': 'STAT 231 Assignment 1',
  #'location': '200 Uni ave West',
  #'description': '',
  'start': {
    'date': '2020-01-29',
    'timeZone': 'America/New_York',
  },
  'end': {
    'date': '2020-01-29',
    'timeZone': 'America/New_York',
  },

  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}



    nEvent = {
  'summary': 'STAT 231 Assignment 2',
  'start': {
    'date': '2020-02-12',
    'timeZone': 'America/New_York',
  },
  'end': {
    'date': '2020-02-12',
    'timeZone': 'America/New_York',
  },

  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
    mEvent = service.events().insert(calendarId='primary', body=mEvent).execute()
    nEvent = service.events().insert(calendarId='primary', body=nEvent).execute()
    print('Event created: %s' % (mEvent.get('htmlLink')))
    print('Event created: %s' % (nEvent.get('htmlLink')))



#if __name__ == '__main__':
#    main()

# [END calendar_quickstart]
#def smain():
app = QApplication(sys.argv)
ex = gui()
ex.setGeometry(300,300,500,300)
ex.setWindowTitle('lmao')
ex.show()
sys.exit(app.exec_())
 