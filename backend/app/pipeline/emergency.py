class EmergencyKillSwitch:
    """
    Global Emergency Kill Switch.
    Can be toggled via Admin Dashboard or API to immediately freeze autonomous publishing and generation.
    """
    _is_active: bool = False

    @classmethod
    def activate(cls, reason: str = "Manual Admin Emergency Stop"):
        cls._is_active = True

    @classmethod
    def deactivate(cls):
        cls._is_active = False

    @classmethod
    def is_triggered(cls) -> bool:
        return cls._is_active
