"""Topmine application runner."""
import configs
from app_factory import create_application

application = create_application(configs.Config)


if __name__ == '__main__':
    application.run()
