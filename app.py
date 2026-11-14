from flask import Flask, jsonify, render_template, request
from playlist import Playlist

app = Flask(__name__)
playlist = Playlist()  # เก็บ Playlist ไว้ในหน่วยความจำขณะ Server ทำงาน


def response(message="", ok=True):
    return jsonify({"ok": ok, "message": message, "state": playlist.get_state()})


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/state")
def get_state():
    return jsonify(playlist.get_state())


@app.post("/api/add")
def add_song():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return response("กรุณาใส่ชื่อเพลง", False), 400
    playlist.add(title)
    return response(f"เพิ่มเพลง {title} แล้ว")


@app.post("/api/insert")
def insert_song():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return response("กรุณาใส่ชื่อเพลง", False), 400
    playlist.insert_after_current(title)
    return response(f"แทรกเพลง {title} หลังเพลงปัจจุบันแล้ว")


@app.post("/api/play")
def play_song():
    title = playlist.play_song()
    if title is None:
        return response("Playlist ยังไม่มีเพลง", False), 400
    return response(f"กำลังเล่น: {title}")


@app.post("/api/next")
def next_song():
    title = playlist.next_song()
    if title is None:
        return response("Playlist ยังไม่มีเพลง", False), 400
    return response(f"เพลงถัดไป: {title}")


@app.post("/api/previous")
def previous_song():
    title = playlist.previous_song()
    if title is None:
        return response("Playlist ยังไม่มีเพลง", False), 400
    return response(f"เพลงก่อนหน้า: {title}")


@app.post("/api/remove")
def remove_song():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return response("กรุณาใส่ชื่อเพลงที่ต้องการลบ", False), 400
    if not playlist.remove_song(title):
        return response(f"ไม่พบเพลง {title}", False), 404
    return response(f"ลบเพลง {title} แล้ว")


@app.post("/api/remove-current")
def remove_current_song():
    if not playlist.remove_current_song():
        return response("Playlist ยังไม่มีเพลง", False), 400
    return response("ลบเพลงปัจจุบันแล้ว")


@app.post("/api/history-back")
def history_back():
    title = playlist.history_back()
    if title is None:
        return response("History ยังว่างอยู่", False), 400
    return response(f"ย้อนกลับไปเพลง: {title}")


@app.post("/api/clear")
def clear_playlist():
    playlist.__init__()
    return response("ล้าง Playlist แล้ว")


if __name__ == "__main__":
    app.run(debug=True)
