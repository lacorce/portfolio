from aiogram import filters, types


class IsPaymentMethodStarsFilter(filters.BaseFilter):
    def __call__(self, callback: types.CallbackQuery):
        callback_data = callback.data
        splitted_callback_data = callback_data.split(':')

        payment_method = splitted_callback_data[2]
        
        if payment_method == 'stars': 
            return True 
        
        return False
