"use client";

import React, { useEffect } from "react";
import Link from "next/link";

const page = () => {
const [message, setMessage] = React.useState("Loading");


  useEffect(() => {
    fetch("http://localhost:8080")
      .then((response) => response.json())
      .then((data) =>{
        setMessage(data.message);
      })
  },[]);

  const pageLink = [
    {
      name: "Report",
      link: "/report",
    },
    {
      name: "Instadoc",
      link: "/instadoc",
    },
    {
      name: "Nutritionist",
      link: "/chat",
    },
  ];
  return (
    <>
      <h1 className="text-3xl font-bold text-center m-4">{message}</h1>
      <div className="m-4 flex cards">
        {pageLink.map((link) => (
          <div
            key={link.name}
            className="text-lg font-bold text-center bg-blue-500 m-2 rounded-md w-1/3 p-4"
          >
            <Link href={link.link}>{link.name}</Link>
          </div>
        ))}
      </div>
    </>
  );
};

export default page;
