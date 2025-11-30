from app import create_app
from app.extensions import db
from app.models.dish import CategoryGroup, DishCategory, Dish, DishUnit
from app.models.user import Waiter, Manager, Cashier, Admin, Customer, Gender, UserRole
from app.models.inventory import Ingredient, IngredientUnit, IngredientCategory
from app.models.order import Regulation
from app.utils import hash_password

app = create_app()

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

    c1 = Customer(
        fullname='Nguyen Trong Tin 1',
        username='test1',
        password=hash_password('1'),
        phone='0123456789'
    )

    a1 = Admin(
        fullname='Admin',
        username='admin1',
        password=hash_password('1'),
        phone='0000000000'
    )

    w1 = Waiter(
        fullname='Nguyen Trong Tin 2',
        username='test2',
        password=hash_password('2'),
        phone='1123456789',
        email='test2@gmail.com',
        dob='2000-11-27',
        gender=Gender.MALE,
        address='123 Doc lap Quan Tan Phu',
        identity_card='112233445566',
        driver_license='112233445567',
        user_role=UserRole.EMPLOYEE
    )

    cs1 = Cashier(
        fullname='Nguyen Trong Tin 3',
        username='test3',
        password=hash_password('3'),
        phone='1223456789',
        email='test3@gmail.com',
        dob='2000-11-24',
        gender=Gender.FEMALE,
        address='123 Luy Ban Bich Quan Tan Phu',
        identity_card='112233445568',
        user_role=UserRole.EMPLOYEE
    )

    m1 = Manager(
        fullname='Nguyen Trong Tin 4',
        username='test4',
        password=hash_password('4'),
        phone='1233456789',
        email='test4@gmail.com',
        dob='1991-11-24',
        gender=Gender.FEMALE,
        address='123 Binh Long Quan Tan Phu',
        identity_card='112233445569',
        graduation_certificate='112233445570',
        user_role=UserRole.EMPLOYEE
    )
    r1 = Regulation(key='SERVICE_FEE_PERCENT',
                    value='0.05')
    r2 = Regulation(key='MAX_QUANTITY',
                    value='10')

    ic1 = IngredientCategory(name='Coffee')

    ic2 = IngredientCategory(name='Syrup')

    ic3 = IngredientCategory(name='Teas')

    i1 = Ingredient(name='Coffee bean',
                    cost=20000,
                    description='Coffee beans from china',
                    unit=IngredientUnit.KG,
                    ingredientCategory_id=1)
    i2 = Ingredient(name='Sugar',
                    cost=12000,
                    description='Sugar from us',
                    unit=IngredientUnit.KG,
                    ingredientCategory_id=2)
    i3 = Ingredient(name='Black tea',
                    cost=100000,
                    description='Tea from Vietnam',
                    unit=IngredientUnit.L,
                    ingredientCategory_id=3)
    i4 = Ingredient(name='Matcha',
                    cost=150000,
                    description='Tea from Japan',
                    unit=IngredientUnit.KG,
                    ingredientCategory_id=3)
    i5 = Ingredient(name='Grenadine',
                    cost=200000,
                    description='Syrup from France',
                    unit=IngredientUnit.L,
                    ingredientCategory_id=2)
    i6 = Ingredient(name='Chocolate bar',
                    cost=250000,
                    description='Chocolate from Germany',
                    unit=IngredientUnit.KG,
                    ingredientCategory_id=1
                    )

    db.session.add_all([cg1, cg2, dc1, dc2, dc3, dc4, dc5,
                        d1, d2, d3, d4, d5, d6, d7, c1, a1, w1, cs1, m1, r1, r2, ic1, ic2, ic3, i1, i2, i3, i4, i5, i6])
    db.session.commit()

    print("✅ Database initialized & seeded.")
