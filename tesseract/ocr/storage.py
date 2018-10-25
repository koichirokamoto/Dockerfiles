"""Google Cloud Storage utility."""

import time

from google.cloud import storage
from google.oauth2 import service_account

DEFAULT_EXPIRATION = 5 * 60


def upload(project, bucket_name, filename, service_account_file=None):
  credentials = None
  if service_account_file:
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file)
  client = storage.Client(project=project, credentials=credentials)
  bucket = client.bucket(bucket_name)
  blob = bucket.blob(filename)
  blob.upload_from_filename(filename)
  return blob


def signed_url_for_png(blob, credentials=None, expiration=DEFAULT_EXPIRATION):
  expiration = int(time.time()) + expiration
  return blob.generate_signed_url(
      expiration, response_type='image/png', credentials=credentials)
