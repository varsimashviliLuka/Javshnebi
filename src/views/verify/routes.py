from flask import render_template, Blueprint, request
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, Config.TEMPLATES_FOLDERS, "verify")
verify_blueprint = Blueprint("verify", __name__, template_folder=TEMPLATES_FOLDER)

@verify_blueprint.route("/verify")
def verify():
    user_id = request.args.get('user_id')
    return render_template("verify.html", user_id=user_id)