from subprocess import PIPE, Popen
import gspread
import os

# find those that are match in 2021-12
index_key = '2022-04'
# to_be_exclude_idx = [8, 9, 11, 22]           # this is google sheet idx (idx + 1)
to_be_exclude_idx = []

# remove the previously-generated emails
os.system('rm -r mentor_emails')
os.system('mkdir mentor_emails')

gc = gspread.oauth()

# read mentor sheet
mentor_sh = gc.open("SIGPLAN-M mentors")
mentor_year_2_worksheet = mentor_sh.worksheet('Year 2')

# first obtained the headers
mentor_headers = mentor_year_2_worksheet.row_values(1)
# print(mentor_headers)

# read mentee sheet 
mentee_sh = gc.open("SIGPLAN-M mentees")
mentee_year_2_worksheet = mentee_sh.worksheet('Year 2')

# first obtained the headers
mentee_headers = mentee_year_2_worksheet.row_values(1)
# print(mentee_headers)

# obtain the values in the Last Match Batch column
last_match_batch_idx = mentee_headers.index('Last Match Batch')
last_match_batch = mentee_year_2_worksheet.col_values(last_match_batch_idx + 1)
# print(last_match_batch)

to_be_renew_index = [i for i, s in enumerate(last_match_batch) if index_key in s and i + 1 not in to_be_exclude_idx]
# print(to_be_renew_index)
# print([last_match_batch[i] for i in to_be_renew_index])

# find out the right mentee, mentor pairs based on the index 
mentee_column_idx = mentee_headers.index('Name')
mentees = mentee_year_2_worksheet.col_values(mentee_column_idx + 1)

mentee_email_column_idx = mentee_headers.index('Email')
mentee_emails = mentee_year_2_worksheet.col_values(mentee_email_column_idx + 1)

# mentor_column_idx = mentee_headers.index('Previous Mentors')
# mentors = mentee_year_2_worksheet.col_values(mentor_column_idx + 1)

# form (sheet idx, mentee, mentor) list
to_be_renew_results = [(idx, mentees[idx].strip()) for idx in to_be_renew_index]
# print(to_be_renew_results)

# get the email for all the mentee to be sent email to
to_be_email_mentees = [mentee_emails[idx] for idx in to_be_renew_index]
print('======== mentee emails =========')
print(','.join(to_be_email_mentees))
print('================================')

# get the mentor informaton to be sent
mentor_column_idx = mentor_headers.index('Mentor Name')
mentors = mentor_year_2_worksheet.col_values(mentor_column_idx + 1)

mentor_email_column_idx = mentor_headers.index('Email')
mentor_emails = mentor_year_2_worksheet.col_values(mentor_email_column_idx + 1)

mentor_slots_column_idx = mentor_headers.index('Slots')
mentor_slots = mentor_year_2_worksheet.col_values(mentor_slots_column_idx + 1)


renewed_mentor_idx = []

# for each renew candidate, generate an email
for _, mentee in to_be_renew_results:

    # find the current mentor of the mentee
    # because how the spreadsheet is set up the current way is highly inefficient
    for idx, slot in enumerate(mentor_slots):
        if mentee in slot:
            curr_mentor_idx = idx
            break

    # read the mentor renewal template
    with open('SIGPLAN-M: Mentor Renewal.md', 'r') as f:
        mentor_renewal_template = f.read()

    # mentor's first name
    mentor = mentors[idx]
    mentor_first_name = mentor.split(' ')[0]

    # find index of the mentor in the mentor list
    # curr_mentor_idx = mentors.index(mentor)
    renewed_mentor_idx.append(curr_mentor_idx)

    # find the mentor's email
    curr_mentor_email = mentor_emails[curr_mentor_idx]

    # find mentor's slot
    curr_mentor_slot = mentor_slots[curr_mentor_idx]

    # we need to check if the current mentor already have some emails generated
    # that means at least one of their mentee is renewing
    fname = 'mentor_emails/{}.md'.format(curr_mentor_email)
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            mentor_renewal_template = f.read()

    # update mentor_renewal_template
    mentor_renewal_email = mentor_renewal_template.replace('[FirstName]', mentor_first_name)
    mentor_renewal_email = mentor_renewal_email.replace('[Slots]', curr_mentor_slot)

    # remember to highlight the mentee name in red
    mentor_renewal_email = mentor_renewal_email.replace(mentee, '**{}**'.format(mentee))
    mentor_renewal_email = mentor_renewal_email.replace('\'', '\"')
    mentor_renewal_email = mentor_renewal_email.replace('\"', '\\"')

    # send the email
    script = 'tell application "Mail"\n set theTos to {{ "{}" }}\n set theMessage to make new outgoing message with properties {{visible:true, subject:"SIGPLAN-M: Mentor Renewal", content: "{}" }}\n tell theMessage\n repeat with theTo in theTos\n make new recipient at end of to recipients with properties {{address:theTo}}\n end repeat\n end tell\n end tell'.format(curr_mentor_email, mentor_renewal_email).encode()
    print(script)
    p = Popen('/usr/bin/osascript',stdin=PIPE,stdout=PIPE)
    p.communicate(script)

    # save the file!
    with open(fname, 'w+') as f:
        f.write(mentor_renewal_email)
    
print("========= The row of mentee updated ==========")
print([idx + 1 for idx, _ in to_be_renew_results])
print([mentee for _, mentee in to_be_renew_results])
print("==============================================")

print("========= The row of mentor updated ==========")
print([idx + 1 for idx in renewed_mentor_idx])
print([mentors[idx] for idx in renewed_mentor_idx])
print("==============================================")