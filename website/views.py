from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Product, Computer, Comment

views = Blueprint('views', __name__)

@views.route('/main')
def main():
    return render_template("index.html", user=current_user)
@views.route('/prod')
def prod():
    return render_template("prod.html", user=current_user)

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


@views.route('/delete-product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found.', category='error')
    elif product.user_id != current_user.id:
        flash('You do not have permission to delete this product.', category='error')
    else:
        db.session.delete(product)
        db.session.commit()
        flash('Product has been deleted!', category='success')
    return redirect(url_for('views.profile'))


@views.route('/add_computer/<int:computer_id>')
@login_required
def add_computer(computer_id):
    computer = Computer.query.get(computer_id)
    if computer and computer.user_id is None:
        computer.user_id = current_user.id
        db.session.commit()
        flash('Computer added to your list', category='success')
    else:
        flash('Computer not found or already added by someone else', category='error')
    return redirect(url_for('views.my_computers'))


@views.route('/my_computers')
@login_required
def my_computers():
    user_computers = Computer.query.filter_by(user_id=current_user.id).all()
    return render_template('my_computers.html', computers=user_computers, user=current_user)


@views.route('/computer/<int:computer_id>', methods=['GET', 'POST'])
def computer(computer_id):
    computer = Computer.query.get_or_404(computer_id)
    comments = Comment.query.filter_by(computer_id=computer_id).all()

    if request.method == 'POST' and current_user.is_authenticated:
        comment_text = request.form.get('comment')
        new_comment = Comment(text=comment_text, computer_id=computer_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', category='success')
        return redirect(url_for('views.computer', computer_id=computer_id))

    return render_template('computer_details.html', computer=computer, comments=comments)

@views.route('/user_page')
@login_required
def user_page():
    return render_template('user_page.html', user=current_user)

@views.route('/profile')
@login_required
def profile():
    user_products = Product.query.filter_by(user_id=current_user.id).all()
    user_computers = Computer.query.filter_by(user_id=current_user.id).all()  # Added line to fetch user computers
    return render_template("profile.html", user=current_user, products=user_products, computers=user_computers)
