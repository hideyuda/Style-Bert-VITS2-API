import base64
import json
import requests
import wave
from io import BytesIO

url = "https://api.runpod.ai/v2/xxxxxxxxxxxxx/runsync"
api_key = "GFD304DOHXXXXXXXXXXXXE635"

text = """ギャル語でファストエーピーアイについて説明するって、マジでやばいチャレンジだけど、やってみるね！

まずさ、ファストエーピーアイっていうのは、ウェブアプリケーションとかAPIをサクッと作れる超便利なツールなの。パイソンで書かれてるから、パイソン好きな人にはマジでたまんないよね。

で、なんでファストエーピーアイがそんなに人気なのかっていうと、まずめっちゃ速いってこと。非同期処理がデフォでできるから、同時にたくさんのリクエストをバリバリ処理できちゃうの。これが、例えばフラスクとか他のフレームワークと比べても、ファストエーピーアイの大きなウリなわけ。

あと、ファストエーピーアイは自動でドキュメントを生成してくれるの。これがまた便利で、APIを作ったらすぐにそのAPIの使い方がわかるドキュメントが手に入るってわけ。開発がラクになるし、チームで作業してる時もコミュニケーションがスムーズになるよね。

コードの書き方もシンプルで、型ヒントを使ってパラメータの型を指定するだけで、自動的にリクエストのバリデーションとかもやってくれるの。これがまたエラーを減らしてくれるから、開発スピードがグンと上がるんだよね。

使い方もめっちゃ簡単で、ファストエーピーアイのインスタンスを作って、デコレータを使ってルーティングを設定するだけ。あとはそのルートで何をするかを関数で書くだけで、もうAPIの完成ってわけ。

こんな感じで、ファストエーピーアイは開発が速い、処理も速い、使いやすいっていう三拍子揃った最強のフレームワークなの。API作るなら、マジでファストエーピーアイおすすめだよ！"""

file_path = "runpod_test_voice.wav"
model_id = 0


# APIから音声データを取得する関数
def fetch_audio_from_api(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "input": {
            "action": "/voice",
            "model_id": model_id,
            "text": text,
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return base64.b64decode(response.json()["output"]["voice"])
    else:
        raise Exception(f"API call failed with status code {response.status_code}")


# 沈黙（無音）のデータを生成する関数
def generate_silence(duration_ms, sample_rate, num_channels):
    num_samples = int(sample_rate * duration_ms / 1000.0)
    # 16ビットの無音データは0で、num_channels分のチャンネルごとに0を配置
    silence_data = (b"\x00\x00" * num_samples) * num_channels
    return silence_data


# テキストを一文字ずつ処理し、句読点ごとに音声データを取得して結合する関数
def process_text_and_fetch_audio(text, file_path):
    output_wav = wave.open(file_path, "wb")
    first = True
    segment = ""
    for char in text:
        if char in ["。", "、"]:
            if segment:
                audio_data = fetch_audio_from_api(segment)
                with wave.open(BytesIO(audio_data), "rb") as wav_file:
                    if first:
                        output_wav.setparams(wav_file.getparams())
                        first = False
                    output_wav.writeframes(wav_file.readframes(wav_file.getnframes()))
                segment = ""
            silence_duration_ms = 700 if char == "。" else 300
            silence_data = generate_silence(
                silence_duration_ms,
                output_wav.getframerate(),
                output_wav.getnchannels(),
            )
            output_wav.writeframes(silence_data)
        else:
            segment += char
    # 最後のセグメントがあれば処理
    if segment:
        audio_data = fetch_audio_from_api(segment)
        with wave.open(BytesIO(audio_data), "rb") as wav_file:
            output_wav.writeframes(wav_file.readframes(wav_file.getnframes()))
    output_wav.close()


if __name__ == "__main__":
    try:
        process_text_and_fetch_audio(text, file_path)
        print(f"Audio saved to {file_path}")
    except Exception as e:
        print(f"Error: {e}")
