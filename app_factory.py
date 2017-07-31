"""Flask factory for Topmine."""
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from resources import test
from resources import topmine_extractor
from frequent_mining_module import findFrequentPhrases


def create_application(config):
    """Create flask application."""
    application = Flask(__name__)
    application.config.from_object(config)

    register_blueprints(application)
    setup_logging(application)
    setup_error_handlers(application)
    load_corpus_and_find_frequent_phrases(application)

    return application


def load_corpus_and_find_frequent_phrases(app):
    """Loads the corpus into memory and extracts the frequent phrases."""
    app.logger.info('Loading corpus into memory.')
    app.phrase_counter, app.vocab_size = findFrequentPhrases(
        app.config['CORPUS_FILE'], app.config['FREQ_PATTERN_THRESHOLD'])
    app.logger.info('Finished loading corpus into memory.'
                    'Total vocabulary size is {}'.format(app.vocab_size))


def register_blueprints(app):
    """Register blueprints."""
    app.register_blueprint(test)
    app.register_blueprint(topmine_extractor)


def setup_logging(app):
    """Set up simple logging."""
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])


def setup_error_handlers(app):
    def handler_404(error):
        return jsonify(
            status_code=error.code,
            status_text=error.name,
            message='Sorry, the path was not found.'
        )
