from flask import Flask, render_template, jsonify, request
# from constants.topics import TOPICS
from agents.GenerateSummary import generateInterviewSummary
from agents.ProcessTranscript import processTranscript

app = Flask(__name__, template_folder='templates',
            static_folder='static', static_url_path='/static')


@app.route('/')
def hello_world():
    """Route to display Hello World page."""
    return render_template('index.html')


# @app.route('/api/topics')
# def get_topics():
#     """API endpoint to get available topics."""
#     return jsonify({'topics': TOPICS})


@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit_form():
    """Handle form submission from the web page."""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No JSON data received'}), 400

        interview_id = data.get('interviewId')
        topicName = data.get('topic')
        skip_transcript = data.get('skipTranscript', False)
        generate_summary = data.get('generateSummary', False)
        analyze_transcript = data.get('analyzeTranscript', False)
        incorrect_question_input = data.get('improvementQuestions', '')
        gender = data.get('gender', '')

        # Validate required fields
        if not interview_id or not topicName:
            return jsonify({'message': 'Missing required fields'}), 400

        if generate_summary:
            output_file = generateInterviewSummary({
                'interviewId': interview_id,
                'topicName': topicName,
                'incorrect_question_input': incorrect_question_input,
                'gender': gender
            })
            # Return success response
            return jsonify({
                'results': str(output_file) if generate_summary else None,
            }), 200
        if analyze_transcript:
            transcript_summary = processTranscript(skip_transcript, topicName)
            return jsonify({
                'results': transcript_summary
            }), 200
        else:
            return jsonify({'message': 'Summary generation not requested'}), 200
    except Exception as e:
        print(f"Error processing submission: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.before_request
def log_request():
    """Log incoming requests for debugging."""
    print(f"[{request.method}] {request.path}")
    if request.method == 'POST':
        print(f"  Content-Type: {request.content_type}")


if __name__ == '__main__':
    print("Starting Flask app...")
    print(f"Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule}")
    app.run(debug=True, port=5000, use_reloader=True)
