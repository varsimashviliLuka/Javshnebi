from src import db
from src.models import Subscription
from src.logger import get_logger
from datetime import datetime, timedelta

logger = get_logger("get_sendable_subscriptions")

def get_sendable_subscriptions():
    from flask import current_app
    able_subscriptions = []

    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    with current_app.app_context():
        logger.info('Filtering subscriptions')
        subscriptions = Subscription.query.filter(
            db.or_(
                Subscription.email_sent_at == None,
                Subscription.email_sent_at < two_weeks_ago
            )
        ).all()

        for subscription in subscriptions:
            if subscription.user.verified != True:
                continue
            else:
                logger.info('Adding subscription to list')
                able_subscriptions.append(subscription)

    logger.info('Returning full list of subscriptions which are able to send email')
    return able_subscriptions
