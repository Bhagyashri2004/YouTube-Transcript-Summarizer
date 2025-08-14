# // App 

from groq_client import client

import sys
import os
import re
import markdown
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton,
                            QLabel, QStatusBar, QTextEdit, QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt6.QtGui import QIcon

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from groq_client import client

def extract_video_id(input_string):
    if re.match(r'http(s)?:\/\/', input_string):
        if 'youtube.com' in input_string:
            match = re.search(r'v=([^&]*)', input_string)
            if match:
                return match.group(1)
        elif 'youtu.be' in input_string:
            match = re.search(r'youtu\.be/([^&]*)', input_string)
            if match:
                return match.group(1)
    return input_string  # If it's not a URL, assume it's a video ID

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Transcript Downloader v1 by Jie')
        self.setWindowIcon(QIcon('transcription.png'))
        self.resize(800, 600)
        self.setStyleSheet('font-size: 14px;')

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.init_ui()

    def init_container(self):
        self.button = {}
        self.line_edit = {}
        self.label = {}

    def init_ui(self):
        self.init_container()
        self._add_video_input_section()
        self._add_output_section()
        self._add_button_section()

        self.status_bar = QStatusBar()
        self.layout['main'].addWidget(self.status_bar)

    def _add_video_input_section(self):
        self.layout['video_input'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['video_input'])

        self.label['video_id'] = QLabel('Video ID:')
        self.layout['video_input'].addWidget(self.label['video_id'])

        self.line_edit['video_id'] = QLineEdit()
        self.line_edit['video_id'].setFixedWidth(350)
        self.line_edit['video_id'].setPlaceholderText('Enter video ID or URL')
        self.layout['video_input'].addWidget(self.line_edit['video_id'])

        # Language dropdown
        self.language_dropdown = QComboBox()
        self.language_dropdown.setFixedWidth(200)
        self.language_dropdown.setPlaceholderText("Select language")
        self.layout['video_input'].addWidget(self.language_dropdown)

        # Fetch languages button
        self.button['fetch_languages'] = QPushButton('Fetch Languages')
        self.button['fetch_languages'].setFixedWidth(130)
        self.button['fetch_languages'].clicked.connect(self.fetch_languages)
        self.layout['video_input'].addWidget(self.button['fetch_languages'])

        self.layout['video_input'].addStretch()

    def _add_output_section(self):
        self.label['output'] = QLabel('Transcript:')
        self.layout['main'].addWidget(self.label['output'])

        self.text_edit = QTextEdit()
        self.layout['main'].addWidget(self.text_edit)

    def _add_button_section(self):
        self.layout['transcript_download'] = QHBoxLayout()
        self.layout['main'].addLayout(self.layout['transcript_download'])

        self.button['download_transcript'] = QPushButton('&Download Transcript')
        self.button['download_transcript'].setFixedWidth(175)
        self.button['download_transcript'].clicked.connect(self.download_transcript)
        self.layout['transcript_download'].addWidget(self.button['download_transcript'])

        self.button['summarize_transcript'] = QPushButton('&Summarize Transcript')
        self.button['summarize_transcript'].setFixedWidth(150)
        self.button['summarize_transcript'].clicked.connect(self.summarize_transcript)
        self.layout['transcript_download'].addWidget(self.button['summarize_transcript'])

        self.layout['transcript_download'].addStretch()

    def fetch_languages(self):
        video_id = self.line_edit['video_id'].text()
        if not video_id:
            self.status_bar.showMessage('Please enter a video ID or URL')
            return

        video_url = extract_video_id(video_id)

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_url)

            self.language_dropdown.clear()
            for transcript in transcript_list:
                lang_name = transcript.language
                lang_code = transcript.language_code
                self.language_dropdown.addItem(f"{lang_name} ({lang_code})", lang_code)

            self.status_bar.showMessage("Languages fetched successfully.")
        except Exception as e:
            self.status_bar.showMessage(f"Error fetching languages: {e}")
            
    def download_transcript(self):
        video_id = self.line_edit['video_id'].text()

        if not video_id:
            self.status_bar.showMessage('Please enter a video ID or URL')
            return
        else:
            self.status_bar.clearMessage()

        video_url = extract_video_id(video_id)
        selected_lang = self.language_dropdown.currentData()

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_url)

            if selected_lang:
                transcript = transcript_list.find_transcript([selected_lang])
            else:
                transcript = transcript_list.find_transcript(['en'])

            fetched = transcript.fetch()
            transcript_text = '\n'.join([line.text for line in fetched])  # ✅ fixed here
            self.text_edit.setPlainText(transcript_text)

        except Exception as e:
            self.text_edit.setPlainText(f'Error: {e}')


    def summarize_transcript(self):
        transcript_text = self.text_edit.toPlainText()
        if not transcript_text:
            self.status_bar.showMessage('Transcript is empty.')
            return
        else:
            self.status_bar.clearMessage()

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the video transcript below into bullet points:\n\n{transcript_text}",
                }
            ],
            model="llama3-8b-8192",
            temperature=0.3
        )

        html_content = markdown.markdown(chat_completion.choices[0].message.content)
        self.text_edit.setHtml(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app_window = AppWindow()
    app_window.show()
    sys.exit(app.exec())
