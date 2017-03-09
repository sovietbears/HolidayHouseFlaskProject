from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import time
import csv
import random
global generatedAnt, spamAnsw

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WebCoursework'  # Secret key for added security

mail=Mail(app)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'webprogrammingcoursework2@gmail.com',
    MAIL_PASSWORD = 'cantwaittillchristmas' )
mail = Mail(app)

# read file function and return as a list
def readFile(aFile):
    with open(aFile, 'r') as inFile:
        reader = csv.reader(inFile)
        aList = [row for row in reader]
    return aList


# write 'aList' to 'aFile'
def writeFile(aList, aFile):
    with open(aFile, 'w', newline='') as outFile:
        writer = csv.writer(outFile)
        writer.writerows(aList)
    return


# extracts dates from a list and returns them in formatted standard
def formatDates(aList, column):
    dates = []
    for row in aList:
        parsedDate = time.strptime(row[column], "%Y-%m-%d")
        formattedDate = time.strftime("%d %B %Y", parsedDate)
        dates.append(formattedDate)

    return dates


# Function that tests if the start or end date overlaps with existing bookings. Returns True if overlap present
# False if no overlap
def dateValidator(startDate, endDate):
    rentalArray = list(csv.reader(open(r'static/csv/rentals.csv')))  # Quick read function
    for row in rentalArray:
        startDateFile = row[2]
        endDateFile = row[3]
        return ((startDateFile <= startDate <= endDateFile) or (startDateFile <= endDate <= endDateFile))


# Function to convert numbers to uppercase strings related to that number and returns it
def numToString(argument):
    switcher = {
        1: "ONE", 2: "TWO", 3: "THREE",
        4: "FOUR", 5: "FIVE", 6: "SIX", 7: "SEVEN", 8: "EIGHT", 9: "NINE"
    }
    return switcher.get(argument, "nothing")


# Function which generates two integers in range 1 to 5.
# Creates a formatted string by using the numToString function and returns it
# The function also returns  the answer to the current maths problem
def antiSpamGenerator():
    num1 = random.randint(1, 5)
    num2 = random.randint(1, 5)
    generatedQuestion = "{} + {} = ".format(numToString(num1), numToString(num2))
    spamAnsw = num1 + num2
    stringAnsw = numToString(spamAnsw)
    return generatedQuestion, stringAnsw


generatedAnt, spamAnsw = antiSpamGenerator()


# Code for rendering all pages
@app.route("/")
def homePage():
    rentalFile = 'static\csv\\rentals.csv'
    rentalList = readFile(rentalFile)
    allStartDate = formatDates(rentalList, 2)
    allEndDate = formatDates(rentalList, 3)
    return render_template("index.html", allStartDate=allStartDate, allEndDate=allEndDate, generatedAnti=generatedAnt)


@app.route("/detailsPage")
def detailsPage():
    rentalFile = 'static\csv\\rentals.csv'
    rentalList = readFile(rentalFile)

    allStartDate = formatDates(rentalList, 2)
    allEndDate = formatDates(rentalList, 3)
    return render_template("details.html", allStartDate=allStartDate, allEndDate=allEndDate, generatedAnti=generatedAnt)


@app.route("/directionsPage")
def directionsPage():
    rentalFile = 'static\csv\\rentals.csv'
    rentalList = readFile(rentalFile)

    allStartDate = formatDates(rentalList, 2)
    allEndDate = formatDates(rentalList, 3)
    return render_template("directions.html", allStartDate=allStartDate, allEndDate=allEndDate,
                           generatedAnti=generatedAnt)


@app.route("/nearbyPage")
def nearbyPage():
    rentalFile = 'static\csv\\rentals.csv'
    rentalList = readFile(rentalFile)

    allStartDate = formatDates(rentalList, 2)
    allEndDate = formatDates(rentalList, 3)
    return render_template("nearby.html", allStartDate=allStartDate, allEndDate=allEndDate, generatedAnti=generatedAnt)


# Displays reviews from csv on page load.
@app.route("/reviewsPage", methods=['GET'])
def reviewsPage():
    reviewsFile = 'static\csv\\reviews.csv'
    reviewsList = readFile(reviewsFile)

    rentalFile = 'static\csv\\rentals.csv'
    rentalList = readFile(rentalFile)

    allStartDate = formatDates(rentalList, 2)
    allEndDate = formatDates(rentalList, 3)

    return render_template("reviews.html", reviewsList=reviewsList, allStartDate=allStartDate,
                           allEndDate=allEndDate, generatedAnti=generatedAnt)


# Adds user's review to the CSV file
@app.route('/postComment', methods=['POST'])
def postComment():
    reviewsFile = 'static\csv\\reviews.csv'
    reviewsList = readFile(reviewsFile)
    name = request.form[('commentName')]
    email = request.form[('commentEmail')]
    review = request.form[('review')]
    # stores date in formatted standard
    date = time.strftime("%d %B %Y")

    newPost = [name, email, review, date]
    reviewsList.append(newPost)

    rentalFile = 'static\csv\\rentals.csv'
    rentalList = readFile(rentalFile)

    allStartDate = formatDates(rentalList, 2)
    allEndDate = formatDates(rentalList, 3)

    writeFile(reviewsList, reviewsFile)
    return render_template("reviews.html", reviewsList=reviewsList, allStartDate=allStartDate,
                           allEndDate=allEndDate, generatedAnti=generatedAnt)


# Function to record and process data entered into the FORM
@app.route("/rentalPage", methods=['GET', 'POST'])
def rentalPage():
    rentalFile = 'static\csv\\rentals.csv'
    rentalList = readFile(rentalFile)  # read function initiated

    if request.method == 'POST':  # if the method post is used, carry out code below
        allStartDate = formatDates(rentalList, 2)
        allEndDate = formatDates(rentalList, 3)
        antiSpam = request.form[('antiSpam')]
        antiSpam = antiSpam.upper()  # make user input all uppercase
        name = request.form[('name')]
        email = request.form[('email')]
        startDate = request.form[('startDate')]
        endDate = request.form[('endDate')]
        notes = request.form[('notes')]
        confirmation = False  # confirmation is automatically set to false

        if antiSpam != spamAnsw:  # Condition to check if user answer corresponds with the one generated within the programme
            flash('Wrong anti spam answer. Please try again (Example: FOUR + FOUR = eight)')  # Flash message to display error feedback
            global generatedAnt, spamAnsw  # anti spam test will be changed if the user fails to solve maths problem
            generatedAnt, spamAnsw = antiSpamGenerator()
            return render_template("rental.html", rentalList=rentalList, allStartDate=allStartDate,
                                   allEndDate=allEndDate, generatedAnti=generatedAnt)
        elif dateValidator(startDate, endDate):  # Validate dates funtion initiated
            flash('Oops, looks like the dates overlap with someone else. Please check booked dates and try again.') #error message

        else:
            flash('Your booking has been recorded  and is now pending. You will receive an email confirmation shortly')
            newEntry = [name, email, startDate, endDate, notes, confirmation]
            rentalList.append(newEntry)
            writeFile(rentalList, rentalFile)  # Write to CSV
            subject = "{}  {} ".format('Thank you for your booking', name)
            message = "We hope you will enjoy your stay {}, at our luxurious holiday home" \
                      "\n\n the dates you have booked are, starting from: {}, until: {}" \
                      "\n\n The owner will be in touch with you soon about the payment for your stay (booking status will stay as pending until payment has been complete)" \
                      "\n\n Looking forward to seeing you at Kapalua" \
                      "\n\n All the best! \n Maui Beach team".format(name, startDate, endDate)
            print(email)
            msg = Message(subject, sender='Bob Vibeson', recipients=[email])
            msg.body = message
            mail.send(msg)

    allStartDate = formatDates(rentalList, 2)
    allEndDate = formatDates(rentalList, 3)
    return render_template("rental.html", rentalList=rentalList, allStartDate=allStartDate, allEndDate=allEndDate,
                           generatedAnti=generatedAnt)


# Auto reloads page on modification
if __name__ == "__main__":
    app.run(debug=True)
