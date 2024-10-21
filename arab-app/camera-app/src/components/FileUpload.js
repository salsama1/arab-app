import React, { useState } from 'react';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('image', selectedFile);

      try {
        const response = await fetch('http://localhost:5000/api/upload', {
          method: 'POST',
          body: formData,
        });

        const data = await response.json();
        console.log('Recognized number:', data.number);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-4"
      />
      {selectedFile && (
        <button
          onClick={handleUpload}
          className="bg-green-500 text-white px-4 py-2 rounded-lg"
        >
          Upload & Recognize
        </button>
      )}
    </div>
  );
};

export default FileUpload;
