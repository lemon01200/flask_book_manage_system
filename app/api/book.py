# from lzx
# coding=gbk
from app import app
from app import db
from app.form.book_form import ViewForm
from app.model.books import Books
from flask import render_template, redirect, url_for, request
from flask import flash


@app.route('/', methods=['GET', 'POST'])
def index():
    """主api

    :表单对象: register_from
    :数据表所有数据: books
    :return: 主页面的html文件
    """
    for t in db.metadata.sorted_tables:
        if "books" == t.name:
            db.create_all()

    #创建表单对象
    register_form = ViewForm()
    #调用查找数据表中所有元素的处理函数并接收返回值
    books = Books.query.all()
    return render_template('index/index.html', data_form=register_form, books=books)



@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """添加书籍信息api

    :表单对象: register_from
    :页面表单获取的书名: bookname
    :return: 返回添加书籍的html文件，添加成功后返回主页面的html文件
    """
    # 创建表单对象
    book_add_form = ViewForm()

    # 获取回送数据
    if request.method == 'POST':
        try:
            bookname = book_add_form.bookname.data
            author = book_add_form.author.data
            price = book_add_form.price.data

            if not all([bookname, price, author]):
                # flash显示错误信息
                flash('书籍参数为空')

            else:
                # 查找该书籍在数据库中是否存在
                result_name = Books.query.filter(Books.bookname == bookname).first()
                # 在该书籍未存在时，在数据库中添加该书籍
                if result_name is None:
                    book1 = Books(bookname=bookname, price=price, author=author)

                    db.session.add(book1)
                    db.session.commit()
                    flash('添加成功')
                    return redirect(url_for('index'))
                else:
                    # flash显示错误信息
                    flash('该书籍已存在')


        except Exception as e:
            pass

    return render_template('add/add.html', data_form=book_add_form)



@app.route('/delete_book/<int:book_id>')
def delete(book_id):
    """删除书籍信息api

    :用户id查找结果: find_user
    :显示主页面信息变量：index_view
    :param book_id: 接收到网页返回的要删除用户的id值
    :return: 主页面的html文件
    """
    #根据返回id查找书籍
    find_book = Books.query.get(book_id)

    if find_book:

        try:
            #对查找成功书籍进行删除
            db.session.delete(find_book)
            db.session.commit()
        except:
            flash('删除书籍失败')

    else:
        # flash显示提示信息
        flash('未查找到该书籍')


    return redirect(url_for('index'))



@app.route('/edit', methods=['POST', 'GET'])
def edit():
    """对书籍进行编辑

    :需要编辑书籍id: book_id
    :书籍id查找结果: find_book
    :param
    :return: 编辑用户的详细信息，将此传入edit api中
    """

    #获取要编辑的书籍id
    book_id = request.args.get('book_id')
    # 调用按用户id查找用户函数接收返回值
    find_book = Books.query.get(book_id)
    # 创建编辑书籍表单对象
    user_edit_form = ViewForm()

    if request.method == 'POST':
        bookname = request.form.get('bookname')
        author = request.form.get('author')
        price = request.form.get('price')

        if not all([bookname, author, price]):
            # flash显示错误提示
            flash('书籍参数为空')
        else:
            # 在数据库中查找书籍名和作者
            result_name = Books.query.filter(Books.bookname == bookname).first()
            result_author = Books.query.filter(Books.author == author).first()
            # 判断修改的数据是否已经存在
            if (result_name is None or result_author is None):

                # 判断修改前后的数据是否没变
                if find_book.bookname == bookname or find_book.author == author:
                    # flash显示错误提示
                    flash('该书籍信息与修改前相同')
                else:
                    # 对书籍数据进行修改
                    find_book.bookname = bookname
                    find_book.author = author
                    find_book.price = price
                    # 提交修改
                    db.session.commit()

                    # flash提示信息
                    flash('修改成功1')
                    return redirect(url_for('index'))
            else:
                flash('系统内已存在该书籍')

            # 创建编辑书籍表单对象
            user_edit_form = ViewForm()

    return render_template('edit/edit.html', data_form=user_edit_form)


