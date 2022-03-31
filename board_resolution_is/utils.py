def get_int_or_none(text: str):
    try:
        return int(text)
    except:
        return None


def get_form_errors(tests: list[tuple[bool, str]]):
    errors = []

    for passed, error_message in tests:
        if not passed:
            errors.append(error_message)

    return errors
