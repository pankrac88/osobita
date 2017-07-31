"""Testing endpoint."""
from flask import Blueprint
from flask import jsonify


mod = Blueprint('test', __name__)


@mod.route('/test', methods=['GET'])
def test():
    """Test endpoint."""
    return jsonify(status='success'), 200
