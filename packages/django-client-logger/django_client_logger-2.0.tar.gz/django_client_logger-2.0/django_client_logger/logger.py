import logging
import hashlib


def process_log_message(message, session_key, override_user, original_user):
    for entry in message:
        session_hash = hashlib.md5(session_key.encode('utf-8')).hexdigest()
        entry['session_key'] = session_hash
        entry['override_user'] = override_user
        entry['original_user'] = original_user
        write_log(entry['logger'], entry)


def write_log(log_name, entry):
    logger = logging.getLogger(log_name)
    logger.info(entry)
