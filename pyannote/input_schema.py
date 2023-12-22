INPUT_SCHEMA = {
    "audio_base64": {"type": str, "required": True, "default": None},
    "audio_brotli": {"type": bool, "required": False, "default": False},
    "task": {"type": str, "required": True, "default": None},
    "room_id": {"type": str, "required": False, "default": None},
}
