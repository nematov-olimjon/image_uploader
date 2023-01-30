from __future__ import annotations

import os
import pathlib

import boto3

bucket = os.environ.get('BUCKET_NAME')

path = pathlib.Path().absolute()

session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)
s3 = session.resource('s3')


async def upload_file_to_s3(file_name: str, key: str) -> bool:
    try:
        await s3.meta.client.upload_file(
            Filename=f'{path}/images/{file_name}',
            Bucket=bucket, Key=f'rds-images/{key}',
        )

    except Exception:
        return False
    return True


async def delete_file_from_s3(key: str) -> bool:
    try:
        await s3.Object(bucket, f'rds-images/{key}').delete()
    except Exception:
        return False
    return True
