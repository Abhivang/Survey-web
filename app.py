from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure, random key

# Survey questions
questions = [
    {
        "Claim": "Trump's claim: Kamala Harris “wants to forcibly compel doctors and nurses against their will to give chemical castration drugs to young children.”",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "Harris support for prisoner access to transgender surgery aligns with federal law and court rulings. Kamala Harris “supports taxpayer-funded sex changes for prisoners and illegal aliens.”",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "Kamala Harris on Project 2025 limiting access to IVF, contraception. Project 2025 calls for restricting “access to IVF and contraception.”",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "Vice President Kamala Harris “cast the tiebreaking votes that caused the worst inflation in American history, costing a typical American family $28,000,” stated by Trump.",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "“As of today, there is not one member of the United States military who is in active duty in a combat zone, in any war zone around the world, for the first time this century,” stated by Harris.",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "Donald Trump mentioned ending the Affordable Care Act and, when confronted, denied it.",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "More people were drawn to MLK's I Have a Dream speech compared to Trump's Jan 6 speech, regardless of what Trump said or believed.",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "Trump called Kamala Harris a communist and a Marxist. Vice President Kamala Harris “is a communist. … She is really a Marxist,” stated by Donald Trump.",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "Kamala Harris assigned to tackle immigration causes, not border security. President Joe Biden appointed Kamala Harris to be his border czar to deal with illegal immigration … Harris was put in charge of stopping illegal immigration.",
        "Your Opinion": ["True", "False"],
    },
    {
        "Claim": "The Trump administration added more to the national debt than any presidential term in American history, Joe Biden stated.",
        "Your Opinion": ["True", "False"],
    },
]

responses = []

# Admin credentials
ADMIN_USERNAME = "aditi"
ADMIN_PASSWORD = "aditi"  # Replace with a secure password

@app.route("/", methods=["GET"])
def start_survey():
    return render_template("start_survey.html")

@app.route("/questions", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        responses.append(request.form)
        return redirect(url_for("thank_you"))
    return render_template("questions.html", questions=questions)

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")  # Display only a thank-you message

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("view_results"))
        else:
            return "Invalid credentials", 403
    return render_template("admin_login.html")  # Login form for admin

@app.route("/results")
def view_results():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    results = {}
    totals = {}

    # Initialize results and totals for each claim
    for question in questions:
        totals[question["Claim"]] = 0
        for opinion in question["Your Opinion"]:
            results.setdefault(question["Claim"], {}).setdefault(opinion, 0)

    # Count responses
    for response in responses:
        for claim, answer in response.items():
            results[claim][answer] += 1
            totals[claim] += 1

    # Calculate percentages
    percentages = {}
    for claim, opinions in results.items():
        percentages[claim] = {
            opinion: (count / totals[claim] * 100) if totals[claim] > 0 else 0
            for opinion, count in opinions.items()
        }

    return render_template("results.html", percentages=percentages)

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("start_survey"))

if __name__ == "__main__":
    app.run(debug=True)
