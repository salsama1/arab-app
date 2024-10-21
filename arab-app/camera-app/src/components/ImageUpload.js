import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
    const [image, setImage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState('');

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!image) {
            alert('Please select an image');
            return;
        }

        // Check image type
        if (!image.type.startsWith('image/')) {
            alert('Please upload a valid image file');
            return;
        }

        const formData = new FormData();
        formData.append('image', image);

        setIsLoading(true);
        try {
            const res = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResponse(res.data.message);
        } catch (error) {
            console.error('Error uploading image:', error.response || error.message);
            setResponse('Error uploading image');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
            <h1 className="text-3xl font-bold mb-4">Upload Image for OCR</h1>
            <input 
                type="file" 
                accept="image/*" 
                onChange={handleImageChange} 
                className="mb-4 p-2 border rounded"
            />
            <button
                onClick={handleSubmit}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
                disabled={isLoading}
            >
                {isLoading ? 'Uploading...' : 'Submit'}
            </button>
            {response && (
                <div className="mt-4 text-green-500">{response}</div>
            )}
        </div>
    );
};

export default ImageUpload;
