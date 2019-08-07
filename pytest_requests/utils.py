
def parse_content(content, kwargs):

    if isinstance(content, dict):
        return {
            key: parse_content(value, kwargs)
            for key, value in content.items()
        }

    elif isinstance(content, list):
        return [
            parse_content(item, kwargs)
            for item in content
        ]

    elif isinstance(content, str):
        return content.format(**kwargs)

    else:
        return content
