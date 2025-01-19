import React, { useState } from 'react';
import { Camera, Search, Image as ImageIcon, Send, AlertCircle, Upload, X } from 'lucide-react';
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
    const [uploadedImage, setUploadedImage] = useState(null);
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
                const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_API_KEY);
                // console.log(import.meta.env.REACT_APP_API_KEY)
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
        <div className="min-h-screen bg-gray-50 p-8 text-black">
            <div className="max-w-6xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
                        <Camera className="w-8 h-8 text-blue-600" />
                        ByteLocker - Vision Language Model
                    </h1>
                    <p className="text-gray-600 mt-2">
                        Advanced visual analysis powered by AI for enhanced security and monitoring
                    </p>
                </header>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="md:col-span-2 bg-white rounded-lg shadow-md p-6">
                        <div className="mb-6">
                            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                <Upload className="w-5 h-5 text-blue-600" />
                                Upload Image
                            </h2>
                            <div className="flex items-center gap-4">
                                <label className="flex-1">
                                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center cursor-pointer hover:border-blue-500 transition-colors">
                                        <input
                                            type="file"
                                            accept="image/*"
                                            onChange={handleImageUpload}
                                            className="hidden"
                                        />
                                        <p className="text-gray-600">Click to upload or drag and drop</p>
                                    </div>
                                </label>
                                {uploadedImage && (
                                    <button
                                        onClick={clearUploadedImage}
                                        className="p-2 text-red-500 hover:bg-red-50 rounded-full"
                                    >
                                        <X className="w-5 h-5" />
                                    </button>
                                )}
                            </div>
                            {uploadedImage && (
                                <div className="mt-4">
                                    <img
                                        src={uploadedImage}
                                        alt="Uploaded preview"
                                        className="max-h-64 rounded-lg mx-auto"
                                    />
                                </div>
                            )}
                        </div>

                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <ImageIcon className="w-5 h-5 text-blue-600" />
                            Or Select Sample Image
                        </h2>
                        <div className="grid grid-cols-2 gap-4">
                            {sampleImages.map((image) => (
                                <div
                                    key={image.id}
                                    className={`relative rounded-lg overflow-hidden cursor-pointer border-2 transition-all ${selectedImage?.id === image.id ? 'border-blue-500 shadow-lg' : 'border-gray-200'
                                        }`}
                                    onClick={() => handleImageSelect(image)}
                                >
                                    <img
                                        src={image.src}
                                        alt={image.alt}
                                        className="w-full h-40 object-cover"
                                    />
                                    <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white p-2 text-sm">
                                        {image.type}
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="mt-6">
                            <div className="flex gap-2 mb-2 items-center">
                                <Search className="w-5 h-5 text-gray-500" />
                                <label className="font-medium text-gray-700">
                                    Analysis Prompt
                                </label>
                            </div>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={prompt}
                                    onChange={(e) => setPrompt(e.target.value)}
                                    placeholder="Enter your analysis prompt or just click analyze..."
                                    className=" text-black flex-1 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                />
                                <button
                                    onClick={handleSubmit}
                                    disabled={(!selectedImage && !uploadedImage) || loading}
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg flex items-center gap-2 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                                >
                                    {loading ? "Analyzing..." : "Analyze"}
                                    <Send className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <AlertCircle className="w-5 h-5 text-blue-600" />
                            Analysis Results
                        </h2>
                        {response ? (
                            <div className="prose">
                                <p className="text-gray-700">{response}</p>
                            </div>
                        ) : (
                            <div className="text-center text-gray-500 py-8">
                                Select an image and enter a prompt to see analysis results
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default VLMInterface;