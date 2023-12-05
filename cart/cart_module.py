from products.models import Product
from profile_users.models import User

CART_SESSION_ID = 'cart'


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __len__(self):
        # Return the number of items in the cart
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            item['unique_id'] = self.unique_id_generator(product.id, item['color'], item['size'])
            yield item

    def unique_id_generator(self, id, color, size):
        result = f'{id}-{color}-{size}'
        return result

    def add(self, product, quantity, color, size):
        unique = self.unique_id_generator(product.id, color, size)
        if unique not in self.cart:
            if product.on_sale:
                self.cart[unique] = {'quantity': 0, 'price': str(product.discount), 'color': color, 'size': size,
                                     'id': str(product.id)}
            else:
                self.cart[unique] = {'quantity': 0, 'price': str(product.price), 'color': color, 'size': size,
                                     'id': str(product.id)}

        if self.cart[unique]['quantity'] is None:
            self.cart[unique]['quantity'] = 0

        # If quantity is not specified or is None, default it to 1
        if quantity is None:
            quantity = 1

        self.cart[unique]['quantity'] += int(quantity)

        self.save()

    # def total(self):
    #     cart = self.cart.values()
    #     total = sum(int(item['price']) * int(item['quantity']) for item in cart)
    #     # for item in cart:
    #     #     total += item['total']
    #     return total

    def total(self):
        cart = self.cart.values()
        total = 0

        for item in cart:
            product = Product.objects.get(id=int(item['id']))
            if product.on_sale:
                total += int(product.discount) * int(item['quantity'])
            else:
                total += int(item['price']) * int(item['quantity'])

        return total

    def remove_cart(self):
        del self.session[CART_SESSION_ID]

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True
