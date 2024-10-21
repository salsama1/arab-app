import React from 'react';
import './App.css';

function App() {
  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { exact: 'environment' } }  // Request the back camera
      });
      const videoElement = document.getElementById('video');
      videoElement.srcObject = stream;
    } catch (error) {
      console.error('Error accessing back camera:', error);
    }
  };

  return (
    <div className="App flex flex-col items-center justify-center h-screen bg-gray-100">
      <header className="App-header text-center">
        <h1 className="text-2xl font-bold mb-4">Back Camera App</h1>
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          onClick={openCamera}
        >
          Open Back Camera
        </button>
        <div className="mt-4">
          <video id="video" width="400" height="300" autoPlay className="border-2 border-gray-300"></video>
        </div>
      </header>
    </div>
  );
}

export default App;
