from plyer import notification


def send_notification(title: str, message: str):
    """
    Send a desktop notification.

    Args:
        title: Notification title
        message: Notification body
    """
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Greek Parcel CLI",
            timeout=10,
        )
    except Exception as e:
        # Fallback to print if notification fails
        print(f"\n[!] Notification failed: {e}")
        print(f"[*] {title}: {message}")
