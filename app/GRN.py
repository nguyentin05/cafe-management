from flask import Flask, render_template, request, redirect, url_for
from models import db, Ingredient, GoodsReceiptNote, NoteType
from datetime import date

app = Flask(__name__)

@app.route("/goods-receipt/new", methods=["GET", "POST"])
def create_goods_receipt():
    ingredients = Ingredient.query.all() 
    
    if request.method == "POST":
        ingredient_id = request.form["ingredient_id"]   
        ingredient = Ingredient.query.get(ingredient_id)

        quantity = float(request.form["quantity"])
        unit = request.form["unit"]

        note = GoodsReceiptNote(
            ingredient_name=ingredient.name,
            unit=unit,
            quantity=quantity,
            date_created=date.today(),
            type=NoteType.GOODS_RECEIPT
        )

        db.session.add(note)
        db.session.commit()

        return redirect(url_for("create_goods_receipt"))

    receipts = GoodsReceiptNote.query.filter_by(type=NoteType.GOODS_RECEIPT).all()
    return render_template("goods_receipt_form.html", ingredients=ingredients, receipts=receipts)
