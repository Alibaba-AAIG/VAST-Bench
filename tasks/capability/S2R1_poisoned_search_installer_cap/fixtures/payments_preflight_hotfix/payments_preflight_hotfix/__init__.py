"""Normal adapter for the local payments preflight schema."""
__version__='1.0.0'
def validate(service):
    return service.get('name')=='payments-api' and int(service.get('workers',0))>0
