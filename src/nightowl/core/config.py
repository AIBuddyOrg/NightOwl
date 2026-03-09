from dataclasses import dataclass, field


@dataclass(slots=True)
class AppConfig:
    """Top-level application configuration.

    Keep this generic so SIS/SMS implementations can plug in tenant-specific values.
    """

    environment: str = "dev"
    default_language: str = "en"
    escalation_confidence_threshold: float = 0.72
    enable_mcp: bool = False
    mcp_server_url: str | None = None
    allowed_channels: tuple[str, ...] = ("whatsapp",)
    metadata: dict[str, str] = field(default_factory=dict)
