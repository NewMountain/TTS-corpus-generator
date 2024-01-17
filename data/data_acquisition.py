# This file is intended to show how the data was sourced from [Cognitive-Speech-TTS](https://github.com/Azure-Samples/Cognitive-Speech-TTS)
# We are grabbing the US English datasets

# Note: This script is intended to run on Python 3.x (run on 3.9) and assumes the requests and pandas libraries (pip install requests pandas)
# have been installed. This assumes you are running the python script data_acquisition.py from the ./data directory

import pandas as pd
import requests as rq

YOUR_NAME = "YOUR NAME HERE"
YOUR_COMPANY = "YOUR COMPANY HERE"

GENERAL_TEXT_URI = "https://raw.githubusercontent.com/Azure-Samples/Cognitive-Speech-TTS/master/CustomVoice/script/English%20(United%20States)_en-US/0000000001_0300000050_General.txt"
CHAT_TEXT_URI = "https://raw.githubusercontent.com/Azure-Samples/Cognitive-Speech-TTS/master/CustomVoice/script/English%20(United%20States)_en-US/3000000001_3000000300_Chat.txt"
CUSTOMER_SERVICE_URI = "https://raw.githubusercontent.com/Azure-Samples/Cognitive-Speech-TTS/master/CustomVoice/script/English%20(United%20States)_en-US/4000000001_4000000300_CustomerService.txt"
# As of Jan 16, 2024, the authorization text is "I  [state your first and last name] am aware that recordings of my voice will be used by [state the name of the company] to create and use a synthetic version of my voice."
# This will be hard-coded into the dataset at this time
# SPEAKER_AUTHORIZATION_URI = "https://raw.githubusercontent.com/Azure-Samples/Cognitive-Speech-TTS/master/CustomVoice/script/English%20(United%20States)_en-US/SpeakerAuthorization.txt"

TEXT_SOURCES = [
    {"name": "general_text", "uri": GENERAL_TEXT_URI},
    {"name": "chat_text", "uri": CHAT_TEXT_URI},
    {"name": "customer_service_text", "uri": CUSTOMER_SERVICE_URI},
]


def acquire_datasets():
    for source in TEXT_SOURCES:
        uri = source["uri"]
        res = rq.get(uri)
        text = res.text
        source["content"] = text


def normalize_data():
    for source in TEXT_SOURCES:
        clean_data = []

        content = source["content"]
        for line in content.strip().split("\n"):
            # The line is tab separated between some microsoft id and the sentence
            try:
                ms_id, text = line.strip().split("\t")
                data = {"ms_id": ms_id.strip(), "text": text.strip()}
                clean_data.append(data)
            except ValueError:
                # Just in case
                print("Error with line:", line)

        df = pd.DataFrame(clean_data)

        source["data"] = df


def create_csv_files():
    for source in TEXT_SOURCES:
        df = source["data"]
        name = source["name"]
        df.to_csv(f"./{name}.csv")


def create_and_save_merged_dataset():
    # I have no doubt there's some esoteric pandas api to do this faster / more efficiently
    frames = [source["data"] for source in TEXT_SOURCES]
    # authorization frame
    df = pd.DataFrame(
        [
            {
                "ms_id": "auth",
                "text": f"I {YOUR_NAME} am aware that recordings of my voice will be used by {YOUR_COMPANY} to create and use a synthetic version of my voice.",
            }
        ]
    )

    frames.append(df)

    df_merged = pd.concat(frames, ignore_index=True)
    df_merged.reset_index()

    df_merged.to_csv("./merged_dataset.csv")


def main():
    # TEXT_SOURCES is mutated in place and is hydrated with "content"
    acquire_datasets()

    # Next, convert the datasets into csv files with just the sentence we need to read
    # again, these dataframes are saved as "data"
    normalize_data()

    # Create the csv files under /data
    create_csv_files()

    # Create a merged document of all unique sentences and the final file, your authorization
    create_and_save_merged_dataset()


if __name__ == "__main__":
    main()
