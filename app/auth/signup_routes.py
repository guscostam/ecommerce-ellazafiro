from flask import Blueprint, render_template

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')
