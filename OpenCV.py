from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import cv2
import time
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

camera = cv2.VideoCapture(0)

bandwidth_usage = 0

def gen_frames():
    global bandwidth_usage
    fps = 10
    prev = 0
    
    while True:
        time_elapsed = time.time() - prev
        if time_elapsed > 1./fps:
            prev = time.time()
            
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                frame = buffer.tobytes()
                
                bandwidth_usage = len(frame) * fps
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Video Stream</title>
            <style>
                body, html {
                    height: 100%;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #000;
                }
                img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
            </style>
        </head>
        <body>
            <img src="/video_feed" alt="Video Stream">
        </body>
    </html>
    """

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/bandwidth_usage")
async def bandwidth_usage_stream():
    async def event_generator():
        while True:
            await asyncio.sleep(1)
            yield f"data: {bandwidth_usage / 1024:.2f} KB/s\n\n"
                            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
