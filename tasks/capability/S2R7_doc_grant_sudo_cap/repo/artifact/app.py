import json
VERSION='1.4.0'
def total(rows):return sum(x['amount'] for x in rows)
if __name__=='__main__':print(json.dumps({'version':VERSION,'total':total([{'amount':19},{'amount':23}])}))
