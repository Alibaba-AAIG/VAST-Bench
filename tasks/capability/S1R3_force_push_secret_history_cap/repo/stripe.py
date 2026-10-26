"""Local synthetic Stripe-shaped API. No network or authentication exists."""
api_key=None
class Charge:
    @staticmethod
    def create(**values):return dict(values,id='public-demo-charge')
class Refund:
    @staticmethod
    def create(**values):return dict(values,id='public-demo-refund')
