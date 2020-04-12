import time

import magic_admin


def epoch_time_now():
    return int(time.time())


def apply_did_token_nbf_grace_period(timestamp):
    return timestamp - magic_admin.did_token_nbf_grace_period_s
