import os, math, random
from sqlalchemy import desc
from flask import make_response, render_template, request, redirect, url_for,flash, session 

from werkzeug.security import generate_password_hash, check_password_hash

from holacakesapp import app,db
from holacakesapp.models import Admin, Order_Details, Order_product, Product_image, Product_cat, Product, Payment, User, Profile_pic, Reviews, Delivery
#from holacakesapp.forms import LoginForm

"""admin login"""
@app.route('/admin/')
def admin_login():
    return render_template('admin/admin_login.html')

"""admin login submit"""
@app.route('/admin/submit/', methods=['POST'])
def admin_login_submit():
    email=request.form.get('email')
    pwd=request.form.get('password')

    #validation on submit
    if email=="" or pwd=="": #note database has not been created.
        flash('ensure to fill all the fields')
        return redirect('/admin/')

    if email !="" or pwd != "":
        adm=db.session.query(Admin).filter(Admin.admin_email==email).first()
        formated_pwd=adm.admin_pass
        chk=check_password_hash(formated_pwd, pwd)
        if chk:
            session['adminlogin']=adm.admin_id
            return redirect(url_for('admin_dashboard'))
        else:
            flash('kindly supply a valid email address and password ')
            return redirect('/admin/')
    else:
        flash('You have provided an invalid credentials')
        return redirect('/admin/')

""" Admin Dashboard submit"""
@app.route('/admin/dashboard/')
def admin_dashboard():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        category=Product_cat.query.all()
        allprod=Product.query.all()
        det=Order_Details.query.all()
        admorder=Order_product.query.all()
        owo=Payment.query.all()
        user=User.query.all()
        rev=Reviews.query.all()
        delv=Delivery.query.all()
        img=Profile_pic.query.all()
        return render_template('admin/admin_dashboard.html', category=category, allprod=allprod, det=det, admorder=admorder, owo=owo, user=user, rev=rev, delv=delv, img=img)

""" Admin signup """
@app.route('/admin/signup/')
def admin_signup():
    admin=session.get('adminlogin')
    if request.method=='GET':
        return redirect('/admin')
    if admin==None:
        return redirect('/admin/')
    else:
        return render_template('admin/admin_signup.html')

""" Admin signup submit"""
@app.route('/admin/signup/', methods=['POST'])
def admin_signup_submit():
    admin_fname = request.form.get('fname')
    admin_lname = request.form.get('lname')
    admin_email = request.form.get('email')
    admin_pass = request.form.get('password')
    admin_confirmpassword = request.form.get('confirmpassword')
    admin_phone = request.form.get('phoneno')
    admin_address = request.form.get('address')
    admin_gender = request.form.get('gender')
    
    # regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    # if re.fullmatch(regex, user_email):

    if admin_fname=="" or admin_lname=="" or admin_email=="" or admin_pass=="" or admin_confirmpassword=="" or admin_phone=="" or admin_address=="" or admin_gender=="":
        flash('Validation faild')
        return redirect('/admin/signup/')
    
    elif admin_pass != admin_confirmpassword:
        flash('invalid credentials')
        return redirect('/admin/signup/')
    else:
        formated = generate_password_hash(admin_pass)
        ok=Admin(admin_fname=admin_fname, admin_lname=admin_lname, admin_email=admin_email,admin_pass=formated, admin_phone=admin_phone, admin_address=admin_address, admin_gender=admin_gender)
        db.session.add(ok)
        db.session.commit()
        id=ok.admin_id
        session['Adminlogin']=id
        flash('Welcome onboard')
        return redirect('/admin/')
   
    # return render_template('admin/admin_signup.html')

"""admin products"""
@app.route('/admin/products/')
def admin_product():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        category=Product_cat.query.all()
        allprod=Product.query.all()
        return render_template('admin/list_product.html', allprod=allprod, category=category)

"""product submit"""
@app.route('/admin/submit/products/', methods=['POST'])
def submit_admin_product():
    name=request.form.get('cakename') #category id, also as cake name
    size=request.form.get('cakesize')
    flavour=request.form.get('cakeflavour')
    ordertype=request.form.get('order')
    description=request.form.get('description')
    message=request.form.get('cakemessage')
    category=request.form.get('cakecat')
    productno=request.form.get('productno')
    price=request.form.get('price')

    if name=="" or size=="" or flavour=="" or ordertype=="" or description=="" or message=="" or category=="" or productno=="" or price=="":
        flash('one or more field is empty')
        return render_template('admin/list_product.html')
    else:
        #requesting image from form
        image=request.files.get('filename')
        original_name = image.filename
        #checking if file is not empty
        if original_name !="":
            extension = os.path.splitext(original_name)
            if extension[1].lower() in ['.jpg','.png','gif']:
                fn=math.ceil(random.random()*10000000000)
                save_as=str(fn)+extension[1]
                image.save(f'holacakesapp/static/images/{save_as}')
                
                k=Product(product_name=name, product_size=size, product_flavour=flavour, product_type=ordertype, product_description=description, product_message=message, product_prodcatid=category, product_no=productno, product_price=price, product_image_url=save_as)
                db.session.add(k)
                db.session.commit()
                flash('Product Added successfully')
                return redirect('/admin/products/')
            else:
                flash("File Type Not Allowed")
                return redirect("/admin/products/")
        else:
            #if no picture supplied
            save_as==""

            k=Product(product_name=name, product_size=size, product_flavour=flavour, product_type=ordertype, product_description=description, product_message=message, product_prodcatid=category, product_no=productno, product_price=price, product_image_url=save_as)
            db.session.add(k)
            db.session.commit()
            flash('Product Added successfully')
            return redirect('/admin/products/')

"""admin products categories"""
@app.route('/admin/products/categories/')
def admin_categories():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        cati=Product_cat.query.all()
        return render_template('admin/admin_categories.html', cati=cati)

"""submit category"""
@app.route('/admin/products/categories/', methods=['POST'])
def submit_admin_categories():
    admin= session.get('adminlogin')
    if admin == None:
        return redirect('/admin/')
    else:
        addcat=request.form.get('addcategory')

        #checking if title and level is empty
        if addcat=="":
            flash('Category name cannot be empty')
            return redirect('/admin/dashboard/')
        else:        
            #inserting into the database
            bc = Product_cat(product_cat_name=addcat)
            db.session.add(bc)
            db.session.commit()
            flash('Successfully add category')
            return redirect('/admin/products/categories/')

"""admin images"""
@app.route('/admin/profile/picture/')
def admin_images():
    admin= session.get('adminlogin')
    if admin == None:
        return redirect('/admin/')
    else:
        cati=Product_cat.query.all()
        img=db.session.execute("SELECT * FROM `profile_pic` JOIN `user` WHERE pic_userid=user_id")
        return render_template('admin/admin_images.html', img=img, cati=cati)

# """admin images"""
# @app.route('/admin/products/addimages/', methods=['POST'])
# def add_images():
#     admin= session.get('adminlogin')
#     if admin == None:
#         return redirect('/admin/')
#     else:
#         imgcat=request.form.get('cat')
#         title=request.form.get('img')

#         #requesting image from form
#         image=request.files.get('filename')
#         original_name = image.filename

#         #checking if title and level is empty
#         if title=="" or imgcat=="":
#             flash('field cannot be empty')
#             return redirect('/admin/products/addimages/')

#             #checking if file is not empty
#         if original_name !="":
#             extension = os.path.splitext(original_name)
#             if extension[1].lower() in ['.jpg','.png','gif']:
#                 fn=math.ceil(random.random()*10000000000)
#                 save_as=str(fn)+extension[1]
#                 image.save(f'holacakesapp/static/images/{save_as}')
                    
#                 #inserting into the database
#                 b = Product_image(product_image_name=title, product_image_url=save_as, prodimage_prodcatid=imgcat)
#                 db.session.add(b)
#                 db.session.commit()
#                 flash('image added successfully')
#                 return redirect("/admin/products/images/")
#             else:
#                 flash("File Type Not Allowed")
#                 return redirect("/admin/products/addimages/")
#         else:
#             #if no picture supplied
#             save_as==""
                    
#             #inserting into the database
#             b = Product_image(product_image_name=title, product_image_url=save_as)
#             db.session.add(b)
#             db.session.commit()
#             return render_template('admin/admin_images.html', admin=admin)

    # return render_template('admin/admin_images.html')
    
"""admin products order"""
@app.route('/admin/products/order/')
def admin_orderproduct():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        admorder=Order_product.query.order_by(desc(Order_product.order_product_date)).all()
        return render_template('admin/admin_orderproduct.html', admorder=admorder)

"""admin products order detail"""
@app.route('/admin/products/order/detail/')
def admin_orderdetail():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        det=Order_Details.query.join(Order_product).add_columns(Order_product).order_by(desc(Order_Details.order_detail_date)).all()
        return render_template('admin/admin_orderdetail.html', det=det)

"""update order status"""
@app.route('/update/orderstatus', methods=['POST'])
def update_status():
    statu=request.form.get('status')
    productid=request.form.get('productid')
    stat=Order_product.query.filter(Order_product.order_productid==productid).first()
    stat.order_status=statu
    # db.session.execute(f"UPDATE `order_product` SET `order_status` = 'completed' WHERE `order_product`.`order_productid` = order_productid")
    db.session.commit()
    flash("status updated successfully")
    return redirect('/admin/products/order/detail/')
    


"""admin products order detail"""
@app.route('/admin/products/delivery/')
def admin_delivery():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        delv=Delivery.query.join(User).add_columns(User).order_by(desc(Delivery.delivery_id)).all()
        return render_template('admin/admin_delivery.html', delv=delv)

"""admin products order detail"""
@app.route('/admin/update/delivery/', methods=['POST'])
def admin_delivery_status():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    if request.method=='POST':
        delivery_id=request.form.get('delivery')
        status=request.form.get('deliverystatus')
        delv=Delivery.query.filter(Delivery.delivery_id==delivery_id).first()
        delv.delivery_status=status
        db.session.commit()
        flash("status updated successfully")
        return redirect('/admin/products/delivery/')

"""admin products order detail"""
@app.route('/admin/products/payment/')
def admin_payment():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        owo=Payment.query.order_by(desc(Payment.payment_transdate)).all()
        return render_template('admin/admin_payment.html', owo=owo)

"""admin products reviews"""
@app.route('/admin/products/reviews/')
def admin_reviews():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        rev=Reviews.query.all()
        return render_template('admin/admin_reviews.html', rev=rev)

"""admin products reviews"""
@app.route('/admin/user/')
def admin_user():
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        user=User.query.all()
        return render_template('admin/admin_user.html', user=user)

"""Error 404 page"""
@app.errorhandler(404)
def page_not_found(error):
    admin=session.get('adminlogin')
    if admin==None:
        return redirect('/admin/')
    else:
        return render_template('admin/error.html', error=error),404