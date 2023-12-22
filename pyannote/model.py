import torch
from pyannote.audio import Model
from pyannote.audio.pipelines import SpeakerDiarization
from runpod.serverless.utils import rp_cuda


class DiarizePyannote:
    def get_emb_model(self):
        return

    def setup(self):
        self.emb = Model.from_pretrained("pyannote/wespeaker-voxceleb-resnet34-LM.bin")
        self.segmentation = Model.from_pretrained(
            "pyannote/pyannote-segmentation-3.0.bin"
        )

        pipeline = SpeakerDiarization(self.segmentation, embedding=self.emb).to(
            torch.device("cuda") if rp_cuda.is_available() else torch.device("cpu")
        )
        pipeline.instantiate(
            {
                "segmentation": {
                    "min_duration_off": 0.0,
                },
                "clustering": {
                    "method": "centroid",
                    "min_cluster_size": 12,
                    "threshold": 0.7045654963945799,
                },
            }
        )
        self.pipeline = pipeline
        print("pipeline initialized")

    def run(self, waveform, sampling_rate):
        diarization, embeddings = self.pipeline(
            {"waveform": waveform, "sample_rate": sampling_rate}, return_embeddings=True
        )

        res = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_n = int(speaker.split("_")[1])
            emb = embeddings[speaker_n]
            res.append(
                {
                    "start": turn.start,
                    "end": turn.end,
                    "emb": emb.tolist(),
                }
            )

        return res
