from flask_login import current_user
from sqlalchemy import cast, Date, extract, func

from app import db
from app.models import Ingredient, GoodsReceiptNote, NoteDetail, InventoryReport, InventoryReportDetail, Note


def load_ingredients():
    return Ingredient.query.all()


def add_note(note):
    if not note:
        raise ValueError("Note is empty")

    try:
        grn = GoodsReceiptNote()
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
        rpt = InventoryReport()
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


def get_grn_by_ingredient_id(id, day):
    return (NoteDetail.query.join(GoodsReceiptNote)
            .filter(NoteDetail.ingredient_id == id,
                    cast(GoodsReceiptNote.created_date, Date) == day
                    ).first())


def get_grn_by_day(day):
    query = db.session.query(NoteDetail.ingredient_id, func.sum(NoteDetail.quantity)) \
        .join(Note, Note.id == NoteDetail.note_id) \
        .filter(cast(Note.created_date, Date) == day) \
        .group_by(NoteDetail.ingredient_id).all()

    return {r[0]: r[1] for r in query}


def get_report_by_day(day):
    query = db.session.query(InventoryReportDetail.ingredient_id, func.sum(InventoryReportDetail.quantity)) \
        .join(InventoryReport, InventoryReport.id.__eq__(InventoryReportDetail.inventoryReport_id)) \
        .filter(cast(InventoryReport.created_date, Date).__eq__(day)) \
        .group_by(InventoryReportDetail.ingredient_id).all()

    return {r[0]: r[1] for r in query}

def get_ingredient_by_id(id):
    return Ingredient.query.get(id)
