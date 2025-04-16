import os
import pytest
from django.conf import settings

# Test to check if all required environment variables are set
@pytest.mark.parametrize("env_var", [
    "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", 
    "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_STORAGE_BUCKET_NAME", 
    "AWS_S3_REGION_NAME", "GOOGLE_GEMINI_API_KEY"
])
def test_environment_variables_set(env_var):
    assert os.getenv(env_var) is not None, f"{env_var} is not set in the environment variables"

# Test database settings
def test_database_settings():
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    assert db_name == os.getenv("DB_NAME", "meiari_db"), f"Expected DB_NAME: {os.getenv('DB_NAME', 'meiari_db')}, but got {db_name}"
    assert db_user == os.getenv("DB_USER", "root"), f"Expected DB_USER: {os.getenv('DB_USER', 'root')}, but got {db_user}"
    assert db_password == os.getenv("DB_PASSWORD", "root"), f"Expected DB_PASSWORD: {os.getenv('DB_PASSWORD', 'root')}, but got {db_password}"
    assert db_host == os.getenv("DB_HOST", "localhost"), f"Expected DB_HOST: {os.getenv('DB_HOST', 'localhost')}, but got {db_host}"
    assert db_port == os.getenv("DB_PORT", "3306"), f"Expected DB_PORT: {os.getenv('DB_PORT', '3306')}, but got {db_port}"

# Test CORS settings
def test_cors_settings():
    assert settings.CORS_ALLOW_ALL_ORIGINS is True, "CORS_ALLOW_ALL_ORIGINS is not set to True"
    assert "http://localhost:3000" in settings.CORS_ALLOWED_ORIGINS, "CORS_ALLOWED_ORIGINS does not include 'http://localhost:3000'"
    assert "http://192.168.1.2:3000" in settings.CORS_ALLOWED_ORIGINS, "CORS_ALLOWED_ORIGINS does not include 'http://192.168.1.2:3000'"

# Test AWS S3 Configuration
def test_aws_s3_configuration():
    assert settings.AWS_ACCESS_KEY_ID is not None, "AWS_ACCESS_KEY_ID is not set"
    assert settings.AWS_SECRET_ACCESS_KEY is not None, "AWS_SECRET_ACCESS_KEY is not set"
    assert settings.AWS_STORAGE_BUCKET_NAME is not None, "AWS_STORAGE_BUCKET_NAME is not set"
    assert settings.AWS_S3_REGION_NAME is not None, "AWS_S3_REGION_NAME is not set"

    assert settings.STATIC_URL.startswith("https://"), "STATIC_URL should be a valid URL"
    assert settings.MEDIA_URL.startswith("https://"), "MEDIA_URL should be a valid URL"
    assert settings.STATICFILES_STORAGE == "storages.backends.s3boto3.S3Boto3Storage", \
        "STATICFILES_STORAGE should be set to 'storages.backends.s3boto3.S3Boto3Storage'"
    assert settings.DEFAULT_FILE_STORAGE == "storages.backends.s3boto3.S3Boto3Storage", \
        "DEFAULT_FILE_STORAGE should be set to 'storages.backends.s3boto3.S3Boto3Storage'"

# Test Google Gemini API Key
def test_google_gemini_api_key():
    assert settings.GOOGLE_GEMINI_API_KEY is not None, "GOOGLE_GEMINI_API_KEY is not set"

# Test Secret Key
def test_secret_key():
    assert settings.SECRET_KEY != 'django-insecure-xg-)0vl&omad44pg!b^o6%7*xslh&^y@9-5zs2k#9yt*s5x$ej', \
        "SECRET_KEY should not be the default insecure key. Please update it in your environment"

# Test Allowed Hosts
def test_allowed_hosts():
    assert "127.0.0.1" in settings.ALLOWED_HOSTS, "127.0.0.1 is not in ALLOWED_HOSTS"
    assert "localhost" in settings.ALLOWED_HOSTS, "localhost is not in ALLOWED_HOSTS"
    assert "192.168.20.76" in settings.ALLOWED_HOSTS, "192.168.20.76 is not in ALLOWED_HOSTS"
