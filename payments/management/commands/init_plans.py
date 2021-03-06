import decimal

from django.conf import settings
from django.core.management.base import BaseCommand

import stripe


class Command(BaseCommand):

    help = "Make sure your Stripe account has the plans"

    def handle(self, *args, **options):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        for plan in settings.PAYMENTS_PLANS:
            if settings.PAYMENTS_PLANS[plan].get("stripe_plan_id"):
                price = settings.PAYMENTS_PLANS[plan]["price"]
                if isinstance(price, decimal.Decimal):
                    amount = int(100 * price)
                else:
                    amount = int(100 * decimal.Decimal(str(price)))

                try:
                    stripe.Plan.create(
                        amount=amount,
                        interval=settings.PAYMENTS_PLANS[plan]["interval"],
                        name=settings.PAYMENTS_PLANS[plan]["name"],
                        currency=settings.PAYMENTS_PLANS[plan]["currency"],
                        trial_period_days=settings.PAYMENTS_PLANS[plan].get(
                            "trial_period_days"
                        ),
                        id=settings.PAYMENTS_PLANS[plan].get("stripe_plan_id"),
                        interval_count=settings.PAYMENTS_PLANS[plan].get(
                            "interval_count"
                        ),
                    )
                    print "Plan created for {0}".format(plan)
                except Exception as e:
                    print e.message
