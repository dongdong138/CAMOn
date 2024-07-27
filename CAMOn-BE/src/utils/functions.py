import json
import numbers
import os
import re
import uuid
import pickle
from cryptography.fernet import Fernet
import loguru
import hashlib
import unidecode
from datetime import date, datetime
from typing import Dict, List, Union, Any

from fastapi import UploadFile
import urllib.parse
from src.settings.config import DATE_FORMAT, DATETIME_FORMAT


def today():
    """
    get today
    :return: date
    """
    return date.today()


def get_encode_password(password):
    if isinstance(password, bytes):
        return urllib.parse.quote_from_bytes(password)
    elif isinstance(password, str):
        return urllib.parse.quote_plus(password)
    else:
        raise TypeError("Password must be bytes or string")


def now():
    return datetime.now()


def datetime_to_string(_time: datetime, default='', _format=DATETIME_FORMAT) -> str:
    if _time:
        return _time.strftime(_format)
    return default


def string_to_datetime(string: str, default=None, _format=DATETIME_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def date_to_string(_date: date, default='', _format=DATE_FORMAT) -> str:
    if _date:
        return _date.strftime(_format)
    return default


def string_to_date(string: str, default=None, _format=DATE_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def date_to_datetime(date_input: date, default=None) -> datetime:
    try:
        return datetime.combine(date_input, datetime.min.time())
    except (ValueError, TypeError):
        return default


def end_time_of_day(datetime_input: datetime) -> datetime:
    return datetime_input.replace(hour=23, minute=59, second=59)



def is_valid_mobile_number(mobile_number: str) -> bool:
    regex = r'0([0-9]{9})$'
    found = re.match(regex, mobile_number)
    return True if found else False


def to_json(data: Union[List[Dict[str, str]], Dict[str, str], str]) -> str:
    return json.dumps(data) if not isinstance(data, str) else ''


def insert_query(table_name: str, data: dict, return_key: str = None) -> str:
    values = tuple(value if not isinstance(value, datetime) else str(value) for value in data.values())
    query = f"""
       INSERT INTO {table_name} ({','.join(data.keys())}) VALUES
       {values}
   """
    if return_key:
        query += f"returning {return_key};"
    return query


def slugify(text: str):
    text = unidecode.unidecode(text).lower()
    text = re.sub(r'[\W_]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def convert_chapter(text: str):
    texts = text.strip().split(" ")
    result = [str(_number) for _number in texts if _number.isdigit()]
    if len(result) > 0:
        return f"Chương {result[0]}"
    return text


def load_pickle(filename: str):
    with open(filename, "rb") as infile:
        # Load the dictionary from the file
        my_dict = pickle.load(infile)
    return my_dict


def save_pickle(data):
    with open("my_dict.pickle", "wb") as outfile:
        pickle.dump(data, outfile)


async def load_pickle_upload_file(file: UploadFile) -> [bool, str, Any, str]:
    try:
        file_name = file.filename
        content = await file.read()
        loaded_pickle = pickle.loads(content)
        return True, file_name, loaded_pickle, None
    except Exception as ex:
        return False, None, None, ex


def get_number_from_str(text) -> str:
    pattern = r'\d+\.?\d*'
    matches = re.findall(pattern, text)
    return matches[0]


def remove_empty_dict_key(data: dict) -> dict:
    return {key: value for key, value in data.items() if
            value is not None and value != '' and value != -1 and value != '-1'}



def load_json(text):
    try:
        return json.loads(text)
    except Exception as ex:
        loguru.logger.error(f"load_json ex: {ex}")
        return text


def write_log(client_id, request_id, rotation: str = '10 MB') -> bool:
    folder_path = os.path.abspath(os.getcwd()) + f"/logs/{client_id}/{request_id}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # bot_success_path = folder_path + f"/success.log"
    # bot_warning_path = folder_path + f"/warning.log"
    # bot_error_path = folder_path + f"/error.log"
    # handlers = [item._name.replace("'", "") for item in loguru.logger._core.handlers.values()]
    # if bot_success_path not in handlers:
    # loguru.logger.add(bot_success_path, filter=lambda record: record["level"].name == 'SUCCESS',rotation=rotation)
    # loguru.logger.add(bot_warning_path, filter=lambda record: record["level"].name == 'WARNING',rotation=rotation)
    # loguru.logger.add(bot_error_path, filter=lambda record: record["level"].name == 'ERROR', rotation=rotation)
    loguru.logger.add(folder_path + "/request.log", rotation=rotation)
    return True


def get_fernet_key(is_webhook_key: bool = False):
    key = "Z4R5cMeA4gwIId20WGdzdyMO4pg8yHh7PgR_14PX7hY="
    key_bytes = key.encode('utf-8')
    fernet = Fernet(key_bytes)
    return fernet


def get_hash(message):
    return hashlib.sha256(message.encode()).hexdigest()


def encrypt(message, is_webhook_key: bool = False) -> Union[bool, Any, Any]:
    try:
        if isinstance(message, dict):
            message = json.dumps(message)
        fernet = get_fernet_key(is_webhook_key=is_webhook_key)
        encrypted_message = fernet.encrypt(message.encode('utf-8'))
        return True, encrypted_message.decode('utf-8'), None
    except Exception as ex:
        False, None, str(ex)


def decrypt(encrypted_message: str, return_json=False, is_webhook_key: bool = False) -> Union[bool, Any, Any]:
    try:
        fernet = get_fernet_key(is_webhook_key=is_webhook_key)
        encrypted_message = fernet.decrypt(encrypted_message)
        if return_json:
            return True, json.loads(encrypted_message), None
        return True, encrypted_message.strip(), None
    except Exception as ex:
        False, None, str(ex)


def sha256(message):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode())
    hex_digest = sha256_hash.hexdigest()
    return hex_digest
