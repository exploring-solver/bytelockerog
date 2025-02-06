"use client"
import React, { useState } from 'react';
import { Upload } from 'lucide-react';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { Buffer } from 'buffer';

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

const sampleResponses = {
    1: "Analysis shows a standard burger meal setup. Food safety protocols appear to be followed with proper preparation surfaces. Temperature indicators suggest food is being held at safe temperatures.",
    2: "Detected 72 vehicles in the parking area. No unauthorized vehicles or suspicious activity identified. Parking space utilization is currently at 100%.",
    3: "Current crowd density: High. Approximately 34 people detected near entrance. Movement patterns indicate normal flow. No congestion points identified.",
    4: "9 workers detected, all wearing casual. No safety violations detected. Work zone boundaries are properly maintained."
};

const VLMInterface = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [uploadedImage, setUploadedImage] = useState(null );
    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const handleImageSelect = (image) => {
        setSelectedImage(image);
        setUploadedImage(null);
        setResponse("");
    };

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setUploadedImage(reader.result);
                setSelectedImage(null);
                setResponse("");
            };
            reader.readAsDataURL(file);
        }
    };

    const clearUploadedImage = () => {
        setUploadedImage(null);
        setResponse("");
    };

    const handleSubmit = async () => {
        setLoading(true);
        if (uploadedImage) {
            try {
                const genAI = new GoogleGenerativeAI(process.env.NEXT_PUBLIC_GEMINI_API_KEY || "");
                const base64Response = await fetch(uploadedImage);
                const arrayBuffer = await base64Response.arrayBuffer();
                const model = genAI.getGenerativeModel({ model: 'models/gemini-1.5-pro' });
                const result = await model.generateContent([
                    {
                        inlineData: {
                            data: Buffer.from(arrayBuffer).toString('base64'),
                            mimeType: 'image/jpeg',
                        },
                    },
                    prompt || 'Analyze this image for security concerns and respond as a security llm and no extra text just to the point info and extract the text and info fetched in the image.',
                ]);
                setResponse(result.response.text);
            } catch (error) {
                console.error('Error analyzing image:', error);
                setResponse('Error analyzing image. Please try again.');
            }
        } else if (selectedImage) {
            // Use sample responses for demo images
            setTimeout(() => {
                setResponse(sampleResponses[selectedImage.id]);
            }, 1000);
        }
        setLoading(false);
    };

    return (
        <div className="p-16 bg-gradient-to-b from-black to-gray-900 text-white">
            <p className="mb-8 text-center">Advanced visual analysis powered by AI for enhanced security and monitoring</p>

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
                {response ? (
                    <p className="bg-gray-800 p-4 rounded-lg">{response}</p>
                ) : (
                    <p>Select an image and enter a prompt to see analysis results</p>
                )}
            </div>
        </div>
    );
};

export default VLMInterface;