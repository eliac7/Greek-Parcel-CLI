# HTTP Configuration
DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Courier Names
COURIER_NAMES = [
    "acs",
    "couriercenter",
    "easymail",
    "elta",
    "geniki",
    "skroutz",
    "speedex",
]

# Status Messages
STATUS_TRACKING = "Tracking {tracking_number} with {courier}..."
STATUS_PACKAGE_NOT_FOUND = "Package not found or error occurred for {courier_name}"
STATUS_DELIVERED = "✅ Delivered"
STATUS_IN_TRANSIT = "🚚 in transit..."

# Delivery Status Indicators
DELIVERY_INDICATORS = {
    "couriercenter": "(29) DeliveryCompleted",
    "easymail": "Παραδόθηκε",
    "elta": "Αποστολή παραδόθηκε",
    "speedex": "Η ΑΠΟΣΤΟΛΗ ΠΑΡΑΔΟΘΗΚΕ",
}

# Error Messages
ERROR_UNKNOWN_COURIER = "Unknown courier: {courier}"
ERROR_TRACKING_PACKAGE = "Error tracking package: {error}"
