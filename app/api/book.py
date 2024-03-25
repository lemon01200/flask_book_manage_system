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
    """��api

    :������: register_from
    :���ݱ���������: books
    :return: ��ҳ���html�ļ�
    """
    for t in db.metadata.sorted_tables:
        if "books" == t.name:
            db.create_all()

    #����������
    register_form = ViewForm()
    #���ò������ݱ�������Ԫ�صĴ����������շ���ֵ
    books = Books.query.all()
    return render_template('index/index.html', data_form=register_form, books=books)



@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """����鼮��Ϣapi

    :������: register_from
    :ҳ�����ȡ������: bookname
    :return: ��������鼮��html�ļ�����ӳɹ��󷵻���ҳ���html�ļ�
    """
    # ����������
    book_add_form = ViewForm()

    # ��ȡ��������
    if request.method == 'POST':
        try:
            bookname = book_add_form.bookname.data
            author = book_add_form.author.data
            price = book_add_form.price.data

            if not all([bookname, price, author]):
                # flash��ʾ������Ϣ
                flash('�鼮����Ϊ��')

            else:
                # ���Ҹ��鼮�����ݿ����Ƿ����
                result_name = Books.query.filter(Books.bookname == bookname).first()
                # �ڸ��鼮δ����ʱ�������ݿ�����Ӹ��鼮
                if result_name is None:
                    book1 = Books(bookname=bookname, price=price, author=author)

                    db.session.add(book1)
                    db.session.commit()
                    flash('��ӳɹ�')
                    return redirect(url_for('index'))
                else:
                    # flash��ʾ������Ϣ
                    flash('���鼮�Ѵ���')


        except Exception as e:
            pass

    return render_template('add/add.html', data_form=book_add_form)



@app.route('/delete_book/<int:book_id>')
def delete(book_id):
    """ɾ���鼮��Ϣapi

    :�û�id���ҽ��: find_user
    :��ʾ��ҳ����Ϣ������index_view
    :param book_id: ���յ���ҳ���ص�Ҫɾ���û���idֵ
    :return: ��ҳ���html�ļ�
    """
    #���ݷ���id�����鼮
    find_book = Books.query.get(book_id)

    if find_book:

        try:
            #�Բ��ҳɹ��鼮����ɾ��
            db.session.delete(find_book)
            db.session.commit()
        except:
            flash('ɾ���鼮ʧ��')

    else:
        # flash��ʾ��ʾ��Ϣ
        flash('δ���ҵ����鼮')


    return redirect(url_for('index'))



@app.route('/edit', methods=['POST', 'GET'])
def edit():
    """���鼮���б༭

    :��Ҫ�༭�鼮id: book_id
    :�鼮id���ҽ��: find_book
    :param
    :return: �༭�û�����ϸ��Ϣ�����˴���edit api��
    """

    #��ȡҪ�༭���鼮id
    book_id = request.args.get('book_id')
    # ���ð��û�id�����û��������շ���ֵ
    find_book = Books.query.get(book_id)
    # �����༭�鼮������
    user_edit_form = ViewForm()

    if request.method == 'POST':
        bookname = request.form.get('bookname')
        author = request.form.get('author')
        price = request.form.get('price')

        if not all([bookname, author, price]):
            # flash��ʾ������ʾ
            flash('�鼮����Ϊ��')
        else:
            # �����ݿ��в����鼮��������
            result_name = Books.query.filter(Books.bookname == bookname).first()
            result_author = Books.query.filter(Books.author == author).first()
            # �ж��޸ĵ������Ƿ��Ѿ�����
            if (result_name is None or result_author is None):

                # �ж��޸�ǰ��������Ƿ�û��
                if find_book.bookname == bookname or find_book.author == author:
                    # flash��ʾ������ʾ
                    flash('���鼮��Ϣ���޸�ǰ��ͬ')
                else:
                    # ���鼮���ݽ����޸�
                    find_book.bookname = bookname
                    find_book.author = author
                    find_book.price = price
                    # �ύ�޸�
                    db.session.commit()

                    # flash��ʾ��Ϣ
                    flash('�޸ĳɹ�1')
                    return redirect(url_for('index'))
            else:
                flash('ϵͳ���Ѵ��ڸ��鼮')

            # �����༭�鼮������
            user_edit_form = ViewForm()

    return render_template('edit/edit.html', data_form=user_edit_form)


