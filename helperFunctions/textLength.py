def text_length_checker(regex_object):
    if regex_object is None:
        return None
    else:
        return len(regex_object.group())
