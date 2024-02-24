#FROM public.ecr.aws/lambda/python:3.12
FROM python:3.12

RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    apt-get clean

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/* ${LAMBDA_TASK_ROOT}

RUN mkdir model
RUN curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/config.json -o ./model/config.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/model.safetensors.index.json -o ./model/model.safetensors.index.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/model-00001-of-00002.safetensors -o ./model/model-00001-of-00002.safetensors \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/model-00002-of-00002.safetensors -o ./model/model-00002-of-00002.safetensors \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/generation_config.json -o ./model/generation_config.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/tokenizer_config.json -o ./model/tokenizer_config.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/vocab.json -o ./model/vocab.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/merges.txt -o ./model/merges.txt \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/normalizer.json -o ./model/normalizer.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/added_tokens.json -o ./model/added_tokens.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/special_tokens_map.json -o ./model/special_tokens_map.json \
    && curl -L https://huggingface.co/Cristhian2430/whisper-large-coes-v3/resolve/main/preprocessor_config.json -o ./model/preprocessor_config.json

#EXPOSE 8080

CMD ["python", "main.py"]

#CMD ["main.handler"]