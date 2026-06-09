def validate_threshold(value):

    try:
        threshold = float(value)
    except (ValueError, TypeError):
        raise ValueError("threshold must be numeric")

    if threshold < 0 or threshold > 1:
        raise ValueError("threshold must be between 0 and 1")

    return threshold
