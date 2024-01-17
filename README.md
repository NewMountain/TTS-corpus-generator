# TTS-corpus-generator

Simple web app to bootstrap a TTS dataset

## Purpose

This application is intended to allow the user to quickly generate a text-to-speech (TTS) training corpus. The data is originally supplied by Azure Samples in their [Cognitive-Speech-TTS](https://github.com/Azure-Samples/Cognitive-Speech-TTS) repo.

That data has been slightly modified here to fit into a CSV format which is then used by a web application allowing the user to quickly generate the required wav files for training.

The UI is not functional and practical, but not going to win any awards. The point is to be very quick and easy to generate the dataset you need to create a custom TTS voice.

## Usage

The data has already been sourced. The Demo is intended to run against `./data/merged_dataset.csv`. It is advised that you update the last row
of that CSV to reflect your use case (adjust your name and company).

Once that is set up, move to the `./src` directory run `python app.py`. Note, for this to work, you will need Flask installed (pip install flask).

The application will create an `./audio` directory in application root if it does not already exist. Open `http://localhost:5000` in a browser of your
choice. The workflow from that point should be self explanatory. Follow the instructions to create, sentence by sentence, the dataset required to train
a custom voice TTS model.

If ever you need to stop, you can shut down the application. On restart, the program will check the `./audio` directory for the last sample and advance
you to the next sample and let you know when you are done.

## Requirements

For the basic web application:

```text
Python >= 3.9
flask
```

For the data acquisition (you can just use the csvs, but in case you want to start over)

```text
python >= 3.9
pandas
requests
```

Library versions shouldn't matter as we're using extremely basic functionality.

## Credit

The datasets are originally from [Azure-Samples/Cognitive-Speech-TTS](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/English%20(United%20States)_en-US/0000000001_0300000050_General.txt).

The repo is [MIT licensed](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/LICENSE.md)
