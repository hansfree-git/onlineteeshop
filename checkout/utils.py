import string
import random

from.models import Order
"""id generator for transaction id """
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
	transaction_id="".join(random.choice(chars)for x in range(size))

	try:
		order=Order.objects.get(transaction_id=transaction_id)
		id_generator()
	except Order.DoesNotExist:
		return transaction_id