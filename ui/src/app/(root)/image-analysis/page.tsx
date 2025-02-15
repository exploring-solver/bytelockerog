/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import React, { useState } from 'react';
import { Upload } from 'lucide-react';

const sampleImages = [
  {
    id: 1,
    src: "/vlm/burger.webp",
    alt: "Burger and fries",
    type: "Food safety"
  },
  {
    id: 2,
    src: "/vlm/cars.png",
    alt: "Parking lot",
    type: "Vehicle monitoring"
  },
  {
    id: 3,
    src: "/vlm/store_crowd.jpeg",
    alt: "Store entrance",
    type: "Crowd analysis"
  },
  {
    id: 4,
    src: "/vlm/work_people.jpg",
    alt: "Work area",
    type: "Safety compliance"
  }
];

const VLMInterface = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageSelect = (image: React.SetStateAction<null>) => {
    setSelectedImage(image);
    setUploadedImage(null);
    setAnalysis("");
  };

  const handleImageUpload = async (event: { target: { files: any[]; }; }) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target?.result);
        setSelectedImage(null);
        setAnalysis("");
      };
      reader.readAsDataURL(file);
    }
  };

  const clearUploadedImage = () => {
    setUploadedImage(null);
    setAnalysis("");
  };

  const handleSubmit = async () => {
    setLoading(true);
    setAnalysis("");

    try {
      let imageFile = null;

      if (uploadedImage) {
        // Convert data URL to blob
        const blob = await fetch(uploadedImage).then((res) => res.blob());
        imageFile = new File([blob], "upload.jpg", { type: "image/jpeg" });
      } else if (selectedImage) {
        // Fetch the sample image as a blob
        const imageResponse = await fetch(selectedImage.src);
        const blob = await imageResponse.blob();
        imageFile = new File([blob], "sample.jpg", { type: "image/jpeg" });
      } else {
        throw new Error("Please select or upload an image");
      }

      const formData = new FormData();
      formData.append("image", imageFile);
      formData.append("question", prompt || "Analyze this image for security concerns");

      const res = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Analysis failed");
      }

      const data = await res.json();
      setAnalysis(typeof data.analysis === 'object' ? 
        JSON.stringify(data.analysis, null, 2) : 
        data.analysis || "No analysis available"
      );

    } catch (error) {
      console.error(error);
      setAnalysis(error instanceof Error ? error.message : "Error analyzing image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-16 bg-gradient-to-b from-black to-gray-900 text-white">
      <p className="mb-8 text-center">
        Advanced visual analysis powered by AI for enhanced security and monitoring
      </p>

      {/* Image Upload Section */}
      <div className="mb-8">
        <label className="block text-lg font-semibold mb-2">Upload Image</label>
        <div className="border-dashed border-2 border-gray-600 p-4 rounded-lg cursor-pointer">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
            id="upload-input"
          />
          <label htmlFor="upload-input" className="cursor-pointer flex items-center justify-center">
            <Upload className="mr-2" /> Click to upload or drag and drop
          </label>
        </div>
        {uploadedImage && (
          <div className="mt-4">
            <img src={uploadedImage} alt="Uploaded" className="max-w-full h-auto" />
            <button onClick={clearUploadedImage} className="mt-2 text-red-400">
              Remove Image
            </button>
          </div>
        )}
      </div>

      {/* Sample Images Section */}
      <div className="mb-8">
        <label className="block text-lg font-semibold mb-2">Or Select Sample Image</label>
        <div className="flex gap-4">
          {sampleImages.map((image) => (
            <div
              key={image.id}
              onClick={() => handleImageSelect(image)}
              className="cursor-pointer border p-2 rounded-lg hover:bg-gray-800"
            >
              <img src={image.src} alt={image.alt} className="w-24 h-24 object-cover" />
              <p className="text-center mt-2">{image.type}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Analysis Prompt Section */}
      <div className="mb-8">
        <label className="block text-lg font-semibold mb-2">Analysis Prompt</label>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your analysis prompt or just click analyze..."
          className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-gray-800 text-white"
        />
      </div>

      {/* Analyze Button */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {/* Analysis Results */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-2">Analysis Results</h2>
        {analysis ? (
          <pre className="bg-gray-800 p-4 rounded-lg whitespace-pre-wrap">
            {analysis}
          </pre>
        ) : (
          <p>Select an image and enter a prompt to see analysis results</p>
        )}
      </div>
    </div>
  );
};

export default VLMInterface;
