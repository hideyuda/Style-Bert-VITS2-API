import time

import runpod
import base64
import requests
from requests.adapters import HTTPAdapter, Retry

API_URL = "http://127.0.0.1:5000"


automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount("http://", HTTPAdapter(max_retries=retries))


def wait_for_service(url):
    while True:
        try:
            requests.get(url)
            return
        except requests.exceptions.RequestException as e:
            print(f"Service not ready yet. Retrying... Error: {e}")
        except Exception as err:
            print("Error: ", err)

        time.sleep(0.2)


def inference(params):
    # params={
    #     "model_id": model_id,
    #     "encoding": "utf-8",
    #     "text": text,
    # },
    response = automatic_session.get(
        url=f"{API_URL}/voice",
        params=params,
        timeout=60,
    )

    print(response.status_code)
    audio_wav = response.content

    # wav音源をbase64に変換する
    audio_base64 = base64.b64encode(audio_wav).decode("utf-8")

    return {"voice": audio_base64}


def models_info():
    response = automatic_session.get(
        url=f"{API_URL}/models/info",
        timeout=60,
    )
    return response.json()


def handler(event):
    print("Event: ", event)
    params = event["input"]
    action = params["action"]

    if action == "/voice":
        print("Inference API is called.")
        return inference(params)
    elif action == "/models/info":
        print("Models info API is called.")
        return models_info()
    else:
        return {"error": "Unknown action"}


if __name__ == "__main__":
    wait_for_service(url=f"{API_URL}/models/info")

    print("API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler})
