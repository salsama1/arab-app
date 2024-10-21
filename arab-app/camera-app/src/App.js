import React, { useRef } from 'react';
import axios from 'axios';  // Import Axios
import './App.css';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { exact: 'environment' } }  // Back camera
      });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error('Error accessing back camera:', error);
    }
  };

  const captureAndSendImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    // Draw the video frame onto the canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas data to a blob (image format)
    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append('image', blob, 'photo.jpg');  // Send as a file

      // Use Axios to send the image to the backend
      try {
        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        // Handle the response
        console.log('OCR Result:', response.data);
      } catch (error) {
        console.error('Error uploading image:', error);
      }
    }, 'image/jpeg');
  };

  return (
    <div className="App flex flex-col items-center justify-center h-screen bg-gray-100">
      <header className="App-header text-center">
        <h1 className="text-2xl font-bold mb-4">Capture Arabic Numbers</h1>
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          onClick={openCamera}
        >
          Open Back Camera
        </button>
        <div className="mt-4">
          <video ref={videoRef} width="400" height="300" autoPlay className="border-2 border-gray-300"></video>
          <canvas ref={canvasRef} className="hidden"></canvas>
        </div>
        <button
          className="bg-green-500 text-white px-4 py-2 rounded-lg mt-4 hover:bg-green-700 transition"
          onClick={captureAndSendImage}
        >
          Capture and Send Image
        </button>
      </header>
    </div>
  );
}

export default App;
