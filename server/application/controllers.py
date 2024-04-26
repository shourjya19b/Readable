import re
import os
from datetime import date, timedelta

from .models import db, User, Section, Book, Request, Issue, Review
from .worker import cache

from flask import request, send_file, jsonify
from flask import current_app as app
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_user, auth_required, roles_required, current_user
from sqlalchemy import and_, or_
from celery.result import AsyncResult

@app.route("/user/register", methods=["POST"])
def index():
    username = request.json.get("name")
    email = request.json.get("email","")
    password = request.json.get("password")
    confirm = request.json.get("confirm_pwd")

    if not username:
        return {"error": "invalid_name"}, 404

    if not re.match("^.+@.+.+$", email):
        return {"error": "invalid_email"}, 404
    elif app.security.datastore.find_user(email=email):
        return {"error": "duplicate_email"}, 404

    if password != confirm:
        return {"error": "invalid_password"}, 404
    
    user = app.security.datastore.create_user(username=username,
                                              email=email,
                                              password=password)

    role = app.security.datastore.find_role("user")
    app.security.datastore.add_role_to_user(user, role)
    db.session.commit()
    return {"message": "Created user successfully"}, 201

@app.route("/user/login", methods=["POST"])
def signin():
    email = request.json.get("email", "")
    password = request.json.get("password")

    user = app.security.datastore.find_user(email=email)
    if (not user) or (user.password!=password):
        return {"error": "user not found"}, 404
    
    login_user(user)
    token = user.get_auth_token()
    roles = [role.name for role in user.roles]
    return {"token": token, "role": roles[0]}, 200

@app.route("/admin/login", methods=["POST"])
def admin_signin():
    email = request.json.get("email", "")
    password = request.json.get("password")

    user = app.security.datastore.find_user(email=email)
    roles = [role.name for role in user.roles]
    if (not user) or (user.password!=password) or ('admin' not in roles):
        return {"error": "user not found"}, 404
    
    login_user(user)
    token = user.get_auth_token()
    return {"token": token, "role": roles[0]}, 200

@app.route("/section/create", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def create_section():
    name = request.json.get("name",None)
    desc = request.json.get("desc","")

    if not name:
        return {"error": "invalid_name"}, 404
    
    section = Section(name=name, desc=desc)
    db.session.add(section)
    db.session.commit()
    return {"message": "Created section successfully"}, 201

@app.route("/sections", methods=["GET"])
@auth_required("token")
def search_section():
    search = request.args.get("search", "")

    if search!="":
        sections = Section.query.filter(Section.name.like(f"%{search}%")).all()
    else:
        sections = Section.query.all()

    return [{"id": section.id,
             "name": section.name,
             "desc": section.desc} for section in sections]

@app.route("/section/<int:section_id>/edit", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def update_section(section_id):
    name = request.json.get("name","")
    desc = request.json.get("desc")

    if not name or name=="":
        return {"error": "invalid_name"}, 404
    if not desc:
        return {"error": "invalid_desc"}, 404
    
    section = Section.query.filter(Section.id==section_id).first()
    
    if not section:
        return {"error": "Section not found"}, 404
    
    section.name = name
    section.desc = desc
    db.session.commit()
    return {"SUCCESS": True}, 200

@app.route("/section/<int:section_id>/delete", methods=["DELETE"])
@auth_required("token")
@roles_required("admin")
def delete_section(section_id):
    section = Section.query.filter(Section.id==section_id).first()

    if not section:
        return {"error": "Section not found"}, 404
    
    db.session.delete(section)
    db.session.commit()
    return {"message": "Deleted section successfully"}, 200

@app.route("/book/create", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def create_book():
    title = request.form.get("name", None)
    author = request.form.get("author", None)
    desc = request.form.get("desc", "")
    section_name = request.form.get("section", None)
    image = request.files.get("image")
    
    section = Section.query.filter(Section.name==section_name).first()

    if not title or title=="":
        return {"error": "invalid_title"}, 404
    elif not author or author=="":
        return {"error": "invalid_author"}, 404
    elif not section_name or not section:
        return {"error": "invalid_section"}, 404
    
    if not image:
        print('no image')
        img_src="default_section.jpg"
    else:
        img_src=image.filename
        current_dir=os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(current_dir,"../static/uploads", img_src))

    book = Book(name=title, author=author, desc=desc, section_id=section.id, image=img_src, rating=0)
    db.session.add(book)

    db.session.commit()
    
    return {"message": "Created book successfully"}, 201

@app.route("/book/<int:book_id>/edit", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def update_book(book_id):
    title = request.form.get("name", None)
    author = request.form.get("author", None)
    desc = request.form.get("desc", "")
    section_name = request.form.get("section", None)
    image = request.files.get("image")
    
    section = Section.query.filter(Section.name==section_name).first()

    if not title or title=="":
        return {"error": "invalid_title"}, 404
    elif not author or author=="":
        return {"error": "invalid_author"}, 404
    elif not section_name or not section:
        return {"error": "invalid_section"}, 404
    
    if not image:
        img_src="default_section.jpg"
    else:
        img_src=image.filename
        current_dir=os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(current_dir,"../static/uploads", img_src))

    book = Book.query.filter(Book.id==book_id).first()
    
    book.name=title
    book.author=author
    book.desc=desc
    book.section_id=section.id
    book.image=img_src

    db.session.commit()
    
    return {"message": "Updated book successfully"}, 201

@app.route("/book/<int:book_id>/delete", methods=["DELETE"])
@auth_required("token")
@roles_required("admin")
def delete_book(book_id):

    book = Book.query.filter(Book.id==book_id).first() 

    if not book:
        return {"error" : "Book not found"}, 404

    db.session.delete(book)
    db.session.commit()
    return {"message": "Deleted book successfully"}

@app.route("/books", methods=["GET"])
@auth_required("token")
def get_books():
    title = request.args.get("title", None)
    author = request.args.get("author", None)
    rating = request.args.get("rating", type=int)
    section_name = request.args.get("section", None)

    searched_books = []

    if not section_name:
        if not rating:
            if not author:
                if not title:
                    books=Book.query.all()
                else:
                    books=Book.query.filter(Book.name.like(f"%{title}%")).all()
            else:
                if not title:
                    books=Book.query.filter(Book.author.like(f"%{author}%")).all()
                else:
                    books=Book.query.filter(and_(Book.name.like(f"%{title}%"),Book.author.like(f"%{author}%"))).all()
        else:
            if not author:
                if not title:
                    books=Book.query.filter(Book.rating >= rating).all()
                else:
                    books=Book.query.filter(and_(Book.name.like(f"%{title}%"), Book.rating >= rating)).all()
            else:
                if not title:
                    books=Book.query.filter(and_(Book.author.like(f"%{author}%"), Book.rating >= rating)).all()
                else:
                    books=Book.query.filter(and_(Book.name.like(f"%{title}%"),Book.author.like(f"%{author}%"), Book.rating >= rating)).all()  
    else:
        section=Section.query.filter(Section.name==section_name).first()
        if not rating:
            if not author:
                if not title:
                    books=Book.query.filter(Book.section_id==section.id).all()
                else:
                    books=Book.query.filter(and_(Book.name.like(f"%{title}%"), Book.section_id==section.id)).all()
            else:
                if not title:
                    books=Book.query.filter(and_(Book.author.like(f"%{author}%"), Book.section_id==section.id)).all()
                else:
                    books=Book.query.filter(and_(Book.name.like(f"%{title}%"),Book.author.like(f"%{author}%"), Book.section_id==section.id)).all()
        else:
            if not author:
                if not title:
                    books=Book.query.filter(and_(Book.rating >= rating, Book.section_id==section.id)).all()
                else:
                    books=Book.query.filter(and_(Book.name.like(f"%{title}%"), Book.rating >= rating, Book.section_id==section.id)).all()
            else:
                if not title:
                    books=Book.query.filter(and_(Book.author.like(f"%{author}%"), Book.rating >= rating, Book.section_id==section.id)).all()
                else:
                    books=Book.query.filter(and_(Book.name.like(f"%{title}%"),Book.author.like(f"%{author}%"), Book.rating >= rating, Book.section_id==section.id)).all()

    for book in books:
        n_req=Request.query.filter(and_(Request.user_id==current_user.id,Request.book_id==book.id)).count()
        n_issue=Issue.query.filter(and_(Issue.user_id==current_user.id,Issue.book_id==book.id,Issue.returned==False)).count()
        book_section=Section.query.filter(Section.id==book.section_id).first()
        if (n_req+n_issue)==0:
            searched_books.append({"id": book.id,
                                   "image":book.image,
                                   "name":book.name,
                                   "author":book.author,
                                   "section": book_section.name,
                                   "desc":book.desc,
                                   "rating":book.rating})

    return searched_books

@app.route("/requests",methods=["GET"])
@auth_required("token")
@roles_required("admin")
def get_requests():
    result=[]
    requests=Request.query.all()

    for request in requests:
        book=Book.query.filter(Book.id==request.book_id).first()
        user=User.query.filter(User.id==request.user_id).first()
        section=Section.query.filter(Section.id==book.section_id).first()
        result.append({"id":request.id, "book_name":book.name, "book_section":section.name, "username":user.username})
    
    return result

@app.route("/admin/issues",methods=["GET"])
@auth_required("token")
@roles_required("admin")
def get_admin_issues():
    result=[]
    issues=Issue.query.filter(Issue.returned==False).all()

    for issue in issues:
        book=Book.query.filter(Book.id==issue.book_id).first()
        user=User.query.filter(User.id==issue.user_id).first()
        section=Section.query.filter(Section.id==book.section_id).first()
        result.append({"id":issue.id,"book_name":book.name, "book_section":section.name, "username":user.username})
    
    return result

@app.route("/user/issues",methods=["GET"])
@auth_required("token")
def get_user_issues():
    result=[]
    issues=Issue.query.filter(and_(Issue.user_id==current_user.id,Issue.returned==False)).all()

    for issue in issues:
        book=Book.query.filter(Book.id==issue.book_id).first()
        section=Section.query.filter(Section.id==book.section_id).first()
        result.append({"id":issue.id,"book_id":book.id,"book_name":book.name, "book_section":section.name})
    
    return result

@app.route("/request/<int:book_id>",methods=["POST"])
@auth_required("token")
def request_book(book_id):
    book=Book.query.filter(Book.id==book_id).first()
    if not book:
        return {"message": "Book not found"}, 404
    else:
        req=Request(book_id=book_id,user_id=current_user.id)
        n_issues=Issue.query.filter(Issue.user_id==current_user.id).count()
        n_reqs=Request.query.filter(Request.user_id==current_user.id).count()
        total_books=n_issues+n_reqs
        if total_books < 5:
            db.session.add(req)
            db.session.commit()
            return {"message": "Book requested"}, 200
        else:
            return {"message": "Book limit reached"}, 404

@app.route("/request/grant",methods=["POST"])
@auth_required("token")
@roles_required("admin")
def grant_request():
    req_id=request.json.get("request_id")

    req=Request.query.filter(Request.id==req_id).first()
    issue=Issue(book_id=req.book_id,
                user_id=req.user_id, 
                issue_date=date.today(), 
                return_date=date.today() + timedelta(days=7),
                returned=False)

    db.session.add(issue)
    db.session.delete(req)
    db.session.commit()
    return {"message":"Request granted"}, 200

@app.route("/request/cancel",methods=["POST"])
@auth_required("token")
@roles_required("admin")
def cancel_request():
    req_id=request.json.get("request_id")

    req=Request.query.filter(Request.id==req_id).first()

    db.session.delete(req)
    db.session.commit()
    return {"message":"Request cancelled"}, 200


@app.route("/issue/revoke",methods=["POST"])
@auth_required("token")
@roles_required("admin")
def revoke_issue():
    issue_id=request.json.get("issue_id")

    issue=Issue.query.filter(Issue.id==issue_id).first()
    issue.returned=True

    db.session.commit()
    return {"message":"Issue revoked"}, 200

@app.route("/issue/return",methods=["POST"])
@auth_required("token")
def return_issue():
    issue_id=request.json.get("issue_id")

    issue=Issue.query.filter(Issue.id==issue_id).first()
    issue.returned=True

    db.session.commit()
    return {"message":"Issue returned"}, 200

@app.route("/admin/book/statistics",methods=["GET"])
@auth_required("token")
@roles_required("admin")
@cache.cached(5)
def book_stats():
    result = {"books": [], "issues": []}
    for book in Book.query.all():
        n_issues=Issue.query.filter(Issue.book_id==book.id).count()

        result["books"].append(book.name)
        result["issues"].append(n_issues)

    return result


@app.route("/admin/section/statistics",methods=["GET"])
@auth_required("token")
@roles_required("admin")
def section_stats():
    result = {"sections": [], "issues": []}
    for book in Book.query.all():
        n_issues=Issue.query.filter(Issue.book_id==book.id).count()
        section=Section.query.filter(Section.id==book.section_id).first()

        if section.name not in result["sections"]:
            result["sections"].append(section.name)
            result["issues"].append(n_issues)
        else:
            sec_index=result["sections"].index(section.name)
            result["issues"][sec_index]+=n_issues

    return result

@app.route("/user/book/statistics",methods=["GET"])
@auth_required("token")
@cache.cached(5)
def book_stats_user():
    result = {"months": [], "issues": []}
    month_names=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for issue in Issue.query.filter(Issue.user_id==current_user.id).order_by(Issue.issue_date):
        date=issue.issue_date
        month_num=date.month
        month_name=month_names[month_num-1]

        if month_name not in result["months"]:
            result["months"].append(month_names[month_num-1])
            result["issues"].append(1)
        else:
            mon_index=result["months"].index(month_name)
            result["issues"][mon_index]+=1    

    return result


@app.route("/user/section/statistics",methods=["GET"])
@auth_required("token")
@cache.cached(5)
def section_stats_user():
    result = {"sections": [], "issues": []}
    for issue in Issue.query.filter(Issue.user_id==current_user.id).all():
        book=Book.query.filter(Book.id==issue.book_id).first()
        section=Section.query.filter(Section.id==book.section_id).first()

        if section.name not in result["sections"]:
            result["sections"].append(section.name)
            result["issues"].append(1)
        else:
            sec_index=result["sections"].index(section.name)
            result["issues"][sec_index]+=1

    return result

@app.route("/book/<int:book_id>/review", methods=["POST"])
@auth_required("token")
def review_book(book_id):
    
    rating = request.form.get("rating", None)
    user_review = request.form.get("review","")

    if not rating:
        return {"error": "invalid_rating"}, 404
    elif not user_review or user_review=="":
        return {"error": "invalid_review"}, 404
    
    review=Review(user_id=current_user.id,book_id=book_id,rating=int(rating),review=user_review)

    db.session.add(review)
    db.session.commit()

    book_reviews=Review.query.filter(Review.book_id==book_id).all()

    (tot_rating,review_count)=(0,0)
    for book_review in book_reviews:
        tot_rating+=int(book_review.rating)
        review_count+=1
    
    avg_rating=tot_rating/review_count
    book=Book.query.filter(Book.id==book_id).first()
    book.rating=avg_rating
    

    db.session.commit()

    return {"message": "Reviewed book successfully"}, 201




