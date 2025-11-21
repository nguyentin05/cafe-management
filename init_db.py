from app import app, db
from app.models import CategoryGroup, DishCategory, Dish, DishUnit

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        cg1 = CategoryGroup(name='Foods')
        cg2 = CategoryGroup(name='Drinks')

        dc1 = DishCategory(name='Latte',         categoryGroup_id=2)
        dc2 = DishCategory(name='Hot Coffee',    categoryGroup_id=2)
        dc3 = DishCategory(name='Breakfast',     categoryGroup_id=1)
        dc4 = DishCategory(name='Hot Chocolate', categoryGroup_id=2)
        dc5 = DishCategory(name='Bakery',        categoryGroup_id=1)

        d1 = Dish(
            name='Latte', price=40000,
            image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762667757/kices3owtzqzhhxqshie.jpg',
            unit=DishUnit.CUP, dishCategory_id=1
        )
        d2 = Dish(
            name='Americano', price=40000,
            image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668228/nk9biuw7piporcr5ykoa.jpg',
            unit=DishUnit.CUP, dishCategory_id=2
        )
        d3 = Dish(
            name='Matcha Latte', price=40000,
            image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668374/nlai0rzggdsex7bu0mxe.jpg',
            unit=DishUnit.CUP, dishCategory_id=1
        )
        d4 = Dish(
            name='Croissant', price=40000,
            image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668533/qbnmz5iknk5dvuxfb8od.jpg',
            unit=DishUnit.PIECE, dishCategory_id=5
        )
        d5 = Dish(
            name='Bacon Gouda Egg Sandwich', price=40000,
            image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668577/uu2adt55oktzh93j9zlb.jpg',
            unit=DishUnit.PIECE, dishCategory_id=3
        )
        d6 = Dish(
            name='Cappuccino', price=40000,
            image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668604/xvifqkcn1ukgexznfpby.jpg',
            unit=DishUnit.CUP, dishCategory_id=2
        )
        d7 = Dish(
            name='Egg Pesto Mozzarella Sandwich', price=40000,
            image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668656/yxfejhpbb4g3svpgtsvq.jpg',
            unit=DishUnit.PIECE, dishCategory_id=3
        )

        db.session.add_all([cg1, cg2, dc1, dc2, dc3, dc4, dc5,
                            d1, d2, d3, d4, d5, d6, d7])
        db.session.commit()

        print("✅ Database initialized & seeded.")
