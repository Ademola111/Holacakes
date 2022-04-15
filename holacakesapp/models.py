"""contains the models for the database"""
import datetime
from email.policy import default
from holacakesapp import db

class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)
    user_dob = db.Column(db.DateTime(), nullable=False)
    user_phone = db.Column(db.String(255), nullable=True)
    user_address = db.Column(db.Text(), nullable=False)
    user_gender = db.Column(db.Enum('Male','Female'), nullable=False, server_default=('Male'))
    
    #create the foreign keys
    # user_lgaid = db.Column(db.Integer(), db.ForeignKey("lga.lga_id")) 
    user_stateid = db.Column(db.Integer(), db.ForeignKey("state.state_id"))

    #setup the relationships         
    # mylgaobj = db.relationship('Lga', back_populates ='lgausers')
    mystateobj = db.relationship('State', back_populates='stateusers')
    order_productobj=db.relationship('Order_product', back_populates='user_orderobj')
    paymentobj=db.relationship('Payment', back_populates='userpaymentobj')
    reviewuser=db.relationship('Reviews', back_populates='userreviewobj')
    


class State(db.Model): 
    state_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)
    #set up the relationship
    stateusers = db.relationship('User', back_populates ='mystateobj')

# class Lga(db.Model):
#     lga_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
#     lga_name = db.Column(db.String(255), nullable=False)
#     #foreignkey
#     state_id = db.Column(db.Integer(), db.ForeignKey("state.state_id"))
#     #relationaship
#     lgausers = db.relationship('User', back_populates ='mylgaobj')

class Product(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_no = db.Column(db.Integer(), nullable=False)
    product_size = db.Column(db.Enum('5', '6','7','8','9','10','11','12','13','14','15'), nullable=False)
    product_flavour = db.Column(db.Enum('fundant','butter icing','chocolate','vanilla','strawberry'), nullable=False)
    product_type = db.Column(db.Enum('normal','custom'), nullable=False, server_default=('custom'))
    product_no = db.Column(db.String(255), nullable=True)
    product_description = db.Column(db.String(255), nullable=False)
    product_price = db.Column(db.Integer(), nullable=False)
    product_message = db.Column(db.Text(), nullable=True)
    product_image_url = db.Column(db.String(255), nullable=True)
    #foreignkey
    product_prodcatid = db.Column(db.Integer(), db.ForeignKey("product_cat.product_catid"))
    #relationship
    productcatobj=db.relationship('Product_cat', back_populates='productobj')
    productimageobj=db.relationship('Product_image', back_populates='productobj2')
    reviewproduct=db.relationship('Reviews', back_populates='productrevoewobj')
    orderobj=db.relationship('Order_product', back_populates='productobjs')
    orderdetobj=db.relationship('Order_Details', back_populates='productobs')

class Product_cat(db.Model):
    product_catid = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    product_cat_name = db.Column(db.String(255), nullable=False)
    #relationship
    productobj=db.relationship('Product', back_populates='productcatobj')


class Product_image(db.Model):
    product_imageid = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    # product_image_name = db.Column(db.String(255), nullable=False)
    #foreignkey
    prodimage_productid = db.Column(db.Integer(), db.ForeignKey("product.product_id"))
    prodimage_prodcatid = db.Column(db.Integer(), db.ForeignKey("product_cat.product_catid"))
    #relationship
    productobj2=db.relationship('Product', back_populates='productimageobj')
    

class Order_product(db.Model):
    order_productid=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    order_product_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())    
    order_status = db.Column(db.Enum('pending', 'processed', 'completed'), default='pending')
    #foreignkey
    order_userid = db.Column(db.Integer(), db.ForeignKey("user.user_id"))
    order_product_id = db.Column(db.Integer(), db.ForeignKey("product.product_id"))
    #relationship
    user_orderobj=db.relationship('User', back_populates='order_productobj')
    orderdetailobj=db.relationship('Order_Details', back_populates='myorderobj')
    deliveryobj=db.relationship('Delivery', back_populates='orderprodobj')
    payobj=db.relationship('Payment', back_populates='orderpaymentobj')
    productobjs=db.relationship('Product', back_populates='orderobj')
    

class Order_Details(db.Model):
    order_detailid=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    order_detail_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    orderdetail_amount=db.Column(db.Integer())
    order_detail_Qty = db.Column(db.Integer(), nullable=False)
    order_detail_total_amount = db.Column(db.Integer(), nullable=False)
    VAT = db.Column(db.Float())
    order_shipping_address = db.Column(db.String(255), nullable=False)
    grand_total=db.Column(db.Float())
    
    #foreignkey
    orderdetail_productid = db.Column(db.Integer(), db.ForeignKey("product.product_id"))
    orderdetail_orderproductid = db.Column(db.Integer(), db.ForeignKey("order_product.order_productid"))
    #relationship
    myorderobj=db.relationship('Order_product', back_populates='orderdetailobj')
    productobs=db.relationship('Product', back_populates='orderdetobj')

class Delivery(db.Model):
    delivery_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    delivery_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    delivery_mode=db.Column(db.Enum('pickup','home delivery'))
    delivery_status = db.Column(db.Enum('pending', 'on transit', 'delivered'), server_default='pending')
    #foreignkey
    delivery_orderid = db.Column(db.Integer(), db.ForeignKey("order_product.order_productid"))
    delivery_userid = db.Column(db.Integer(), db.ForeignKey("user.user_id"))
    #relationship
    orderprodobj=db.relationship('Order_product', back_populates='deliveryobj')
    deliveryuserobj=db.relationship('User', backref='userdeet')

class Payment(db.Model):
    payment_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    payment_transNo=db.Column(db.Integer(), nullable=True)
    payment_transdate=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    payment_amount=db.Column(db.Float(), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'paid', 'failed'), server_default='pending')
    #foreignkey
    payment_userid = db.Column(db.Integer(), db.ForeignKey("user.user_id"))
    payment_orderid = db.Column(db.Integer(), db.ForeignKey("order_product.order_productid"))
    #relationship
    userpaymentobj=db.relationship('User', back_populates='paymentobj')
    orderpaymentobj=db.relationship('Order_product', back_populates='payobj')

class Reviews(db.Model):
    reviews_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    reviews_comment=db.Column(db.Text(), nullable=False)
    reviews_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #foreignkey
    reviews_userid=db.Column(db.Integer(), db.ForeignKey("user.user_id"))
    reivews_productid=db.Column(db.Integer(), db.ForeignKey("product.product_id"))

    #relationship
    userreviewobj=db.relationship('User', back_populates='reviewuser')
    productrevoewobj=db.relationship('Product', back_populates='reviewproduct')

class Admin(db.Model):
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_fname = db.Column(db.String(255), nullable=False)
    admin_lname = db.Column(db.String(255), nullable=False)
    admin_email = db.Column(db.String(255), nullable=False)
    admin_pass = db.Column(db.String(255), nullable=False)
    admin_phone = db.Column(db.String(255), nullable=True)
    admin_address = db.Column(db.Text(), nullable=False)
    admin_gender = db.Column(db.Enum('Male','Female'), nullable=False, server_default=('Male'))

class Profile_pic(db.Model):
    pic_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    pic_url = db.Column(db.String(255), nullable=True)
    #foreignkey
    pic_userid = db.Column(db.Integer(), db.ForeignKey("product.product_id"))
    
    
