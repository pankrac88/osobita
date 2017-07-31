"""Topmine phrase extraction resource."""
from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask import jsonify
from flask import current_app
from topmine import extract_phrases_from_doc


mod = Blueprint('topmine_extractor', __name__)


document_args = {
    # Required arguments
    'document': fields.Str(required=True)
}


@mod.route('/extract', methods=['GET'])
@use_kwargs(document_args)
def extract_phrases(document):
    phrases = extract_phrases_from_doc(document,
                                       current_app.phrase_counter,
                                       current_app.vocab_size)
    return jsonify(status='success', phrases=phrases), 200
