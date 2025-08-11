import re
import smtplib
import easyimap as e
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage

# Gmail credentials (App Passwords required)
unm = "zaifatima12345@gmail.com"
pwd = "cbve qxte hlav bkdu"  # IMAP password (App password)

# Setup recognizer & speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

# Speak function
def speak(message):
    print(message)
    engine.say(message)
    engine.runAndWait()

# Listen function
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("Speak Now:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except:
            speak("Sorry, could not recognize what you said")
            return None

# Send email
def sendmail():
    rec = "mainproject786@gmail.com"

    speak("Please speak the subject of your email")
    subject = listen()

    speak("You have spoken the subject")
    speak(subject)

    speak("Please speak the body of your email")
    body = listen()

    speak("You have spoken the message")
    speak(body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("zaifatima12345@gmail.com", "hjws qegt owpr ihcn")  # Using app password here
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(unm, rec, msg)
        server.quit()
        speak("The mail has been sent successfully")
    except Exception as e:
        speak("Failed to send the email.")
        print("Error:", e)

# Read email
def readmail():
    try:
        server = e.connect("imap.gmail.com", unm, pwd)
        mail_ids = server.listids(limit=10)  # Latest 10 emails

        if not mail_ids:
            speak("Your inbox is empty.")
            server.quit()
            return

        speak(f"You have {len(mail_ids)} recent emails.")
        speak("Please say the serial number of the email you want to read, starting from one for the latest.")

        num_text = listen()
        if not num_text:
            speak("I could not understand the number.")
            server.quit()
            return

        print(f"[DEBUG] Recognized speech: {num_text}")

        # Extract number from speech (handles 'email number two please')
        match = re.search(r"\d+", num_text)
        if match:
            index = int(match.group())
        else:
            num_map = {
                "one": 1, "two": 2, "to": 2, "too": 2, "three": 3,
                "four": 4, "for": 4, "five": 5, "six": 6,
                "seven": 7, "eight": 8, "ate": 8, "nine": 9, "ten": 10
            }
            index = num_map.get(num_text.strip().lower(), None)

        if not index:
            speak("That is not a valid number.")
            server.quit()
            return

        b = index - 1
        if b < 0 or b >= len(mail_ids):
            speak("Invalid email number.")
            server.quit()
            return

        email = server.mail(mail_ids[b])
        from_addr = email.from_addr or "Unknown sender"
        subject = email.title or "No subject"
        body_text = (email.body or "No body").strip().replace("\n", " ")
        if len(body_text) > 500:
            body_text = body_text[:500] + " ... message truncated."

        speak(f"The mail is from {from_addr}")
        speak(f"The subject is {subject}")
        speak(f"The body is {body_text}")

        server.quit()

    except Exception as err:
        speak("An error occurred while reading the email.")
        print("[ERROR]", err)

# Main loop
speak("Welcome to voice controlled email services")

while True:
    speak("What do you want to do?")
    speak("Speak SEND to send email, READ to read email, or EXIT to exit")

    ch = listen()
    if not ch:
        continue

    ch = ch.lower()
    if "send" in ch:
        speak("You have chosen to send an email")
        sendmail()

    elif "read" in ch:
        speak("You have chosen to read email")
        readmail()

    elif "exit" in ch:
        speak("You have chosen to exit, bye bye")
        break

    else:
        speak(f"Invalid choice, you said: {ch}")
