import json

from flask import jsonify,request
from app.forms.book import SearchForm

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection
from . import web

@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        books = BookCollection()
        yushubook = YuShuBook()
        if isbn_or_key == 'isbn':
            yushubook.search_by_isbn(q)
        else:
            yushubook.search_by_keyword(q,page)
        books.fill(yushubook, q)
        return json.dumps(books, default=lambda x:x.__dict__)
    return jsonify(form.errors)