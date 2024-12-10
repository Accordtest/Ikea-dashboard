from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Profildata med brugernavn og kodeord
users = {
    "profil_a": {
        "username": "Jens",
        "password": "test123",
        "purchase_history": [
            {"name": "Billy reol", "category": "Møbler", "price": 499, "date": "2024-01-01", "co2": 40},
            {"name": "Lack sofabord", "category": "Møbler", "price": 299, "date": "2024-01-10", "co2": 15}
        ],
        "rental_history": []
    },
    "profil_b": {
        "username": "Claus",
        "password": "test123",
        "purchase_history": [
            {"name": "Kallax hylde", "category": "Møbler", "price": 699, "date": "2024-01-20", "co2": 60}
        ],
        "rental_history": [
            {"name": "Poäng lænestol", "category": "Møbler", "rental_period": "3 måneder", "co2": -10}
        ]
    },
    "profil_c": {
        "username": "Gium",
        "password": "test123",
        "purchase_history": [],
        "rental_history": [
            {"name": "Malm seng", "category": "Møbler", "rental_period": "6 måneder", "co2": -25},
            {"name": "Ivar hylde", "category": "Møbler", "rental_period": "12 måneder", "co2": -40}
        ]
    }
}

def calculate_total_co2(purchase_history, rental_history):
    """Beregner samlet CO₂-aftryk."""
    total = sum(item["co2"] for item in purchase_history) + sum(item["co2"] for item in rental_history)
    return total

def calculate_donation_and_trees(co2_footprint):
    """Beregner donation og antal træer for CO₂-neutralitet."""
    if co2_footprint <= 0:
        return {
            "trees_needed": 0,
            "donation_amount": 0,
            "message": "Tillykke! Du har allerede et CO₂-neutralt regnskab."
        }
    trees_needed = co2_footprint / 20  # Ét træ neutraliserer 20 kg CO₂
    donation_amount = trees_needed * 20  # Ét træ koster 20 kr.
    return {
        "trees_needed": round(trees_needed),
        "donation_amount": round(donation_amount, 2),
        "message": f"For at blive CO₂-neutral skal du plante {round(trees_needed)} træer til en pris af {round(donation_amount, 2)} kr."
    }

@app.route("/", methods=["GET", "POST"])
def login():
    """Login-side med brugernavn og kodeord."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Tjek om brugernavn og kodeord matcher en profil
        for profile, user_data in users.items():
            if user_data["username"] == username and user_data["password"] == password:
                return redirect(url_for("dashboard", username=profile))

        return render_template("login.html", error="Ugyldigt brugernavn eller kodeord.")
    return render_template("login.html", error=None)

@app.route("/dashboard/<username>")
def dashboard(username):
    """Dashboard for specifik bruger."""
    user = users.get(username)
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=username)

@app.route("/purchase-history/<username>")
def purchase_history(username):
    """Viser købshistorik for specifik bruger."""
    user = users.get(username)
    if not user:
        return redirect(url_for("login"))
    return render_template("purchase_history.html", purchases=user["purchase_history"], username=username)

@app.route("/rental-history/<username>")
def rental_history(username):
    """Viser lejehistorik for specifik bruger."""
    user = users.get(username)
    if not user:
        return redirect(url_for("login"))
    return render_template("rental_history.html", rentals=user["rental_history"], username=username)

@app.route("/co2-account/<username>")
def co2_account(username):
    """Viser CO₂-regnskab for specifik bruger."""
    user = users.get(username)
    if not user:
        return redirect(url_for("login"))
    purchase_history = user["purchase_history"]
    rental_history = user["rental_history"]
    total_co2 = calculate_total_co2(purchase_history, rental_history)
    donation_info = calculate_donation_and_trees(total_co2)

    purchase_data = {item["name"]: item["co2"] for item in purchase_history}
    rental_data = {item["name"]: item["co2"] for item in rental_history}
    return render_template(
        "co2_account.html",
        username=username,
        purchase_data=purchase_data,
        rental_data=rental_data,
        total_co2=total_co2,
        donation_info=donation_info
    )

@app.route("/logout")
def logout():
    """Log ud og send brugeren tilbage til login-siden."""
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
