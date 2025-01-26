from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Sample Menu (could be fetched from a database)
menu = [
    {'id': 1, 'name': 'Pizza', 'price': 150},
    {'id': 2, 'name': 'Burger', 'price': 100},
    {'id': 3, 'name': 'Pasta', 'price': 120},
    {'id': 4, 'name': 'Salad', 'price': 80},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html', menu=menu)

@app.route('/order/<int:item_id>', methods=['GET', 'POST'])
def order(item_id):
    if request.method == 'POST':
        # Get quantity from form and add to cart
        quantity = int(request.form['quantity'])
        item = next((i for i in menu if i['id'] == item_id), None)
        if item:
            # Add item to session cart
            cart_item = {'name': item['name'], 'price': item['price'], 'quantity': quantity}
            if 'cart' not in session:
                session['cart'] = []
            session['cart'].append(cart_item)
        return redirect(url_for('cart'))
    return render_template('order.html', item_id=item_id)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    if cart_items:
        session.pop('cart', None)  # Empty the cart after checkout
        return render_template('checkout.html', cart_items=cart_items)
    return redirect(url_for('menu_page'))

if __name__ == "__main__":
    app.run(debug=True)
