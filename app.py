from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Realistisk data og CO2-udregninger
data = {
    "purchase_history": [
        {"name": "Billy reol", "category": "Møbler", "price": 499, "date": "2024-01-01", "co2": 40},
        {"name": "Lack sofabord", "category": "Møbler", "price": 299, "date": "2024-01-10", "co2": 15},
        {"name": "Kallax hylde", "category": "Møbler", "price": 699, "date": "2024-01-20", "co2": 60}
    ],
    "rental_history": [
        {"name": "Poäng lænestol", "category": "Møbler", "rental_period": "3 måneder", "co2": -10},
        {"name": "Malm seng", "category": "Møbler", "rental_period": "6 måneder", "co2": -25},
        {"name": "Ivar hylde", "category": "Møbler", "rental_period": "12 måneder", "co2": -40}
    ]
}

def calculate_total_co2(purchases, rentals):
    """Beregner det samlede CO2-aftryk."""
    total_co2 = sum(item["co2"] for item in purchases) + sum(item["co2"] for item in rentals)
    return total_co2

# Route til login-siden
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Simuleret login - brugeren sendes til dashboardet uanset input
        return redirect(url_for("dashboard"))
    return render_template("login.html")

# Route til dashboardet
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Route til købshistorik
@app.route("/purchase-history")
def purchase_history():
    return render_template("purchase_history.html", purchases=data["purchase_history"])

# Route til lejehistorik
@app.route("/rental-history")
def rental_history():
    return render_template("rental_history.html", rentals=data["rental_history"])

# Route til CO2-regnskab
@app.route("/co2-account")
def co2_account():
    # Saml data for cirkel- og søjlediagrammet
    purchase_data = {item["name"]: item["co2"] for item in data["purchase_history"]}
    rental_data = {item["name"]: item["co2"] for item in data["rental_history"]}
    total_co2 = calculate_total_co2(data["purchase_history"], data["rental_history"])
    return render_template(
        "co2_account.html",
        purchase_data=purchase_data,
        rental_data=rental_data,
        total_co2=total_co2
    )

if __name__ == "__main__":
    app.run(debug=True)
