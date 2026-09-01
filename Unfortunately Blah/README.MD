# Unfortunately, Blah

**Unfortunately, Blah** is a Python and Streamlit application that connects to Gmail, identifies job application emails, extracts useful information, and turns the not-so-fun experience of job searching into an interactive analytics dashboard.

##  Why I Built It

Recently, I have been hit hard, just like many other people in this job market. I was tailoring my résumé, writing cover letters, keeping up with new skills, and doing everything I could to become a stronger Data Analyst and Data Engineer. I even completed my Master's degree in Data Engineering during these trying times.

Around February, I started keeping track of my job applications and rejections in an Excel spreadsheet. My original plan was to eventually turn the data into a dashboard that I jokingly called my **"2026 Job Wrapped."**

But as I continued applying, the rejections kept piling up.

After finishing my Master's in Data Engineering, a little lightbulb went off in my head:

**Why am I manually keeping track of all of this when I have a Data Engineering degree?**

Instead of manually entering every application and rejection into Excel, I decided to build something that could do the work for me.

And that is how **Unfortunately, Blah** was born.

The name is a little play on words inspired by the seemingly endless wave of emails in my mailbox beginning with:

*"Unfortunately..."*

After seeing that word enough times, everything after it started to feel like **blah, blah, blah.**

So I decided to turn those emails into data.

---

##  What Unfortunately, Blah Does

Unfortunately, Blah connects to my Gmail account and processes job-related emails to create a structured view of my job search.

Instead of manually tracking hundreds of emails, the application helps identify and organize information such as:

* Job application emails
* Rejection emails
* Companies
* Job titles
* Application outcomes
* Unknown or unclassified results
* Job-search trends and statistics

The processed data is then displayed through an interactive Streamlit dashboard.

---

##  How It Works

The basic pipeline looks like this:

**Gmail → Email Extraction → Data Cleaning → Classification → Analysis → Streamlit Dashboard**

### 1. Gmail Integration

The application connects to Gmail using Google's API and OAuth authentication.

### 2. Email Extraction

Job-related emails are retrieved and processed to identify useful information from email subjects and content.

### 3. Data Cleaning & Transformation

Python and pandas are used to clean and transform the extracted email data into structured information that can actually be analyzed.

### 4. Classification

Emails are evaluated to determine whether they represent events such as an application confirmation, rejection, or another job-search status.

### 5. Analytics

The structured data is aggregated to calculate job-search statistics and identify patterns.

### 6. Streamlit Dashboard

The final results are presented through an interactive Streamlit interface, allowing the data to be explored visually rather than buried inside an inbox.

---

## 🛠️ Tech Stack

* **Python**
* **pandas**
* **Streamlit**
* **Gmail API**
* **Google OAuth**
* **Data Cleaning & Transformation**
* **Data Visualization**

---

##  What I Learned

What looked like a simple idea quickly became a real data-engineering problem.

Emails are not clean datasets.

Companies use different subject lines, different templates, different wording, and different ways of identifying positions. Some emails contain a clear company and job title, while others provide incomplete or ambiguous information.

Building Unfortunately, Blah required me to think about:

* Extracting information from semi-structured text
* Cleaning inconsistent data
* Handling missing and unknown values
* Designing classification logic
* Working with APIs
* Implementing OAuth authentication
* Debugging incorrect classifications
* Building an interactive user interface
* Turning raw information into meaningful metrics

More importantly, this project gave me the opportunity to build something from an idea that was completely my own.

There was no school assignment telling me what dataset to use.

There was no prompt telling me what pipeline to build.

I had a problem, I had data, and I realized I had the skills to create a solution.

---

##  Future Improvements

Unfortunately, Blah is still evolving.

Future versions could include:

* Improved job-title extraction
* More advanced email classification
* Better identification of application updates beyond rejections
* Cross-referencing application confirmations with later status emails
* Automated dashboard refreshes
* Additional job-search KPIs
* More detailed company and role analytics
* Improved handling of unknown or ambiguous emails
* Expanded historical job-search analysis

Ultimately, I want Unfortunately, Blah to become more than a rejection tracker.

I want it to tell the complete story of a job search — from the moment an application is submitted to whatever happens next.

---

##  The Story Behind the Data

Job searching can be discouraging.

But if there is one thing studying data engineering taught me, it is that when you have a lot of messy data...

**you might as well build a pipeline for it.**

And if another email starts with *"Unfortunately..."*?

Unfortunately, Blah will handle it.
