# Scripts for SIGPLAN-M renewal

## Setup

This repo is only tested on python 3.10. 

First, install all the dependencies by running:

```
pip install -r requirements.txt
```

Since this repo will access google sheet. You need to first authorize gspread to access to your account. Follow the setup procedure in this link: https://docs.gspread.org/en/v5.7.1/oauth2.html. 

Since I use Mac and the script will invoke the 'Mail' app in Mac to send the email, it is recommended that this script is run on MacOS (feel free to update the script to invoke other mail clients). 

## Usage

To automatically generate emails for mentor renewal for a particular month, modify the variable `index_key` in renew_email_gen.py. Assuming you have already authorized gspread and set the variable properly, run the following command:

```
python renew_email_gen.py
```

This will automatically generate all renewal emails for a particular month as email drafts in the Mail app. It will not send the email so that you have the chance to do manual modifications before sending. 

Note that this script only generates email for the mentors. To generate email for the mentees, directly copy paste the content in `SIGPLAN-M: Mentee Renewal.md`. The emails for all mentees to be renewed should be printed as stdout when you run the renew_email_gen.py under the section 'mentee emails' in the form of a comma-separated string. 

This repo also support automated formatting for renewal success email and rematch_email. To send a renewal success email, open `renew_success_email_gen.py` and update the names and emails of the mentor and mentee. The output of this script is a Mail email draft as well.

To send a rematch email, open `rematch_email_gen.py` and update the name of the mentee. The output of this script is also a Mail email draft. 