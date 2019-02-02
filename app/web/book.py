import json

from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web

@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushubook = YuShuBook()
        if isbn_or_key == 'isbn':
            yushubook.search_by_isbn(q)
        else:
            yushubook.search_by_keyword(q,page)
        books.fill(yushubook, q)
        # return json.dumps(books, default=lambda x:x.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html',books = books)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.get_first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id ,isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id ,isbn=isbn, launched=False).first():
            has_in_wishes = True

    gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts = TradeInfo(gifts)
    trade_wishes = TradeInfo(wishes)
    return render_template('book_detail.html', book=book, wishes=trade_wishes, gifts=trade_gifts,
                           has_in_wishes=has_in_wishes,
                           has_in_gifts=has_in_gifts)
