from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from extract import authenticate_gmail
import base64
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
st.set_page_config(
    page_title="Unfortunately, Blah",
    page_icon="📊",
    layout="wide"
)
confirmed_rejection_phrases = [
    "not moving forward",
    "move forward with other candidates",
    "pursue other candidates",
    "not selected",
    "decided not to proceed",
    "will not be moving forward"
]
generic_sender_labels = [
    "hiring team",
    "recruiting team",
    "professional recruiting team",
    "notification"
]
generic_domains = [
    "greenhouse-mail.io",
    "dayforce.com",
    "crelate.net",
    "indeed.com",
    "workday.com",
    "paychex.com"
    
]
company_name_fixes = {
    "smithrx": "SmithRx",
    "htijobs": "HTI",
    "sisfirst": "Surgical Information Systems",
    "recruiting team approvals": "Unknown"
}
def clean_body(body):
    soup=BeautifulSoup(body, "html.parser")
    text= soup.get_text()
    words = text.split()
    clean_text = " ".join(words)
    return clean_text

def is_rejection(text):
    for phrase in confirmed_rejection_phrases:
        if phrase in text:
            return True

    return False
def extract_company(sender, subject, body):
    if "<" in sender:                         # Question 1
        company = sender.split("<")[0].strip()

        if company.lower() not in generic_sender_labels:  # Question 2
            return company
    subject_lower = subject.lower()
    if "application to " in subject_lower:
        position = subject_lower.find("application to ")
        company_start = position + len("application to ")
        company = subject[company_start:]
        return company
    if "thank you from " in subject_lower:
        position = subject_lower.find("thank you from ")
        company_start = position + len("thank you from ")
        company = subject[company_start:]
        return company
    if "applying to" in subject_lower:
        position = subject_lower.find("applying to ")
        company_start = position + len("applying to ")
        company = subject[company_start:]
        return company
    if "thank you for your interest in " in subject_lower:
        position = subject_lower.find("thank you for your interest in ")
        company_start = position + len("thank you for your interest in ")
        company = subject[company_start:]
        return company
    if "application update with " in subject_lower:
        position = subject_lower.find("application update with ")
        company_start = position + len("application update with ")
        company = subject[company_start:]
        return company
    if "@" in sender:
        domain = sender.split("@")[1]
        domain = domain.strip(" >")

        is_generic_domain = False

        for generic_domain in generic_domains:
            if domain.endswith(generic_domain):
                is_generic_domain = True
                break
        if not is_generic_domain:
            companyC = domain.split(".")[0]
            return companyC
    return "Unknown"
def clean_company_name(company):
    company = company.replace(" Notification", "")
    company = company.replace(" TalentHub", "")
    if company in company_name_fixes:
         return company_name_fixes[company]

    return company
def fix_unknown_company(company, subject):
    subject = subject.strip()

    if company == "Unknown" and subject in unknown_company_fixes:
        return unknown_company_fixes[subject]

    return company
def extract_job_title(subject, body):
    subject = str(subject)
    body = str(body)

    subject_lower = subject.lower()
    body_lower = body.lower()



    if "application for" in subject_lower:
        position = subject_lower.find("application for")
        job_start = position + len("application for ")
        return subject[job_start:].strip()

    if "application on " in subject_lower:
        position = subject_lower.find("application on ")
        job_start = position + len("application on ")
        return subject[job_start:].strip()

    if "application as" in subject_lower:
        position = subject_lower.find("application as")
        job_start = position + len("application as ")
        return subject[job_start:].strip()

    if "application at" in subject_lower:
        position = subject_lower.find("application at")
        job_start = position + len("application at ")
        return subject[job_start:].strip()

    if "application status for " in subject_lower:
        position = subject_lower.find("application status for ")
        job_start = position + len("application status for ")
        return subject[job_start:].strip()

    if subject_lower.startswith("data ") and " - " in subject:
        return subject.split(" - ")[0].strip()

    if subject_lower.startswith("data ") and "," in subject:
        return subject.split(",")[0].strip()


    if (
        "interest in the " in subject_lower
        and " opportunity" in subject_lower
    ):
        position = subject_lower.find("interest in the ")
        job_start = position + len("interest in the ")
        job_end = subject_lower.find(" opportunity", job_start)

        if job_end != -1:
            return subject[job_start:job_end].strip()

    if (
        "regarding your recent job application" in subject_lower
        and "|" in subject
    ):
        parts = subject.split("|")

        if len(parts) > 1:
            return parts[1].strip()


    if "update from abbvie" in subject_lower and " - " in subject:
        job_title = subject.split(" - ")[0]
        return job_title.strip(" ​")

 
    if subject_lower.startswith("application update - "):
        job_title = subject[len("Application Update - "):]
        return job_title.strip()

   
    if subject_lower.startswith("rhythm energy") and "–" in subject:
        job_title = subject.split("–", 1)[1]
        return job_title.strip()

    if subject_lower.startswith("sca application update:"):
        job_title = subject.split(":", 1)[1]
        job_title = job_title.split(",")[0]
        return job_title.strip()

 
    if subject_lower.startswith("fis application update") and " - " in subject:
        job_title = subject.rsplit(" - ", 1)[1]

        if "(" in job_title:
            job_title = job_title.split("(")[0]

        parts = job_title.split()

        if parts and parts[0].upper().startswith("JR"):
            job_title = " ".join(parts[1:])

        return job_title.strip()


    if subject_lower.startswith(
        "rrd: thank you for your interest -"
    ):
        job_title = subject.split(" - ", 1)[1]
        return job_title.strip(" ​")

    if " position at " in subject_lower:
        position = subject_lower.find(" position at ")
        job_title = subject[:position]
        return job_title.strip()


    if " and the " in subject_lower and " role" in subject_lower:
        job_start = (
            subject_lower.find(" and the ")
            + len(" and the ")
        )

        job_end = subject_lower.find(
            " role",
            job_start
        )

        if job_end != -1:
            return subject[job_start:job_end].strip()

  
    if (
        subject_lower.startswith("thank you for applying to ")
        and " at " in subject_lower
    ):
        job_start = len("thank you for applying to ")

        job_end = subject_lower.find(
            " at ",
            job_start
        )

        if job_end != -1:
            return subject[job_start:job_end].strip()

   
    if (
        subject_lower.startswith("your application to ")
        and " - " in subject
    ):
        return subject.rsplit(" - ", 1)[1].strip()

   
    if (
        "follow-up for the " in subject_lower
        and " position" in subject_lower
    ):
        job_start = (
            subject_lower.find("follow-up for the ")
            + len("follow-up for the ")
        )

        job_end = subject_lower.find(
            " position",
            job_start
        )

        if job_end != -1:
            return subject[job_start:job_end].strip()


    if (
        "north american lighting" in subject_lower
        and " - " in subject
    ):
        parts = subject.split(" - ")

        if len(parts) >= 2:
            return parts[-1].strip(" ​")

    
    if "interest in the " in body_lower:
        position = body_lower.find("interest in the ")
        job_start = position + len("interest in the ")
        job_end = body_lower.find(" position", job_start)

        if job_end != -1:
            return body[job_start:job_end].strip()

    if "application for the " in body_lower:
        position = body_lower.find("application for the ")
        job_start = position + len("application for the ")
        job_end = body_lower.find(" role", job_start)

        if job_end != -1:
            return body[job_start:job_end].strip()

    if "submitting your application to " in body_lower:
        position = body_lower.find(
            "submitting your application to "
        )

        job_start = (
            position
            + len("submitting your application to ")
        )

        job_end = body.find(".", job_start)

        if job_end != -1:
            return body[job_start:job_end].strip()

    if "thank you for applying to the " in body_lower:
        position = body_lower.find(
            "thank you for applying to the "
        )

        job_start = (
            position
            + len("thank you for applying to the ")
        )

        job_end = body_lower.find(
            " position at ",
            job_start
        )

        if job_end != -1:
            return body[job_start:job_end].strip()

    if "apply for the " in body_lower:
        position = body_lower.find("apply for the ")
        job_start = position + len("apply for the ")
        job_end = body_lower.find(" position", job_start)

        if job_end != -1:
            return body[job_start:job_end].strip()

    if "applications for the " in body_lower:
        position = body_lower.find(
            "applications for the "
        )

        job_start = (
            position
            + len("applications for the ")
        )

        job_end = body_lower.find(
            " role",
            job_start
        )

        if job_end != -1:
            return body[job_start:job_end].strip()

    if "applying to the " in body_lower:
        position = body_lower.find("applying to the ")
        job_start = position + len("applying to the ")
        job_end = body_lower.find(" position", job_start)

        if job_end != -1:
            return body[job_start:job_end].strip()


    return "Unknown"
def clean_job_title(job_title):
    if " at " in job_title:
        job_title = job_title.split(" at ")[0]
    if " with " in job_title:
        job_title = job_title.split("with")[0]

    
    return job_title

creds = authenticate_gmail()
service = build("gmail", "v1", credentials=creds)
rejection_phrases = [
    "not moving forward",
    "move forward with other candidates",
    "pursue other candidates",
    "not selected",
    "another candidate",
    "other candidates",
    "decided not to proceed",
    "will not be moving forward"
]
unknown_company_fixes = {
    "Togetherwork Application for Data Migration Specialist Position": "Togetherwork",
    "Your Application with Bridgeway Benefit Technologies": "Bridgeway Benefit Technologies",
    "Re: Your Application for Data Analyst (Consumer Product Safety), Limited Duration at Consumer Reports": "Consumer Reports",
    "Thank you for your interest in Konica Minolta": "Konica Minolta",
    "Judi Health/Capital Rx | Update": "Judi Health/Capital Rx",
    "CORA Physical Therapy - Update on Your Application": "CORA Physical Therapy",
    "Talkdesk Application": "Talkdesk",
    "Application Status Update | Project Specialist (Technical Team) at YA Group": "YA Group",
    "UGT: Application Status": "UGT"
}
SDate="2025/12/01"
query = ""
for phrase in rejection_phrases:
    if query=="":
        query+= '"'+ phrase + '"'
    else:
        query += " OR " + '"' + phrase + '"'
query = "after:" + SDate + " " + "(" + query + ")"
print(query)
results= service.users().messages().list(
    userId="me",
    q=query
).execute()
Rejectresults = results["messages"]
next_page_token=results["nextPageToken"]
while next_page_token:
    next_results=service.users().messages().list(userId="me",
q=query,
pageToken=next_page_token
).execute()
    Rejectresults += next_results["messages"]
    next_page_token = next_results.get("nextPageToken")
#print(len(Rejectresults))
email_records = []
for message in Rejectresults:
        subject = ""
        sender = ""
        Sendate = ""
        decoded_body = ""
        Result_message = message["id"]
        email = service.users().messages().get(  userId="me",
        id=Result_message).execute()
    # print("loop started")
    # print(email)
    # print("loop finished")
        email_info = email["payload"]
        email_headers = email_info["headers"]
        for header in email_headers:
            if header["name"]=="Subject":
                subject=header["value"]
                #print(subject)
            elif header["name"]== "From":
                sender=header["value"]
                #print(sender)
            elif header["name"]=="Date":
                Sendate=header['value']
                #print(Sendate)
        if "parts" in email_info:     
            email_parts = email_info["parts"]  
            for part in email_parts:
                #print(part["mimeType"])
                if part["mimeType"]=="text/plain":
                    bodypart = part["body"]
                    encoded_body = bodypart["data"]
                    decoded_body = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
                    #print(decoded_body)
        else:
            bodypart = email_info["body"]
            encoded_body = bodypart["data"]
            decoded_body = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
            #print(decoded_body)
        email_record={ "date": Sendate,
        "sender": sender,"subject": subject,"body": decoded_body}          
        email_records.append(email_record)
RejectionDataframe=pd.DataFrame(email_records)
RejectionDataframe.to_csv("BlahRejection.csv", index=False)
RejectionDataframe["clean_body"] = RejectionDataframe["body"].apply(clean_body)
RejectionDataframe["is_rejection"] = RejectionDataframe["clean_body"].apply(is_rejection)
#print(RejectionDataframe.head())
confirmed_rejections = RejectionDataframe[
    RejectionDataframe["is_rejection"] == True
].copy()
confirmed_rejections["company"] = confirmed_rejections.apply(
    lambda row: extract_company(
        row["sender"],
        row["subject"],
        row["clean_body"]
    ),
    axis=1
)
confirmed_rejections["clean_company"] = (
    confirmed_rejections["company"]
    .apply(clean_company_name)
)
confirmed_rejections["clean_company"] = confirmed_rejections.apply(
    lambda row: fix_unknown_company(
        row["clean_company"],
        row["subject"]
    ),
    axis=1
)
confirmed_rejections["job_title"] = confirmed_rejections.apply(
    lambda row: extract_job_title(
        row["subject"],
        row["clean_body"]
    ),
    axis=1

)
known_job_titles = len(job_graph_data)
total_rejections = len(confirmed_rejections)

extraction_rate = (
    known_job_titles / total_rejections * 100
    if total_rejections > 0 else 0
)
st.title("Unfortunately, Blah 📩")
st.caption(
    "An interactive analysis of job rejection patterns, companies, roles, and timing."
)
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric(
            "Total Rejections",
            len(confirmed_rejections)
    )

with col2:
    with st.container(border=True):
        st.metric(
            "Unique Companies",
            confirmed_rejections["clean_company"].nunique()
    )

with col3:
    with st.container(border=True):
        st.metric(
            "Known Job Titles",
        (
            confirmed_rejections["job_title"]
            .astype(str)
            .str.strip()
            .str.lower()
            .ne("unknown")
            .sum()
        )
    )
with col4:
    with st.container(border=True):
        st.metric(
            "Job Title Extraction Rate",
            f"{extraction_rate:.1f}%"
        )
confirmed_rejections["parsed_date"] = pd.to_datetime(
    confirmed_rejections["date"]
    .astype(str)
    .str.replace(r"\s*\(UTC\)\s*$", "", regex=True),
    format="mixed",
    errors="coerce",
    utc=True
)
confirmed_rejections["month"] = (
    confirmed_rejections["parsed_date"]
    .dt.tz_localize(None)
    .dt.to_period("M")
    .astype(str)
)

monthly_rejections = (
    confirmed_rejections["month"]
    .value_counts()
    .sort_index()
)
confirmed_rejections["weekday"] = (
    confirmed_rejections["parsed_date"]
    .dt.day_name()
)

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_counts = (
    confirmed_rejections["weekday"]
    .value_counts()
    .reindex(weekday_order, fill_value=0)
)
job_graph_data = confirmed_rejections[
    confirmed_rejections["job_title"]
    .astype(str)
    .str.strip()
    .str.lower()
    .ne("unknown")
].copy()



company_graph_data = confirmed_rejections[
    confirmed_rejections["clean_company"]
    .astype(str)
    .str.strip()
    .str.lower()
    .ne("unknown")
].copy()

company_counts = (
    company_graph_data["clean_company"]
    .value_counts()
    .head(10)
)
def categorize_job_title(title):
    title_lower = str(title).lower()

    if "data analyst" in title_lower:
        return "Data Analyst"

    if "data engineer" in title_lower:
        return "Data Engineer"

    if "business analyst" in title_lower:
        return "Business Analyst"

    if "operations analyst" in title_lower:
        return "Operations Analyst"

    if "financial analyst" in title_lower:
        return "Financial Analyst"

    if "product analyst" in title_lower:
        return "Product Analyst"

    if "systems analyst" in title_lower:
        return "Systems Analyst"

    return str(title).strip()
job_graph_data = confirmed_rejections[
    confirmed_rejections["job_title"]
    .astype(str)
    .str.strip()
    .str.lower()
    .ne("unknown")
].copy()
job_graph_data["job_category"] = (
    job_graph_data["job_title"]
    .apply(categorize_job_title)
)
job_counts = (
    job_graph_data["job_category"]
    .value_counts()
    .head(10)
)


left, right = st.columns(2)

with left:
     with st.container(border=True):
        st.subheader("Top Rejected Job Titles")
        st.bar_chart(
        job_counts,
        height=280
    )

with right:
     with st.container(border=True):
        st.subheader("Top Rejected Companies")
        st.bar_chart(
        company_counts,
        height=280
    )
left, right = st.columns(2)

with left:
     with st.container(border=True):
        st.subheader("Rejections by Month")
        st.line_chart(
        monthly_rejections,
        height=280
    )

with right:
     with st.container(border=True):
        st.subheader("Rejections by Weekday")
        st.bar_chart(
            weekday_counts,
        height=280
    )