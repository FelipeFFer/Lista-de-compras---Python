from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'cart' not in session:
        session['cart'] = []
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        image = request.form.get('image')
        if name and price and quantity:
            try:
                price = float(price)
                quantity = int(quantity)
                if price > 0 and quantity > 0:
                    session['cart'].append({'name': name, 'price': price, 'quantity': quantity, 'image': image or ''})
                    session.modified = True
            except ValueError:
                pass  # ignore invalid input
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('index.html', cart=cart, total=total)

@app.route('/remove/<int:index>')
def remove(index):
    if 'cart' in session and 0 <= index < len(session['cart']):
        session['cart'].pop(index)
        session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)