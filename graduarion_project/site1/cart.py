from decimal import Decimal
from django.conf import settings
from .models import Purchase, Plorts


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = Plorts.objects.get(idPlort=product)
        # print(100 *'!', product_id.idPlort)
        if product_id not in self.cart:
            self.cart[product_id.idPlort] = {'quantity': 0,
                                               'price': str(product_id.price)}
        if update_quantity:
            # print(100 *'!', update_quantity)
            self.cart[product_id.idPlort]['quantity'] = quantity
            # print(self.cart[product_id.idPlort]['quantity'])
        else:
            self.cart[product_id.idPlort]['quantity'] += quantity
            # print(100 *'!', self.cart[product_id.idPlort]['quantity'])
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # print(100 *'!', self.cart)
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = Plorts.objects.get(idPlort=product)
        if product_id in self.cart:
            del self.cart[product_id.idPlort]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # keyPl = ''
        for product_id in product_ids:
            print('ID'*10, product_id)
            # keyPl += product_id + ', '

            # products = Plorts.objects.get(idPlort=product_id)
            # print('products '*10, products.idPlort, products.price)
            # for product in products:
            #     print('product ' * 50, product, product.idPlort)
            #     self.cart[str(product.idPlort)]['product'] = products.price, products.plortName, products.imagePlort

        # keysList = [key for key in product_ids]

        # получение объектов product и добавление их в корзину
        # products = Plorts.objects.get(idPlort=str(list(product_ids)))
        # print(10 *'products, ', products.idPlort, products.price)
        # print(products.idPlort, products.price)

        print(self.cart.values())
        for item in self.cart.values():
            print('item' * 10, item)
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True