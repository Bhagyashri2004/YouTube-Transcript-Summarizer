🔐 Multi-Language YouTube Transcript Summarizer with Secure Authentication
-------------------------------------------------------------------------------------------------------------------

A GUI-based Python application that allows users to securely log in, fetch YouTube video transcripts, and summarize them in multiple languages using LLaMA3 via Groq API. Designed with a glassmorphic UI for a modern look, and built with PyQt6, it combines natural language processing and secure user access in one tool.

👤 1. User Authentication System
The app starts with a secure login screen with options to:

🔐 Login with credentials
📝 Register a new user

All credentials are securely handled using SHA-256 hashing and stored in a local SQLite database.
-------------------------------------------------------------------------------------------------------------------

🏠 2. Dashboard / Home Page
After login, users are redirected to the main summarization interface, which includes:

🎥 YouTube Link Input
🌐 Language Selection
📥 Fetch Transcript Button
📄 Summarized Output Box
-------------------------------------------------------------------------------------------------------------------

🔍 3. Transcript Summarization Flow
✍️ User Input:
YouTube Video URL
Preferred Output Language (e.g., English, Hindi, Japanese, etc.)

🔁 Backend Workflow:
Extracts transcript using youtube_transcript_api
Converts the transcript to plain text
Sends it to Groq API with LLaMA3 model
Gets the summary in the selected language
Displays the result in the UI
-------------------------------------------------------------------------------------------------------------------

🌐 4. Language Support
Currently supports summarization in:

Language	Support
English		✅
Japanese	✅
Hindi		✅
More to come	🚧
-------------------------------------------------------------------------------------------------------------------

💡 5. Smart Features

Feature	Description
🧠 LLaMA3 Summarization	Uses powerful LLM via 	Groq API for accurate summaries
🧾 Multi-language Summary Output		Translates summaries to selected languages
🖼️ Glassmorphism UI				Stylish, modern design with blurred card layout
👁️ Password Visibility Toggle			Eye icon to show/hide password securely
🛡️ Secure Authentication			Uses SHA-256 hashing, not plain-text passwords
📄 Transcript View				Option to view full transcript before summarizing (coming soon)
💬 Error Handling				Informative user messages for invalid URLs, login errors, etc.

------------------------------------------------------------------------------------------------------------------

🛠️ 6. Technologies Used

Technology		Purpose
PyQt6	        	GUI Design and Event Handling
sqlite3 		Secure local user database
hashlib 		SHA-256 password hashing
youtube_transcript_api	Fetch video transcripts
Groq API		Summarization using LLaMA3
requests		API requests to Groq
re			YouTube URL validation
os, sys	 		App control and exit handling


-------------------------------------------------------------------------------------------------------------------

🚀 How to Run

Step 1: Install requirements
pip install youtube-transcript-api


Step 2: Launch the app
python main/login.py

📌 Summary
This app combines secure user management, real-time transcript extraction, and AI-powered summarization into a single, elegant desktop tool. Whether you're learning from YouTube lectures or researching, this app makes content easier to understand—securely, efficiently, and beautifully.