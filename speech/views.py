from django.shortcuts import render
from django.http import JsonResponse
import requests
import time
from django.http import HttpResponse
def make_fetch_request(url, headers, method='GET', data=None):
    if method == 'POST':
        response = requests.post(url, headers=headers, json=data)
        print("Post ------ data check first", response.json())
    else:
        response = requests.get(url, headers=headers)
        print("get ----- ", response.json())
    return response.json()

def index(request):
    gladia_key = "f129d9c3-781d-42d1-bde9-745e233c8750"
    # gladia_key = "7ae2f26b-f07a-48ec-ad23-ed029d48d97f"

    request_data = {"audio_url": "https://testasdsf.s3.amazonaws.com/live_recording.mp3"}
    gladia_url = "https://api.gladia.io/v2/transcription/"

    headers = {
        "x-gladia-key": gladia_key,
        "Content-Type": "application/json"
    }

    print("- Sending initial request to Gladia API...")
    initial_response = make_fetch_request(gladia_url, headers, 'POST', request_data)

    print("Initial response with Transcription ID:", initial_response)
    result_url = initial_response.get("result_url")

    orignal_audio = {}
    if result_url:
        while True:
            # print("Polling for results...")
            poll_response = make_fetch_request(result_url, headers)
            
            if poll_response.get("status") == "done":
                print("- Transcription done: \n")
                print(poll_response.get("result", {}).get("transcription", {}).get("full_transcript"))
                orignal_audio=poll_response.get("result", {}).get("transcription", {}).get("full_transcript")
                break
            else:
                print("Transcription status:", poll_response.get("status"))
            time.sleep(1)
    return JsonResponse(poll_response, safe=False)    
    
def video_content(request):
    gladia_key = "f129d9c3-781d-42d1-bde9-745e233c8750"
    request_data = {"audio_url": "	http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"}
    gladia_url = "https://api.gladia.io/v2/transcription/"
    headers = {
        "x-gladia-key": gladia_key,
        "Content-Type": "application/json"
    }
    initial_response = make_fetch_request(gladia_url, headers, 'POST', request_data)
    result_url = initial_response.get("result_url")
    orignal_audio = {}
    if result_url:
        while True:
            poll_response = make_fetch_request(result_url, headers)
            if poll_response.get("status") == "done":
                orignal_audio=poll_response.get("result", {}).get("transcription", {}).get("full_transcript")
                break
            else:
                print("Transcription status:", poll_response.get("status"))
            time.sleep(1)
    return JsonResponse(poll_response, safe=False)

