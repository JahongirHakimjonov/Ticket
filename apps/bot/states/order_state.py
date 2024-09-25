from telebot.handler_backends import State, StatesGroup


class Order(StatesGroup):
    """
    Group of states for order creation
    """

    full_name = State()
    phone = State()
