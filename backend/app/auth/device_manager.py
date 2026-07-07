from hashlib import sha256


class DeviceManager:

    @staticmethod
    def generate_device_id(
        user_agent: str,
        ip_address: str
    ) -> str:

        raw = f"{user_agent}:{ip_address}"

        return sha256(
            raw.encode()
        ).hexdigest()

    @staticmethod
    def verify_device(
        stored_device: str,
        user_agent: str,
        ip_address: str
    ) -> bool:

        current = DeviceManager.generate_device_id(
            user_agent,
            ip_address
        )

        return current == stored_device
