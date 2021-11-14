from flask import Flask, request
from flask_restful import Api, Resource
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
api = Api(app)


class Transcript(Resource):
    def transcript_parser(video_id):
        transcript_parsed = ""
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for elt in transcript:
            transcript_parsed += elt["text"] + "\n"
        return transcript_parsed

    def get(self):
        video_id = request.json["video_id"]
        print(video_id)
        trans = Transcript.transcript_parser(video_id)
        return trans

    def put(self):
        return "put success"

    def delete(self):
        return "del success"


api.add_resource(Transcript, "/api/videos/")


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
