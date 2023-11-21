from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Product


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])


@views.route('/main')
def main():
    return render_template("index.html", user=current_user)

@views.route('/prod')
def prod():
    return render_template("prod.html", user=current_user)

@views.route('/add-product', methods=['POST'])
@login_required
def add_product():
    product_data = request.form
    new_product = Product(
        image_filename=product_data.get('image_filename'),
        name=product_data.get('name'),
        description=product_data.get('description'),
        price=product_data.get('price'),
        user_id=current_user.id
    )
    db.session.add(new_product)
    db.session.commit()
    flash('Product added to profile!', category='success')
    return redirect(url_for('views.profile'))

@views.route('/hello')
def hello():
    return "<p>hello</p>"





@views.route('/delete-product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('You do not have permission to delete this product.', category='error')
        return redirect(url_for('views.profile'))
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted!', category='success')
    return redirect(url_for('views.profile'))

@views.route('/pc')
def pc():
    return render_template("pc.html", user=current_user)

@views.route('/pc2')
def pc2():
    return render_template("pc2.html", user=current_user)

@views.route('/pc3')
def pc3():
    return render_template("pc3.html", user=current_user)

@views.route('/pc4')
def pc4():
    return render_template("pc4.html", user=current_user)

@views.route('/pc5')
def pc5():
    return render_template("pc5.html", user=current_user)

@views.route('/pc6')
def pc6():
    return render_template("pc6.html", user=current_user)

@views.route('/profile')
@login_required
def profile():
    user_products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", user=current_user, products=user_products)



