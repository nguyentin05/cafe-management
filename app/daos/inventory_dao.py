from flask_login import current_user

from app import db
from app.models import Ingredient, GoodsReceiptNote, NoteDetail, InventoryReport, InventoryReportDetail


def load_ingredients():
    return Ingredient.query.all()

def add_note(note):
    if not note:
        raise ValueError("Note is empty")

    try:
        grn = GoodsReceiptNote(
            waiter_id=current_user.id
        )
        db.session.add(grn)
        db.session.flush()

        for i in note.values():
            nd = NoteDetail(note_id=grn.id,
                            ingredient_id=i['id'],
                            quantity=i['quantity'],
                            unit_cost=i['cost'])
            db.session.add(nd)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in add_note:', e)
        raise e

def add_report(report):
    if not report:
        raise ValueError("Report is empty")

    try:
        rpt = InventoryReport(
            waiter_id=current_user.id
        )
        db.session.add(rpt)
        db.session.flush()

        for r in report.values():
            ird = InventoryReportDetail(inventoryReport_id=rpt.id,
                            ingredient_id=r['id'],
                            quantity=r['quantity'])
            db.session.add(ird)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in add_report:', e)
        raise e