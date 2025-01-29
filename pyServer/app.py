from flask import Flask, request, Response, render_template_string, send_file
import os

app = Flask(__name__)



####################################################################################################################################################################################################################################################################

directory_to_list = "E:/pyServer"  # EDIT a directory which you want to share

####################################################################################################################################################################################################################################################################



@app.route("/")
def list_files():
    try:
        files = os.listdir(directory_to_list)
        message = "Select a file to play or download:" if files else "The directory is empty."
    except FileNotFoundError:
        message = "The specified directory does not exist."
        files = []

    file_list_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Directory Browser</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; display: flex; justify-content: space-between; align-items: center; }
            a { text-decoration: none; color: #007bff; font-weight: bold; }
            a:hover { text-decoration: underline; }
            .button { background-color: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px; }
            .button:hover { background-color: #218838; }
        </style>
    </head>
    <body>
        <h2>Directory Browser</h2>
        <p>{{ message }}</p>
        <ul>
            {% for file in files %}
                <li>
                    <a href="/view/{{ file }}">{{ file }}</a>
                    <a href="/download/{{ file }}" class="button">Download</a>
                </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(file_list_html, files=files, message=message)


@app.route("/view/<path:filename>")
def view_file(filename):
    file_path = os.path.join(directory_to_list, filename)

    # Serve video files directly in a player
    if filename.lower().endswith((".mp4", ".mkv", ".webm")):
        player_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Playing {filename}</title>
            <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }}
                video {{ width: 800px; max-width: 100%; }}
                .buttons {{ margin-top: 15px; }}
                .button {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; }}
                .button:hover {{ background-color: #0056b3; }}
            </style>
        </head>
        <body>
            <h2>Playing: {filename}</h2>
            <video id="video-player" class="video-js vjs-default-skin" controls preload="auto">
                <source src="/stream/{filename}" type="video/webm">
                Your browser does not support the video tag.
            </video>
            <div class="buttons">
                <a href="/download/{filename}" class="button">Download Video</a>
            </div>
            <script src="https://vjs.zencdn.net/7.20.3/video.js"></script>
        </body>
        </html>
        """
        return player_html

    # Handle non-video file types by directly rendering or prompting download
    try:
        return send_file(file_path)
    except FileNotFoundError:
        return "File not found", 404


@app.route("/stream/<path:filename>")
def stream_video(filename):
    file_path = os.path.join(directory_to_list, filename)
    try:
        file_size = os.path.getsize(file_path)
        range_header = request.headers.get("Range", None)

        # Handle byte range requests for video streaming
        if range_header:
            byte1, byte2 = 0, None
            match = range_header.replace("bytes=", "").split("-")
            if match[0]:
                byte1 = int(match[0])
            if match[1]:
                byte2 = int(match[1])

            length = (byte2 - byte1 + 1) if byte2 is not None else file_size - byte1
            with open(file_path, "rb") as f:
                f.seek(byte1)
                data = f.read(length)
                response = Response(data, status=206, mimetype="video/webm")
                response.headers.add("Content-Range", f"bytes {byte1}-{byte1 + length - 1}/{file_size}")
                response.headers.add("Accept-Ranges", "bytes")
                return response

        # Default full file response
        with open(file_path, "rb") as f:
            data = f.read()
            return Response(data, mimetype="video/webm")

    except FileNotFoundError:
        return "File not found", 404


@app.route("/download/<path:filename>")
def download_file(filename):
    file_path = os.path.join(directory_to_list, filename)
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404


if __name__ == "__main__":
    app.run(debug=True)
