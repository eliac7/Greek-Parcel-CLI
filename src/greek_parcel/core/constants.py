# HTTP Configuration
DEFAULT_TIMEOUT = 10



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
