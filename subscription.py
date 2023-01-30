from __future__ import annotations

import os

import boto3
from fastapi import HTTPException

topic_arn = os.environ.get('TOPIC_ARN')

session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_SNS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SNS_SECRET_KEY'),
)

sns = boto3.client('sns')
sqs = boto3.client('sqs')


def subscribe_email(email: str) -> dict:
    try:
        return sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email,
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail='Error occurred!',
        )


def unsubscribe_email(email: str) -> None:
    try:
        subscriptions = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
        for subscription in subscriptions['Subscriptions']:
            if email == subscription['Endpoint']:
                if subscription['SubscriptionArn'] == 'Deleted':
                    raise HTTPException(
                        status_code=400,
                        detail='This email address has been deleted!',
                    )
                elif subscription['SubscriptionArn'] == 'PendingConfirmation':
                    raise HTTPException(
                        status_code=400,
                        detail='Please confirm subscription first!',
                    )
                sns.unsubscribe(
                    SubscriptionArn=subscription['SubscriptionArn'],
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Can't find {email}",
                )
    except Exception:
        # TODO: add reason of error
        raise HTTPException(
            status_code=400,
            detail='Error occurred',
        )


def send_message_to_sqs(message):
    sqs.send_message(
        QueueUrl=os.environ.get('SQS_QUEUE_NAME'),
        MessageBody=message,
    )
    received_msg = sqs.receive_message(
        QueueUrl=os.environ.get('QUEUE_URL'),
        MaxNumberOfMessages=1,
    )['Messages'][0]['Body']
    sns.publish(TopicArn=topic_arn, Message=received_msg)
