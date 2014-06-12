SELF-schedule-2014
==================

Session and Speaker scheduling webpages for the South East Linux Fest 2014 (SELF)

The python script generates html snippets that can be manually inserted into
the sessions and speakers webpages. The script uses the provide CSV file.

```
./self-schedule-creator.py SELF-2014_RFP_Responses.csv
```

Future Enhancements
===================
* Capture the form data with more descrete fields:
```
First Name:     [ text box ]
Last Name:      [ text box ]
Email:          [ text box ]
Position/Title: [ text box ]
Company:        [ text box ]
Bio:            [ multiline text box ]
Photo:          [ file upload ]

Talk Title:        [ text box ]
Talk Logo/Graphic: [ file upload ]
Talk Synopsis:     [ multiline text box ]
Private note to selection committee: [ text box ]
```

* Email the speaker with the submission and a link to a pre-filled form
containing their personal info or similar.

* Insert the form data into a database for sorting and processing.

* Allocate each calendar slot with a number, and assign the slot numbers
to talks that have been accepted.

* Generate the PDF, html, and CalDAV outputs from the database.
