from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource, abort
from youtube_transcript_api import YouTubeTranscriptApi
import Summarize
from urllib.parse import *
from waitress import serve

app = Flask(__name__)
api = Api(app)


# https://youtu.be/s_Zmgx-HTAw

# initial version: http://stackoverflow.com/a/7936523/617185 \
#    by Mikhail Kashkin(http://stackoverflow.com/users/85739/mikhail-kashkin)

def get_yt_video_id(url):
    """Returns Video_ID extracting from the given url of Youtube

    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',

      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """
    if url.startswith(('youtu', 'www')):
        url = 'http://' + url

    query = urlparse(url)

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError


class Summary(Resource):
    def get(self):
        video_link = request.args["link"]
        if len(video_link) == 0:
            abort(404)
        if not request.args:
            abort(400)
        video_id = get_yt_video_id(video_link)
        transcript_string = Transcript.get(video_id)
        summarized_text = Summarize.summarize(transcript_string)
        return jsonify(result=summarized_text, message="success")


class Transcript(Resource):
    def transcript_parser(video_id):
        transcript_parsed = ""
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for elt in transcript:
            transcript_parsed += elt["text"] + "\n"
        return transcript_parsed

    def get(video_id=None):

        if video_id is None:
            video_id = request.args["video_id"]
        # print(video_id)
        trans = Transcript.transcript_parser(video_id)
        return trans


api.add_resource(Transcript, "/transcript/")
api.add_resource(Summary, "/summary/")


@app.route('/web/')
def summarizer_web():
    # We are at web.html, online input boxes are there to summarize the given video URL.
    # Displaying web.html to the end user
    return render_template('web.html')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # serve( , host='0.0.0.0', port=8080)
    app.run()
