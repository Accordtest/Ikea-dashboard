from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Opdaterede profiler med realistiske produktdata og CO₂-udledning
users = {
    "profil_a": {
        "username": "Jens",
        "password": "test123",
        "purchase_history": [
            {"name": "Xenium kontorstol", "category": "Møbler", "price": 2500, "date": "2024-01-01", "co2": 206},
            {"name": "Billy reol", "category": "Møbler", "price": 500, "date": "2024-01-15", "co2": 40}
        ],
        "rental_history": []
    },
    "profil_b": {
        "username": "Claus",
        "password": "test123",
        "purchase_history": [
            {"name": "Kallax hylde", "category": "Møbler", "price": 700, "date": "2024-01-10", "co2": 60}
        ],
        "rental_history": [
            {"name": "Xenium kontorstol", "category": "Møbler", "rental_period": "12 måneder", "co2": 0.68 * 12}
        ]
    },
    "profil_c": {
        "username": "Gium",
        "password": "test123",
        "purchase_history": [],
        "rental_history": [
            {"name": "Xenium kontorstol", "category": "Møbler", "rental_period": "24 måneder", "co2": 0.68 * 24},
            {"name": "Ivar hylde", "category": "Møbler", "rental_period": "12 måneder", "co2": 0.68 * 12}
        ]
    }
}

def calculate_total_co2(purchase_history, rental_history):
    """Beregner samlet CO₂-aftryk."""
    total = sum(item["co2"] for item in purchase_history) + sum(item["co2"] for item in rental_history)
    return total

def calculate_hypothetical_co2(purchase_history, rental_history):
    """Beregner hypotetisk CO₂-aftryk."""
    purchase_total = sum(item["co2"] for item in purchase_history)
    rental_total = sum(item["co2"] for item in rental_history)
    rental_equiv_purchase = rental_total / 0.68 * 0.99
    purchase_equiv_rental = purchase_total / 0.99 * 0.68

    return {
        "actual_total": purchase_total + rental_total,
        "hypothetical_purchase": purchase_total + rental_equiv_purchase,
        "hypothetical_rental": rental_total + purchase_equiv_rental
    }

def calculate_donation_and_trees(total_co2):
    """Beregner donation og antal træer for CO₂-neutralitet."""
    if total_co2 <= 0:
        return {
            "trees_needed": 0,
            "donation_amount": 0,
            "message": "Tillykke! Du har allerede et CO₂-neutralt regnskab."
        }
    trees_needed = total_co2 / 20  # Ét træ neutraliserer 20 kg CO₂
    donation_amount = trees_needed * 20  # Ét træ koster 20 kr.
    return {
        "trees_needed": round(trees_needed),
        "donation_amount": round(donation_amount, 2),
        "message": f"For at blive CO₂-neutral skal du plante {round(trees_needed)} træer til en pris af {round(donation_amount, 2)} kr."
    }

@app.route("/", methods=["GET", "POST"])
def login():
    """Login-side."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Tjek for bruger
        for profile_key, user_data in users.items():
            if user_data["username"] == username and user_data["password"] == password:
                return redirect(url_for("dashboard", username=profile_key))

        return render_template("login.html", error="Ugyldigt brugernavn eller kodeord.")
    return render_template("login.html", error=None)


@app.route("/dashboard/<username>")
def dashboard(username):
    """Dashboard."""
    user = users.get(username)
    print(f"DEBUG: username = {username}, user = {user}")
    if not user:
        print(f"User not found for username: {username}")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user, username=username)

@app.route("/purchase-history/<username>")
def purchase_history(username):
    """Viser købshistorik for specifik bruger."""
    user = users.get(username)
    if not user:
        return redirect(url_for("login"))
    return render_template("purchase_history.html", purchases=user["purchase_history"], user=user, username=username)

@app.route("/rental-history/<username>")
def rental_history(username):
    """Viser lejehistorik for specifik bruger."""
    user = users.get(username)
    if not user:
        return redirect(url_for("login"))
    return render_template("rental_history.html", rentals=user["rental_history"], user=user, username=username)

@app.route("/co2-account/<username>")
def co2_account(username):
    """CO₂-regnskab."""
    user = users.get(username)
    if not user:
        return redirect(url_for("login"))
    purchase_history = user["purchase_history"]
    rental_history = user["rental_history"]
    total_co2 = calculate_total_co2(purchase_history, rental_history)
    hypothetical_co2 = calculate_hypothetical_co2(purchase_history, rental_history)
    donation_info = calculate_donation_and_trees(total_co2)
    
    # Beregn procent for CO₂-neutralitet
    progress_percentage = max(0, 100 - total_co2)

    return render_template(
        "co2_account.html",
        user=user,
        purchase_data={item["name"]: item["co2"] for item in purchase_history},
        rental_data={item["name"]: item["co2"] for item in rental_history},
        total_co2=total_co2,
        hypothetical_co2=hypothetical_co2,
        donation_info=donation_info,
        progress_percentage=progress_percentage
    )

@app.route("/logout")
def logout():
    """Log ud."""
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
