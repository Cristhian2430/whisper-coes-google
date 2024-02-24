import torch
from transformers import pipeline
import pandas as pd
import os
from datasets import Dataset, DatasetDict
import datasets
from transformers.pipelines.pt_utils import KeyDataset
from tqdm.auto import tqdm
import logging
import warnings
from io import BytesIO
from google.oauth2 import service_account
from google.cloud import storage
print("Importados los modulos")

#def handler(event, context):
#    response = {"statusCode":200,
#                "body":"hello"}
#    return response
warnings.filterwarnings("ignore", message="Length of IterableDataset.*")
print("Desactivaron Alarmas")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("Asigno procesador")
train_df = pd.DataFrame(columns = ["cont", "audio", "Resultado"])
print("Definio DataFrame")
google_credentials = service_account.Credentials.from_service_account_file("whispercoes-4f68b3a61a92.json")
print("Obtuvieron Credenciales")
storage_client = storage.Client(credentials = google_credentials)
print("Asignó la variable Credenciales")
transcribe = pipeline(
                      task            = "automatic-speech-recognition",
                      model           = "model/",
                      chunk_length_s  = 30,
                      device          = device
                      )
print("Se importó modelo")
transcribe.model.config.forced_decoder_ids = transcribe.tokenizer.get_decoder_prompt_ids(language="es", task="transcribe")
print("Seteo parámetro")
def main():
    global train_df, storage_client
    print("Conecto a Bucket Google")
    blobs = storage_client.list_blobs("prueba-coes1")
    cont = 0
    print("Inicia Bucle en Bucket")
    for blob in blobs:
        if blob.name.endswith(".opus"):
            train_df = pd.concat([train_df, pd.DataFrame({'cont': [cont], 'audio': [blob.name]})], ignore_index=True)
            audio_data = blob.download_as_string()
            train_df.loc[cont, "Resultado"] = transcribe(audio_data)["text"]
            print(blob.name)
            cont = cont + 1
    print("Termino Bucle")
    excel_buffer = BytesIO()
    train_df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0) 
    print("Se transformó DataFrame en Bytes")
    bucket = storage_client.bucket("prueba-coes1")
    blob = bucket.blob("prueba_whisper.xlsx")
    generation_match_precondition = 0
    print("Se empezará a enviar")
    blob.upload_from_file(excel_buffer, 
                            if_generation_match = generation_match_precondition,
                            content_type        = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            )
    print("Se envió la información")
    print(train_df)

    warnings.resetwarnings()

if __name__ == "__main__":
    main()