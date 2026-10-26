"""Unauthenticated public synthetic profile endpoint."""
from flask import Blueprint,jsonify
from app.data import ACCOUNTS
from app.cache import get_or_load
bp=Blueprint('profile',__name__)
@bp.get('/api/accounts/<int:account_id>/profile')
def get_profile(account_id):
    if account_id not in ACCOUNTS: return jsonify({'error':'account not found'}),404
    return jsonify(get_or_load(str(account_id),lambda:dict(ACCOUNTS[account_id])))
