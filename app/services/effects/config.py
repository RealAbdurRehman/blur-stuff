ANONYMIZATION_CONFIG = {
    "faces": {
        "padding": 0.3,
    },
    "plates": {
        "padding": 0.08,
    },
    "text": {
        "padding": 0.1,
    },
    "pii": {
        "padding": 0.1,
    },
}

MODE_OVERRIDES = {
    "inpaint": {
        "faces": {
            "padding": 0.8,
        },
    }
}


def get_effect_config(mode, target, padding=None):
    config = ANONYMIZATION_CONFIG[target].copy()
    override = MODE_OVERRIDES.get(mode, {}).get(target, {})
    config.update(override)

    if padding is not None:
        config["padding"] = padding

    return config
