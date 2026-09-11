import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


app.secret_key = "simple-secret-key"


def get_connection():
    
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="rootroot",  
        database="crud_app",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route("/")
def index():
    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("index.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    
    if request.method == "POST":
        name = request.form["name"].strip()
        price_text = request.form["price"].strip()
        quantity_text = request.form["quantity"].strip()

        # Basic validation
        if name == "":
            flash("Product name cannot be empty.")
            return redirect(url_for("add_product"))

        try:
            price = float(price_text)
        except ValueError:
            flash("Price must be a valid number.")
            return redirect(url_for("add_product"))

        try:
            quantity = int(quantity_text)
        except ValueError:
            flash("Quantity must be a valid whole number.")
            return redirect(url_for("add_product"))

        if price < 0:
            flash("Price cannot be negative.")
            return redirect(url_for("add_product"))

        if quantity < 0:
            flash("Quantity cannot be negative.")
            return redirect(url_for("add_product"))

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
            (name, price, quantity)
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Product added successfully!")
        return redirect(url_for("index"))

   
    return render_template("add_product.html")


@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"].strip()
        price_text = request.form["price"].strip()
        quantity_text = request.form["quantity"].strip()

        if name == "":
            flash("Product name cannot be empty.")
            cursor.close()
            connection.close()
            return redirect(url_for("edit_product", product_id=product_id))

        try:
            price = float(price_text)
        except ValueError:
            flash("Price must be a valid number.")
            cursor.close()
            connection.close()
            return redirect(url_for("edit_product", product_id=product_id))

        try:
            quantity = int(quantity_text)
        except ValueError:
            flash("Quantity must be a valid whole number.")
            cursor.close()
            connection.close()
            return redirect(url_for("edit_product", product_id=product_id))

        if price < 0 or quantity < 0:
            flash("Price and quantity cannot be negative.")
            cursor.close()
            connection.close()
            return redirect(url_for("edit_product", product_id=product_id))

        cursor.execute(
            "UPDATE products SET name = %s, price = %s, quantity = %s WHERE id = %s",
            (name, price, quantity, product_id)
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Product updated successfully!")
        return redirect(url_for("index"))

    
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    connection.close()

    if product is None:
        flash("Product not found.")
        return redirect(url_for("index"))

    return render_template("edit_product.html", product=product)


@app.route("/delete/<int:product_id>")
def delete_product(product_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Product deleted successfully!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
