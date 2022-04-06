#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from pathlib import Path

import click
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


def filter_input_sentance(sentance):
    sentance = "".join(filter(lambda character: character.isalpha() or character in ".,:;!?", sentance))
    return sentance.strip().strip(".")

def filter_input(input):
    return ". ".join(filter(None, map(filter_input_sentance, input))) + "."

@click.command()
@click.option('--model', default='tts_models/en/ek1/tacotron2')
@click.option('--input-file', required=True)
@click.option('--output', default="out/example.wav")
def main(model: str, input_file: str, output: str):
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

    with open(input_file) as f:
        contents = filter_input(f.readlines())

    # RUN THE SYNTHESIS
    print(" > Text: {}".format(contents))

    # kick it
    wav = synthesizer.tts(contents)

    # save the results
    output_path = output if output.endswith(".wav") else output + ".wav"
    print(" > Saving output to {}".format(output_path))

    directory = os.path.dirname(output_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    synthesizer.save_wav(wav, output_path)


if __name__ == "__main__":
    main()
