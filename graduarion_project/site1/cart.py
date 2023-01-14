from decimal import Decimal
from django.conf import settings
from .models import Plorts


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
        if product_id not in self.cart:
            self.cart[product_id.idPlort] = {'quantity': quantity,
                                               'price': str(product_id.price),
                                               'image': product_id.imagePlort,
                                             }
        if update_quantity:
            self.cart[product_id.idPlort]['quantity'] = quantity
        # else:
        #     self.cart[product_id.idPlort]['quantity'] += quantity
        #     print(self.cart[product_id.idPlort])
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        if product in self.cart:
            del self.cart[product]
        self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        ids = {}
        for i in product_ids:
            products = Plorts.objects.get(idPlort=i)
            ids[products.idPlort] = products.imagePlort
        for product, coun in ids.items():
            self.cart[str(product)]['product'] = product
            self.cart[str(product)]['image'] = coun

        # получение объектов product и добавление их в корзину

        for item in self.cart.values():
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
        return sum(item['price'] * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True