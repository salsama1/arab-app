import React, { useRef, useState } from 'react';
import axios from 'axios';

const CameraCapture = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [isCameraOn, setIsCameraOn] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState('');

    // Start the back camera
    const startCamera = () => {
        // Request video stream with back camera as the preferred device
        navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: { exact: 'environment' }, // 'environment' targets the back camera
            },
        })
        .then((stream) => {
            videoRef.current.srcObject = stream;
            setIsCameraOn(true);
        })
        .catch((err) => {
            console.error('Error accessing back camera:', err);
            alert('Failed to access the back camera. Please try again.');
        });
    };

    // Capture image from the video stream
    const captureImage = () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        
        // Set canvas size to video size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw video frame to canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convert canvas to blob
        canvas.toBlob((blob) => {
            if (blob) {
                sendImage(blob);
            }
        }, 'image/jpeg');
    };

    // Send the captured image to the back end
    const sendImage = async (imageBlob) => {
        const formData = new FormData();
        formData.append('image', imageBlob, 'captured_image.jpg');

        setIsLoading(true);
        try {
            const res = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResponse(res.data.message);
        } catch (error) {
            console.error('Error uploading image:', error);
            setResponse('Error uploading image');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
            <h1 className="text-3xl font-bold mb-4">Capture Image from Back Camera</h1>
            
            {!isCameraOn && (
                <button 
                    onClick={startCamera} 
                    className="bg-green-500 text-white px-4 py-2 rounded mb-4"
                >
                    Start Back Camera
                </button>
            )}

            <video ref={videoRef} autoPlay className="mb-4 border rounded" hidden={!isCameraOn}></video>
            <canvas ref={canvasRef} className="hidden"></canvas>

            {isCameraOn && (
                <button 
                    onClick={captureImage} 
                    className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
                    disabled={isLoading}
                >
                    {isLoading ? 'Processing...' : 'Capture & Submit'}
                </button>
            )}

            {response && (
                <div className="mt-4 text-green-500">{response}</div>
            )}
        </div>
    );
};

export default CameraCapture;
