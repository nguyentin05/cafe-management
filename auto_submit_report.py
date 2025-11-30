from datetime import date
from app import create_app, redis_client, db
from app.models.inventory import InventoryReport, InventoryReportDetail
import json

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        today = date.today().isoformat()
        pattern = f'inventory_report:{today}:*'

        keys = redis_client.keys(pattern)

        for key in keys:
            _, date, waiter_id = key.split(':')
            report_date = date.fromisoformat(date)

            report = InventoryReport(
                created_date=report_date,
                waiter_id=int(waiter_id)
            )

            db.session.add(report)
            db.session.flush()

            redis_data = redis_client.hgetall(key)

            for id, json_str in redis_data.items():
                obj = json.loads(json_str)
                detail = InventoryReportDetail(
                    quantity=obj['quantity'],
                    inventoryReport_id=report.id,
                    ingredient_id=obj['id']
                )
                db.session.add(detail)

            redis_client.delete(key)

        db.session.commit()
