import ua_generator

def get_random_user_agent() -> str:
    """
    Returns a random modern User-Agent string using ua-generator.
    """
    ua = ua_generator.generate(device="desktop", browser=("chrome", "edge", "firefox", "safari"))
    return ua.text
