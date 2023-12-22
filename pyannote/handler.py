import runpod
from input_schema import INPUT_SCHEMA
from model import DiarizePyannote
from runpod.serverless.utils.rp_validator import validate
from utils import decode_audio

d = DiarizePyannote()
d.setup()


async def handler(job):
    job_input = job["input"]
    input_validation = validate(job_input, INPUT_SCHEMA)
    if "errors" in input_validation:
        return {"error": input_validation["errors"]}

    job_input = input_validation["validated_input"]

    task = job_input["task"]
    waveform, sampling_rate = decode_audio(
        job_input["audio_base64"], job_input["audio_brotli"]
    )

    if sampling_rate != 16000:
        return {"error": "sampling rate must be 16000"}

    if task == "diarize":
        res = d.run(waveform, sampling_rate)
        return {
            "result": res,
            # "user_id": job_input["user_id"] if "user_id" in job_input else None,
            "room_id": job_input["room_id"] if "room_id" in job_input else None,
        }

    return {"error": "unknown task"}


def concurrency_modifier(current_concurrency=1):
    desired_concurrency = 120

    return desired_concurrency


runpod.serverless.start(
    {"handler": handler, "concurrency_modifier": concurrency_modifier}
)
