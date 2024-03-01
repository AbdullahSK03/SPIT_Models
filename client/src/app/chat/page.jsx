"use client";

import { useState } from 'react';
import Image from 'next/image';


export default function Home() {
  const [input, setInput] = useState('');
  const [image, setImage] = useState(null);
  const [response, setResponse] = useState('');

  const handleImageUpload = (event) => {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      if (file instanceof Blob) {
        setImage(URL.createObjectURL(file));
      } else {
        console.error('Uploaded file is not a Blob or File object');
      }
    } else {
      console.error('No file was uploaded');
    }
  };
  
  const handleSubmit = async (event) => {
    // event.preventDefault();

    const response = await fetch('http://localhost:8080/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        input,
        image
      })
    });
    const responseData = await response.json();
    setResponse(responseData.output);

    // Here you would call the Google Gemini Pro Vision API with your input and image
    // For now, we'll just set the response to be the input
    setResponse(input);
  };

  return (
    <div>
      <h1>Nutritionist AI 👩🏻‍⚕</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Input Prompt:
          <input type="text" value={input} onChange={(e) => setInput(e.target.value)} />
        </label>
        <label>
          Choose an image:
          <input type="file" accept="image/*" onChange={handleImageUpload} />
        </label>
        {image && <Image src={image} width={200} height={200} alt="Uploaded" />}
        <button type="submit" onSubmit={handleSubmit}>Calculate</button>
      </form>
      {response && <div>{response}</div>}
    </div>
  );
}
