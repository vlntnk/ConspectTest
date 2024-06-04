from flask import (Flask, render_template, request, url_for, redirect, session, render_template_string, jsonify)
from flask_sqlalchemy import SQLAlchemy
import g4f
import os
import uuid
import PyPDF2
import docx
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
UPLOAD_FOLDER = r'.\conspects'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'секретный ключ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pages.db'
app.config['SQLALCHEMY_BINDS'] = {
    "db2" : 'sqlite:///conspects.db',
    "db3" : 'sqlite:///database.db'
}
db1 = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
g4f.debug.logging = True
g4f.check_version = False
print(g4f.version)
print(g4f.Provider.Ails.params)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def formating(answer2):
    answer2 = "".join(answer2)
    rem=0
    for i in range(len(answer2[:answer2.find('?')]), 0, -1):
        if answer2[i].isupper():
            rem=i
            break
    answer2 = answer2[rem:]
    answer2 = list(filter(lambda x: x != "-", answer2))
    answer2 = list(filter(lambda x: x != "*", answer2))
    answer2 = "".join(answer2)
    answer2 = answer2.split()
    answer2 = " ".join(answer2)
    return answer2


import re


def remove_markers(text):
    text = re.sub(r'[А-Г]\)', '', text)
    text = re.sub(r'[А-Г]\.', '', text)
    text = re.sub(r'[1-5]\.', '', text)
    text = re.sub(r'[1-5]\)', '', text)
    text = re.sub(r'\d+\.', '', text)
    return text.strip()


import re


def for_test(text):
    if not isinstance(text, str):
        text = str(text)

    questions_and_options = text

    if "Правильный ответ:" in questions_and_options:
        questions_and_options = re.sub(r" Правильный ответ: ", '', questions_and_options)

    if "Вопрос:" in questions_and_options:
        questions_and_options = re.split(r" Вопрос: ", questions_and_options)

    if "Варианты ответа:" in questions_and_options:
        questions_and_options = re.split(r" Варианты ответов: ", questions_and_options)

    return questions_and_options


def remove_dots(string):
    while "." in string:
        string.replace(".", "")
    return string


def gpt(question):
    response = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user",
                   "content": f'Напиши несколько вопросов на языке текста, с правильными ответами, '
                              f'по шаблону: '
                              f'вопрос, 4 варианта ответа, правильный ответ.'
                              f' пожалуйста, ни в коем случае не маркеруй варианты ответов ни буквами, ни цифрами, иначе я умру,'
                              f'каждый вариант ответа заканчивай точкой:{question}'}],
        stream=True
    )
    print(response)
    answer2 = [message for message in response]
    print(answer2)
    answer2 = formating(answer2)
    print(answer2)
    answer2 = remove_markers(answer2)
    print(answer2)
    answer2 = for_test(answer2)
    print(answer2)
    #answer2 = remove_dots(answer2)
    if isinstance(answer2, list):
        answer2 = " ".join(answer2)
    answer2 = re.split(r"\.|\? ", answer2)
    print(answer2)
    return answer2


class Page(db1.Model):
    id = db1.Column(db1.String, primary_key=True, unique=True)
    title = db1.Column(db1.String, nullable=False, unique=True)


class Conspects(db1.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'conspects'
    key = db1.Column(db1.Integer, primary_key=True)
    name = db1.Column(db1.String, nullable=False)
    num = db1.Column(db1.String, nullable=False)
    path = db1.Column(db1.String, nullable=False)


with app.app_context():
    db1.create_all()

class Users_m(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    login = db1.Column(db1.String, nullable=False)
    password = db1.Column(db1.String, nullable=False)
'''
    class Meta:
        database = db
        table_name = 'users_m'
'''

class Users_s(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    login = db1.Column(db1.String, nullable=False)
    password = db1.Column(db1.String, nullable=False)

'''
    class Meta:
        database = db
        table_name = 'users_s'
'''
with app.app_context():
    db1.create_all()


@app.route('/')
@app.route('/vxod', methods=['POST', 'GET'])
def vxod():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user_m = Users_m(login=login,password=password)
        user_s = Users_s(login=login, password=password)

        if login and password:

            if Users_m.query.filter_by(login=login).first():
                user = Users_m.query.filter_by(login=login).first()
                if check_password_hash(user.password, password):
                    return "Успешно обработано"


            if Users_s.query.filter_by(login=login).first():
                user = Users_s.query.filter_by(login=login).first()
                if check_password_hash(user.password, password):
                    return "Успешно обработано"
    else:
        return render_template("vxod.html")



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login[0:2] == 'm_':
            login=login[2:]
            if not Users_m.query.filter_by(login=login).first():
                    user=Users_m(login=login, password=generate_password_hash(password))
                    db1.session.add(user)
                    db1.session.commit()
                    return "Успешно обработано"
        elif login[0:2] == 's_':
            login = login[2:]
            if not Users_s.query.filter_by(login=login).first():
                    user = Users_s(login=login, password=generate_password_hash(password))
                    db1.session.add(user)
                    db1.session.commit()
                    return "Успешно обработано"
    else:
        return render_template("register.html")

@app.route('/glav')
def glav():
    pages = Page.query.all()
    return render_template('glav.html', pages=pages)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        page_title = request.form.get('title')
        page_id = str(uuid.uuid4())
        with open(rf'templates/{page_title}.html', 'w', encoding="utf-8") as file:
            with open('templates/newpage.html', 'r', encoding="utf-8") as source:
                file.write(source.read())
        new_page = Page(title=page_title, id=page_id)
        db1.session.add(new_page)
        db1.session.commit()
        if page_title == "ОАИП":
            conspect = Conspects(num=page_id, name="Работа return", path="https://oaip.netlify.app/")
            db1.session.add(conspect)
            db1.session.commit()
        return redirect(url_for('glav', page_id=page_id, page_title=page_title))
    else:

        return render_template("create.html")


@app.route('/newpage/<page_title>/<string:page_id>', strict_slashes=False, methods=['POST', 'GET'])
def show_page(page_title, page_id):
    test = session.get('answer2', [])
    filtered_results = Conspects.query.filter_by(num=page_id).all()
    session.clear()
    return render_template(f'{page_title}.html',
                           page_id=page_id,
                           page_title=page_title,
                           test=test,
                           conspects=filtered_results)


@app.route('/chat/<page_title>/<page_id>', methods=['POST', 'GET'])
def chat_save(page_title, page_id):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            conspect = Conspects(num=page_id, name=file.filename, path=path)
            db1.session.add(conspect)
            db1.session.commit()
            if file.filename[file.filename.rfind("."):] == ".txt":
                with open(path, 'rb') as file:
                    question = file.read()
                    answer2 = gpt(question)
                    session['answer2'] = answer2
            elif file.filename[file.filename.rfind("."):] == ".pdf":
                text=""
                with open(path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    num_pages = len(pdf_reader.pages)
                    for page_number in range(num_pages):
                        page = pdf_reader.pages[page_number]
                        text += page.extract_text()
                    question = str(text)
                    print(type(question))
                    answer2 = gpt(question)
                    session['answer2'] = answer2
            elif file.filename[file.filename.rfind('.'):] == '.docx':
                question = ""
                doc = docx.Document(rf'{path}')
                for paragraph in doc.paragraphs:
                    question += paragraph.text+" "
                answer2 = gpt(question)
                session['answer2'] = answer2
            page_title = page_title
            page_id = page_id
        return redirect(url_for('show_page', page_id=page_id, page_title=page_title))

'''
@app.route('/check/<test>/<page_title>/<page_id>', methods=['POST', 'GET'])
def check(test, page_title, page_id):
    if request.method == 'POST':
        selected_option = request.form.get('item1')
        print(selected_option)
        correct_option = test[5]
        # Правильный ответ
        s2 = request.form.get('item2')
        c2 = test[11]
        s3 = request.form.get('item3')
        c3 = test[17]
        print(selected_option, correct_option, s2, c2, s3, c3)

       
        return redirect(url_for('show_page', page_title=page_title, page_id=page_id, test5=test[5]))
        
        # Welcome to GitHub Desktop!

This is your README. READMEs are where you can communicate what your project is and how to use it.

Write your name on line 6, save it, and then head back to GitHub Desktop.

'''

if __name__ == '__main__':
    app.run(debug=True)