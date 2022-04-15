import random, json, math, os
import requests
import re
from sqlalchemy import desc
from flask import make_response, render_template, request, redirect, url_for,flash, session 

from werkzeug.security import generate_password_hash, check_password_hash

from holacakesapp import app, db
from holacakesapp.models import Order_Details, Payment, Reviews, State, User, Product_cat, Product, Order_product, Profile_pic, Delivery
#from holacakesapp.forms import LoginForm

"""Home page view"""
@app.route('/')
@app.route('/home/')
def home():
    loggedin=session.get('user')
    allprod = Product.query.all()
    dir=Product_cat.query.all()
    return render_template('user/index.html', dir=dir, allprod=allprod, loggedin=loggedin )

"""about us page view"""
@app.route('/about/us/')
def about():
    return render_template('user/about.html')

"""signup view page"""
@app.route('/signup/')
def signup():
    loggedin=session.get('user')
    state = State.query.all()
    dir=Product_cat.query.all()
    return render_template('user/signup.html', state=state, loggedin=loggedin, dir=dir)

"""signup/submit view page"""
@app.route('/submit/signup/', methods=['POST'])
def submit_signup():
    user_fname = request.form.get('fname')
    user_lname = request.form.get('lname')
    user_email = request.form.get('email')
    user_pass = request.form.get('password')
    user_confirmpassword = request.form.get('confirmpassword')
    user_dob = request.form.get('date')
    user_phone = request.form.get('phone')
    user_address = request.form.get('address')
    user_gender = request.form.get('gender')
    user_state = request.form.get('state')
    
    
    # regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    # if re.fullmatch(regex, user_email):

    if user_fname=="" or user_lname=="" or user_email=="" or user_pass=="" or user_confirmpassword=="" or user_dob=="" or user_phone=="" or user_address=="" or user_gender=="" or user_state=="":
        flash('Validation faild')
        return redirect('/signup/')
    
    elif user_pass != user_confirmpassword:
        flash('invalid credentials')
        return redirect('/signup/')
    else:
        formated = generate_password_hash(user_pass)
        k=User(user_fname=user_fname, user_lname=user_lname, user_email=user_email,user_pass=formated,user_dob=user_dob, user_phone=user_phone, user_address=user_address, user_gender=user_gender, user_stateid=user_state)
        db.session.add(k)
        db.session.commit()
        id=k.user_id
        session['loggedin']=id
        flash('Welcome onboard')
        return redirect('/login/')
    # return render_template('user/signup.html') #this will be deleted once database is created

"""login page view"""
@app.route('/login/')
def login():
    loggedin=session.get('user')
    dir=Product_cat.query.all()
    return render_template('user/login.html', loggedin=loggedin, dir=dir)

"""submit login/submit page view"""
@app.route('/submit/login/', methods=['POST'])
def submit_login():
    email=request.form.get('email')
    pwd = request.form.get('password')

    #validation on submit
    if email=="" or pwd=="": #note database has not been created.
        flash('ensure to fill all the fields')
        return redirect('/login/')
    if email !="" or pwd != "":
        users=User.query.filter(User.user_email==email).first()
        formated_pwd=users.user_pass
        chk = check_password_hash(formated_pwd, pwd)
        if chk:
            session['user']=users.user_id
            return redirect('/profile/')
        else:
            flash('kindly supply a valid email address and password ')
            return redirect('/login/')
    else:
        flash('You have provided an invalid credentials')
        return redirect('/login/') #this will be remove once database is activavted

"""logout session"""
@app.route('/user/logout')
def userlogout():
    session.get('user')
    session.pop('shoppingcart', None)
    session.pop('user')
    return redirect('/login/')

"""profile view page"""
@app.route('/profile/')
def profile():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    else:
        user=User.query.get(loggedin)
        pic=Profile_pic.query.filter(Profile_pic.pic_userid==user.user_id).limit(1).all()
        dir=Product_cat.query.all()
        state=State.query.all()
        return render_template('user/profile.html', loggedin=loggedin, dir=dir, user=user, state=state, pic=pic)

"""update profile"""
@app.route('/user/update/profile/', methods=['POST', 'GET'])
def update_profile():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    if request.method=='GET':
        return redirect('/')
    if request.method=='POST':
        user=User.query.get(loggedin)
        user.user_fname = request.form.get('fname')
        user.user_lname = request.form.get('lname')
        user.user_email = request.form.get('email')
        user. user_pass = request.form.get('password')
        user.user_phone = request.form.get('phone')
        user.user_address = request.form.get('address')
        user.user_state = request.form.get('state')
        db.session.commit()
        flash('Profile updated successfully')
        return redirect('/profile/')

"""custom view page"""
@app.route('/custom/')
def custom():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/user/signup')
    else:
        user=User.query.get(loggedin)
        dir=Product_cat.query.all()
        pic=Profile_pic.query.filter(Profile_pic.pic_userid==user.user_id).limit(1).all()
        user_productcatid=Product_cat.query.all()
        return render_template('user/custom.html', user_productcatid=user_productcatid, loggedin=loggedin, dir=dir, pic=pic)

@app.route('/submitcustom/', methods=['POST'])
def submit_custom():
    name=request.form.get('cakename') #category id, also as cake name
    size=request.form.get('cakesize')
    flavour=request.form.get('cakeflavour')
    ordertype=request.form.get('order')
    description=request.form.get('description')
    message=request.form.get('cakemessage')
    productcatid=request.form.get('cakecat')


    if name=="" or size=="" or flavour=="" or ordertype=="" or description=="" or message=="" or productcatid=="":
        return render_template('user/custom.html')
    else:
        k=Product(product_name=name, product_size=size, product_flavour=flavour, product_type=ordertype, product_description=description, product_message=message, user_productcatid=productcatid)
        db.session.add(k)
        db.session.commit()
        flash('Order completed, await a call from one of our representative for order confirmation')
        return redirect('/profile')
    # return render_template('user/custom.html')

"""birthday view page"""
@app.route('/product/<variable>/<id>')
def birthday(variable, id):
    dir=Product_cat.query.all()
    biri=Product.query.filter(Product.product_prodcatid==id).all()
    return render_template('user/birthday.html', biri=biri, dir=dir)

"""wedding view page"""
@app.route('/product/<variable>/<id>')
def wedding(variable, id):
    dir=Product_cat.query.all()
    biri=Product.query.filter(Product.product_prodcatid==id).all()
    return render_template('user/wedding.html', biri=biri, dir=dir)

"""cupcake view page"""
@app.route('/product/<variable>/<id>')
def cupcake(variable, id):
    dir=Product_cat.query.all()
    biri=Product.query.filter(Product.product_prodcatid==id).all()
    return render_template('user/cupcake.html', biri=biri, dir=dir)

"""product detail view page"""
@app.route('/product/<id>')
def product(id):
    dir=Product_cat.query.all()
    prod = db.session.query(Product).filter(Product.product_id==id).first()
    return render_template('user/product.html', prod=prod,dir=dir)

"""displaying cart items """
@app.route('/show/cart/')
def showcart():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/user/signup')
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    else:
        dir=Product_cat.query.all()
        if 'shoppingcart' not in session:
            return redirect(request.referrer)

        SubTotal = 0
        grandtotal = 0
        for key, prod in session['shoppingcart'].items():
            SubTotal += (float(prod['price']) * float(prod['quantity']))
            vat = ("%.2f" % (0.075 * float(SubTotal)))
            grandtotal = float(vat) + float(SubTotal)
        return render_template('user/cart.html',dir=dir, loggedin=loggedin, grandtotal=grandtotal, vat=vat)

"""dicts marger for addtocart"""
def margeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

"""add to cart"""
@app.route('/addtocart/', methods=['POST'])
def addtocart():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/login/')
    else:
        dir=Product_cat.query.all()
        try:
            #getting the cart form values
            product_id=request.form.get('product_id')
            qty=request.form.get('qty')
            shipping=request.form.get('address')
            prod=Product.query.filter(Product.product_id==product_id).first()

            #checking for availability of the values coming from post method
            if product_id and qty and shipping and request.method == 'POST':
                #creating a dictionary to pickout products items fetched 
                dicItems = {product_id:{"name":prod.product_name, "price":prod.product_price, "quantity":qty, "image":prod.product_image_url, "shipping":shipping}}
                #checking if shopppingcart is in session 
                if 'shoppingcart' in session:
                    print(session['shoppingcart'])
                    if product_id in session['shoppingcart']:
                        for key, item in session['shoppingcart'].items():
                            if int(key)==int(product_id):
                                session.modified = True
                                item['quantity']+=1
                    else:
                        session['shoppingcart']=margeDicts(session['shoppingcart'], dicItems)
                else:
                    session['shoppingcart'] = dicItems
                    return redirect(request.referrer)
        except Exception as e:
            return e
        finally:
            return redirect(request.referrer)

"""emptying a cart in session"""
@app.route('/empty/cart')
def emptyCart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

"""updating a cart"""
@app.route('/update/cart/<int:id>', methods=['POST'])
def update_cart(id):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method=="POST":
        quantity = request.form.get('qty')
        try:
            session.modified = True
            for key, item in session['shoppingcart'].items():
                if int(key)==id:
                    item['quantity']= quantity
                    flash('Cart updated')
                    return redirect(url_for('showcart'))
        except Exception as e:
            print(e)
            return redirect(url_for('showcart'))

"""removing a item from cart"""
@app.route('/remove/cart/<int:id>')
def remove_cart(id):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    try:
        session.modified = True
        for key, item in session['shoppingcart'].items():
            if int(key)==id:
                session['shoppingcart'].pop(key, None)
                return redirect(url_for('showcart'))
    except Exception as e:
        print(e)
        return redirect(url_for('showcart'))

"""clearing all cart"""
@app.route('/clear/cart')
def clear_cart():
    try:
        session.pop('shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

"""order product route"""
@app.route('/order/', methods=['POST'])
def order_product():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/login/')
    if request.method=="POST":
        Grandtotal=request.form.get('gtotal')
        id=loggedin
        session['shoppingcart']
        status = 'pending'
        ref = int(random.random()*10000000)
        session['refno'] = ref
        
        #querying order_products
        order=Order_product(order_userid=id, order_status=status,)
        db.session.add(order)
        db.session.commit()

        SubTotal=0
        vat=0
        for x,y in session['shoppingcart'].items():
            SubTotal = (float(y['price']) * float(y['quantity']))
            vat = ("%.2f" % (0.075 * float(SubTotal)))
            qty=y['quantity']
            price=y['price']
            gtotal = float(vat) + float(SubTotal)
            ordDetail=Order_Details(orderdetail_orderproductid=order.order_productid, VAT=vat, order_shipping_address=y['shipping'],order_detail_Qty=qty, order_detail_total_amount=SubTotal, orderdetail_amount=price, orderdetail_productid=x, grand_total=gtotal)
            db.session.add(ordDetail)
        db.session.commit()

        pay=Payment(payment_transNo=ref, payment_amount=Grandtotal, payment_status=status, payment_userid=id, payment_orderid=order.order_productid)
        db.session.add(pay)
        db.session.commit()
        return redirect('/confirm/payment')
    

"""payment route"""
@app.route('/confirm/payment', methods=['POST','GET'])
def confirm_payment():
    loggedin=session.get('user')
    ref = session.get('refno')
    if loggedin==None or ref==None:
        return redirect('/')
    users = User.query.get(loggedin)
    payin=Payment.query.filter(Payment.payment_transNo==ref).first()
    if request.method=="GET":
        return render_template('user/confirmpayment.html',users=users, payin=payin)
    else:
        data = {"email":users.user_email,"amount":payin.payment_amount*100, "reference":payin.payment_transNo}

        headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_9ebd9bc239bcde7a0f43e2eab48b18ef1910356f"}

        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

        rspjson = json.loads(response.text) 
        if rspjson.get('status') == True:
            authurl = rspjson['data']['authorization_url']
            session.pop('shoppingcart', None)
            return redirect(authurl)
        else:
            return "Please try again"

@app.route("/user/payverify")
def paystack():
    reference = request.args.get('reference')
    ref = session.get('refno')
    #update our database 
    headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_9ebd9bc239bcde7a0f43e2eab48b18ef1910356f"}

    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
    rsp =response.json()#in json format
    if rsp['data']['status'] =='success':
        amt = rsp['data']['amount']
        ipaddress = rsp['data']['ip_address']
        p = Payment.query.filter(Payment.payment_transNo==ref).first()
        p.payment_status = 'paid'
        db.session.add(p)
        db.session.commit()
        flash("Payment Was Successful", "success")
        return redirect('/delivery')  #update database and redirect them to the feedback page
    else:
        p = Payment.query.filter(Payment.payment_transNo==ref).first()
        p.payment_status = 'failed'
        db.session.add(p)
        db.session.commit()
        flash("Payment Failed", "danger")
        return redirect('/profile/')

"""search result"""
@app.route('/search', methods=['POST'])
def search():
    word=request.form.get('search')
    prod=Product.query.filter(Product.product_name.ilike(f'%{word}%')).order_by(desc(Product.product_id)).limit(10).all()
    dir=Product_cat.query.all()
    return render_template('user/search.html', prod=prod, dir=dir)

"""order view page"""
@app.route('/myorder/')
def myorder():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    else:
        user=User.query.get(loggedin)
        pic=Profile_pic.query.filter(Profile_pic.pic_userid==user.user_id).limit(1).all()
        order = Order_product.query.filter(Order_product.order_userid==user.user_id).order_by(desc(Order_product.order_productid)).all()
        dir=Product_cat.query.all()
        state=State.query.all()
        return render_template('user/order.html', pic=pic, loggedin=loggedin, dir=dir, state=state, order=order, user=user)

"""order detail view page"""
@app.route('/myorder/details')
def order_detail():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    else:
        user=User.query.get(loggedin)
        pic=Profile_pic.query.filter(Profile_pic.pic_userid==user.user_id).limit(1).all()
        order=db.session.query(Order_Details).join(Product).add_columns(Product).filter(Order_Details.order_detailid==user.user_id).order_by(desc(Order_Details.order_detailid)).all()
        dir=Product_cat.query.all()
        state=State.query.all()
        return render_template('user/order_details.html', loggedin=loggedin, pic=pic, dir=dir, user=user, state=state, order=order)

"""payment view page"""
@app.route('/mypayment/')
def mypayment():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    else:
        user=User.query.get(loggedin)
        pic=Profile_pic.query.filter(Profile_pic.pic_userid==user.user_id).limit(1).all()
        pay=Payment.query.filter(Payment.payment_userid==user.user_id).order_by(desc(Payment.payment_id)).all()
        dir=Product_cat.query.all()
        state=State.query.all()
        return render_template('user/payment.html', loggedin=loggedin, dir=dir, pic=pic, user=user, state=state, pay=pay)

"""Profile Picture"""
@app.route('/user/profilepic', methods=['POST'])
def profilepic():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    else:
        user=User.query.get(loggedin)

        # requesting image from form
        image=request.files.get('filename')
        original_name = image.filename

        #checking if file is not empty
        if original_name !="":
            extension = os.path.splitext(original_name)
            if extension[1].lower() in ['.jpg','.png','gif']:
                fn=math.ceil(random.random()*10000000000)
                save_as=str(fn)+extension[1]
                image.save(f'holacakesapp/static/images/profilepic/{save_as}')
                    
                #inserting into the database
                pic = Profile_pic(pic_url=save_as, pic_userid=user.user_id)
                db.session.add(pic)
                db.session.commit()
                flash('image added successfully')
                return redirect("/profile/")
            else:
                flash("File Type Not Allowed")
                return redirect("/profile/")
        else:
            #if no picture supplied
            save_as==""
                    
            #inserting into the database
            pic = Profile_pic(pic_url=save_as, pic_userid=user.user_id)
            db.session.add(pic)
            db.session.commit()
            return render_template('user/profile.html', user=user)

"""Delete Account"""
@app.route('/user/delete/account') 
def delete_account():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    else:
        loggedin=session.get('user')
        deluser = User.query.get(loggedin)
        db.session.delete(deluser)
        db.session.commit()
        flash('Account deleted successfully, if reconcile signup to begin')
        return redirect('/signup/')


"""reviews route"""
@app.route('/reviews', methods=['POST', 'GET'])
def reviews():
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')

    if request.method=='GET':
        revi=Reviews.query.order_by(desc(Reviews.reviews_date)).limit(10).all()
        pic=Profile_pic.query.filter(Profile_pic.pic_userid==loggedin).limit(1).all()
        return render_template('user/reviews.html', revi=revi)
    
    if request.method=="POST":
        comment = request.form.get('comment')
        r = Reviews(reviews_userid=loggedin, reviews_comment=comment)
        db.session.add(r)
        db.session.commit()
    return redirect('/reviews')

"""delivery Route"""
@app.route('/delivery', methods=['POST', 'GET'])
def delivery():
    loggedin=session.get('user')
    dir=Product_cat.query.all()
    if loggedin==None:
        return redirect('/')
    if request.method=='POST':
        user_id=loggedin
        del_mode=request.form.get('deliverymode')
        del_status = 'pending'
        ord=Order_product.query.filter(Order_product.order_productid==loggedin).first()
        ordid=ord.order_productid
        if del_mode !="":
            dd=Delivery(delivery_mode=del_mode, delivery_status=del_status, delivery_orderid=ordid, delivery_userid=user_id)
            db.session.add(dd)
            db.session.commit()
        return redirect('/profile/')
    else:
        flash('fill each filed appropriately')
        return render_template('user/delivery.html', dir=dir)

"""delivery detail view"""
@app.route('/delivery/status')
def delivery_status():
    loggedin=session.get('user')
    dir=Product_cat.query.all()
    delstatus=Delivery.query.filter(Delivery.delivery_userid==loggedin).all()
    return render_template('user/deliverystatus.html', delstatus=delstatus, dir=dir)

"""Error 404 page"""
@app.errorhandler(404)
def page_not_found(error):
    loggedin=session.get('user')
    if loggedin==None:
        return redirect('/')
    else:
        dir=Product_cat.query.all()
        return render_template('user/error.html', dir=dir, error=error),404