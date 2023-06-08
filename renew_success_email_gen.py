from subprocess import PIPE, Popen

mentor = ("Jane Doe", "jane@notexist.edu")
mentee = ("John Doe", "john@notexist.edu")

with open('SIGPLAN-M: Mentee Renewal Success.md', 'r') as f:
    template = f.read()

mentor_first_name = mentor[0].split()[0]
mentee_first_name = mentee[0].split()[0]

email = template.replace('<mentor>', mentor_first_name)
email = email.replace('<mentee>', mentee_first_name)
email = email.replace('<Name>', 'Jocelyn')

# send the email
script = 'tell application "Mail"\n set theTos to {{ "{}", "{}" }}\n set theMessage to make new outgoing message with properties {{visible:true, subject:"SIGPLAN-M: Mentorship renewed!", content: "{}" }}\n tell theMessage\n repeat with theTo in theTos\n make new recipient at end of to recipients with properties {{address:theTo}}\n end repeat\n end tell\n end tell'.format(mentor[1], mentee[1], email).encode()
print(script)
p = Popen('/usr/bin/osascript',stdin=PIPE,stdout=PIPE)
p.communicate(script)