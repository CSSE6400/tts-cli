#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from pathlib import Path

from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


@click.command()
@click.option('--model', default='tts_models/en/ek1/tacotron2')
@click.option('--input-file')
@click.option('--output-path', default="out")
@click.option('--output-name', default="example")
def main(model: str, input_file: str, output_path: str, output_name: str):
    # load model manager
    path = Path(__file__).parent / ".models.json"
    manager = ModelManager(path)

    model_path, config_path, model_item = manager.download_model(model)
    vocoder_path, vocoder_config_path, _ = manager.download_model(model_item["default_vocoder"])

    # load models
    synthesizer = Synthesizer(
        model_path,
        config_path,
        "",
        "",
        vocoder_path,
        vocoder_config_path,
        "",
        "",
        False,
    )

    # RUN THE SYNTHESIS
    print(" > Text: {}".format("todo: read from input"))

    # kick it
    wav = synthesizer.tts("todo: read from input")

    # save the results
    print(" > Saving output to {}".format(output_path))
    synthesizer.save_wav(wav, output_path + f'/{output_name}.wav')


if __name__ == "__main__":
    main()
