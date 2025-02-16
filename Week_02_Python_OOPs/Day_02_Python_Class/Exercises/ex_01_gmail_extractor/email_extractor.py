import os
import json
import base64
from typing import Optional, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailExtractor:
    """
    Provides functionailty for downloading emails from Gmail using the Gmail API.
    """

    def __init__(self, credentials_path: str, token_path: str, scopes: List[str]):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes
        self.service = self.authenticate_gmail_api()

    # Source: https://developers.google.com/gmail/api/quickstart/python
    def authenticate_gmail_api(self):
        """
        Authenticates with Gmail API and returns a service object.
        """
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        try:
            return build("gmail", "v1", credentials=creds)
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def get_message_ids(
        self,
        label_ids: List[str],
        user_id: str = "me",
        max_results: int = 10,
        filter_query: Optional[str] = None,
    ) -> List[str]:
        """
        Retrieves email message IDs based on filters.
        """
        response = (
            self.service.users()
            .messages()
            .list(
                userId=user_id,
                labelIds=label_ids,
                q=filter_query,
                maxResults=max_results,
            )
            .execute()
        )

        return [message["id"] for message in response.get("messages", [])]

    def get_message_content(self, message_ids: List[str], user_id: str = "me"):
        """
        Retrieves the full content of emails given message IDs.
        """
        message_content = []
        for message_id in message_ids:
            content = (
                self.service.users()
                .messages()
                .get(userId=user_id, id=message_id, format="full")
                .execute()
            )
            message_content.append(content)
        return message_content

    def extract_data_from_email(self, email):
        """
        Extracts meaningful data from an email message.
        """
        headers = {
            header["name"]: header["value"] for header in email["payload"]["headers"]
        }

        email_details = {
            "subject": headers.get("Subject", "No Subject"),
            "from": headers.get("From", "Unknown"),
            "to": headers.get("To", "Unknown"),
            "date": headers.get("Date", "Unknown"),
            "text_body": "",
            "text_word_count": 0,
            "line_count": 0,
            "attachments": [],
            "num_attachments": 0,
        }

        if "parts" in email["payload"]:
            for part in email["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    text_body = base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8"
                    )
                    email_details["text_body"] += text_body
                if part["filename"]:
                    email_details["attachments"].append(part["filename"])

        email_details["word_count"] = len(email_details["text_body"].split())
        email_details["line_count"] = email_details["text_body"].count("\n")
        email_details["num_attachments"] = len(email_details["attachments"])
        email_details["text_body"] = ""

        return email_details

    @staticmethod
    def dump_to_json(data, json_path):
        """
        Saves data to a JSON file.
        """
        with open(json_path, "w") as json_output_file:
            json.dump(data, json_output_file)

    @staticmethod
    def load_from_json(json_path):
        """
        Loads data from a JSON file.
        """
        with open(json_path) as json_input_file:
            return json.load(json_input_file)

    @staticmethod
    def build_query(
        email_from: Optional[List[str]] = None,
        email_to: Optional[List[str]] = None,
        subject: Optional[str] = None,
        includes_words: Optional[str] = None,
        excludes_words: Optional[str] = None,
        has_attachment: Optional[bool] = None,
        larger_than: Optional[str] = None,
        before_yyyy_m_dd: Optional[str] = None,
        after_yyyy_m_dd: Optional[str] = None,
    ) -> str:

        query = ""

        # return f"from:{email_from} to:{email_to} subject:{subject} {includes_words} {excludes_words} larger:{larger_than} before:{before_yyyy_m_dd} after:{after_yyyy_m_dd}"

        if email_from:
            query += "from:" + "(" + email_from + ")" + " "
        if email_to:
            query += "to:" + "(" + email_to + ")" + " "
        if subject:
            query += "subject:" + subject + " "
        if includes_words:
            query += includes_words + " "
        if excludes_words:
            query += "-" + excludes_words + " "
        if has_attachment:
            query += "has:attachment" + " "
        if larger_than:
            query += "larger:" + larger_than + " "
        if before_yyyy_m_dd:
            query += "before:" + before_yyyy_m_dd + " "
        if after_yyyy_m_dd:
            query += "after:" + after_yyyy_m_dd

        return query


def main():
    credentials_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/creds/credentials.json"
    token_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/creds/token.json"
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    gmail_extractor = GmailExtractor(credentials_path, token_path, SCOPES)

    filter_query = GmailExtractor.build_query(includes_words="Bootcamp")
    # filter_query = GmailExtractor.build_query(includes_words=".pdf")
    print(f"Query: {filter_query}")

    message_ids = gmail_extractor.get_message_ids(
        label_ids=["INBOX"], filter_query=filter_query, max_results=100
    )
    # raw_message_id_dump_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/files/raw_message_id_dump.json"
    # GmailExtractor.dump_to_json(message_ids, raw_message_id_dump_path)
    # message_ids = GmailExtractor.load_from_json(raw_message_id_dump_path)
    print(f"Got {len(message_ids)} message IDs.")

    message_content = gmail_extractor.get_message_content(message_ids)
    # raw_message_content_dump_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/files/raw_message_content_dump.json"
    # GmailExtractor.dump_to_json(message_content, raw_message_content_dump_path)
    # message_content = GmailExtractor.load_from_json(raw_message_content_dump_path)
    print(f"Got {len(message_content)} messages.")

    extracted_email_data = [
        gmail_extractor.extract_data_from_email(message) for message in message_content
    ]
    print(f"{len(extracted_email_data)} matches found...\n", extracted_email_data)

    extracted_email_data_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/files/extracted_email_data.json"
    GmailExtractor.dump_to_json(extracted_email_data, extracted_email_data_path)


if __name__ == "__main__":
    main()
