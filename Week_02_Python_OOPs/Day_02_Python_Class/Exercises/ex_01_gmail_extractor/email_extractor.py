import os
import json
import base64
from typing import Optional, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Source: https://developers.google.com/gmail/api/quickstart/python
def authenticate_gmail_api(
    credentials_path: str, token_path: str, SCOPES: List[str]
) -> str:
    """
    Authenticates with Gmail API and returns a service object. Writes a refresh token to token_path.

     Attributes:
         pan_details: input PAN which caused the error
         message: explanation of the error
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(
            token_path,
            SCOPES,
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(
            token_path,
            "w",
        ) as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def extract_data_from_email(email):

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
                email_details["text_body"] = email_details["text_body"] + text_body
            if part["filename"]:
                email_details["attachments"].append(part["filename"])

    email_details["word_count"] = len(email_details["text_body"].split())
    email_details["line_count"] = email_details["text_body"].count("\n")
    email_details["num_attachments"] = len(email_details["attachments"])
    email_details["text_body"] = ""

    return email_details


def get_message_content(service, message_ids: List[str], user_id: str = "me"):
    message_content = list()
    for id in message_ids:
        content = (
            service.users()
            .messages()
            .get(userId=user_id, id=id, format=None, metadataHeaders=None)
            .execute()
        )
        message_content.append(content)
    return message_content


def get_message_ids(
    service,
    label_ids: List[str],
    user_id: str = "me",
    max_results: int = 10,
    filter_query: Optional[str] = None,
) -> List[str]:
    message_ids = (
        service.users()
        .messages()
        .list(
            userId=user_id,
            labelIds=label_ids,
            q=filter_query,
            maxResults=max_results,
        )
        .execute()
    )

    return [message["id"] for message in message_ids["messages"]]


def dump_to_json(data, json_path):
    with open(json_path, "w") as json_output_file:
        json.dump(data, json_output_file)


def load_from_json(json_path):
    with open(json_path) as json_input_file:
        return json.load(json_input_file)


# in:inbox from:(megha.marwah@tothenew.com) to:(ahan.jain@tothenew.com) subject:subject includes the words -{doesnt have} has:attachment larger:1/1M/1K after:2024/8/12 before:2025/8/13
# in:inbox from:(megha.marwah@tothenew.com) to:(ahan.jain@tothenew.com) subject:subject
# includes the words -{doesnt have} has:attachment larger:1/1M/1K after:2024/8/12 before:2025/8/13
# from:(ahanjain@gmail.com,ahan.jain@tothenew.com) to:(ahanjain@gmail.com,ahan.jain@tothenew.com) subject:subj itw -dh has:attachment larger:1K
def gmail_filter_query(
    email_from: Optional[List[str]] = None,
    email_to: Optional[List[str]] = None,
    subject: Optional[str] = None,
    includes_words: Optional[str] = None,
    excludes_words: Optional[str] = None,
    has_attachment: Optional[bool] = None,
    larger_than: Optional[str] = None,
    before_yyyy_m_dd: Optional[str] = None,
    after_yyyy_m_dd: Optional[str] = None,
):
    query = ""

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
    credentials_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/credentials.json"
    token_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/token.json"
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    gmail_service = authenticate_gmail_api(credentials_path, token_path, SCOPES)
    # filter_query = gmail_filter_query(
    #     includes_words=".pdf",
    # )

    filter_query = gmail_filter_query(includes_words="Bootcamp")

    print(f"Query: {filter_query}")

    message_ids = get_message_ids(
        gmail_service,
        label_ids=["INBOX"],
        user_id="me",
        max_results=100,
        filter_query=filter_query,
    )

    # raw_message_id_dump_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/raw_message_id_dump.json"
    # dump_to_json(message_ids, raw_message_id_dump_path)
    # message_ids = load_from_json(raw_message_id_dump_path)
    # print(len(message_ids))

    message_content = get_message_content(gmail_service, message_ids, user_id="me")
    # raw_message_content_dump_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/raw_message_content_dump.json"
    # dump_to_json(message_content, raw_message_content_dump_path)
    # message_content = load_from_json(raw_message_content_dump_path)
    # print(len(message_content))

    extracted_email_data = [
        extract_data_from_email(message) for message in message_content
    ]

    print(f"{len(extracted_email_data)} matches found...\n", extracted_email_data)

    # extracted_email_data_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_02_Python_OOPs/Day_02_Python_Class/Exercises/ex_01_gmail_extractor/extracted_email_data.json"
    # print(len(extracted_email_data))
    # dump_to_json(extracted_email_data, extracted_email_data_path)


if __name__ == "__main__":
    main()
