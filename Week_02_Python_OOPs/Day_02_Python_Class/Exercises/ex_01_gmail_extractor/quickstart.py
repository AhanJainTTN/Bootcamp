import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(
        "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/token.json"
    ):
        creds = Credentials.from_authorized_user_file(
            "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/token.json",
            SCOPES,
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/credentials.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(
            "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/token.json",
            "w",
        ) as token:
            token.write(creds.to_json())

    try:
        gmail_service = build("gmail", "v1", credentials=creds)

        # user_messages = (
        #     gmail_service.users()
        #     .messages()
        #     .list(
        #         userId="me",
        #         labelIds=["INBOX"],
        #         q=None,
        #         pageToken=None,
        #         maxResults=1000,
        #         includeSpamTrash=None,
        #     )
        #     .execute()
        # )

        # with open(
        #     "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/raw_email_dump.json",
        #     "w",
        # ) as raw_email_dump:
        #     json.dump(user_messages, raw_email_dump)

        with open(
            "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/raw_email_dump.json",
            "r",
        ) as raw_email_dump:
            user_messages = json.load(raw_email_dump)

        print(len(user_messages["messages"]))
        message_ids = [message["id"] for message in user_messages["messages"]]
        # print(len(message_ids))
        # print(message_ids[0])

        # message_details = list()
        # for id in message_ids:

        #     message_content = (
        #         gmail_service.users()
        #         .messages()
        #         .get(userId="me", id=id, format=None, metadataHeaders=None)
        #         .execute()
        #     )

        #     message_details.append(message_content)
        # print(len(message_details))

        # with open(
        #     "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/raw_message_dump.json",
        #     "w",
        # ) as raw_message_dump:
        #     json.dump(message_details, raw_message_dump)

        with open(
            "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/raw_message_dump.json",
            "r",
        ) as raw_message_dump:
            email_json = json.load(raw_message_dump)

        print(len(email_json))

        extracted_data = []

        for email in email_json:

            headers = {
                header["name"]: header["value"]
                for header in email["payload"]["headers"]
            }

            print(len(headers))

            email_details = {
                "subject": headers.get("Subject", "No Subject"),
                "from": headers.get("From", "Unknown"),
                "to": headers.get("To", "Unknown"),
                "date": headers.get("Date", "Unknown"),
                "body": "",
                "word_count": 0,
                "line_count": 0,
                "attachments": [],
                "num_attachments": 0,
            }

            # print(email_details)

            body_found = False
            if "parts" in email["payload"]:
                for part in email["payload"]["parts"]:
                    mime_type = part["mimeType"]
                    if mime_type == "text/plain" and not body_found:
                        email_details["body"] = base64.urlsafe_b64decode(
                            part["body"]["data"]
                        ).decode("utf-8")
                        email_details["word_count"] = len(email_details["body"].split())
                        email_details["line_count"] = email_details["body"].count("\n")
                        email_details["body"] = ""
                        body_found = True

                    if "filename" in part and part["filename"]:
                        email_details["attachments"].append(part["filename"])

            email_details["num_attachments"] = len(email_details["attachments"])
            extracted_data.append(email_details)

        with open(
            "/home/ahan/Documents/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/output_emails.json",
            "w",
        ) as output_file:

            json.dump(extracted_data, output_file)

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
