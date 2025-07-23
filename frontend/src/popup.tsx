import React, { useEffect, useState } from "react";

function Popup() {
    const [url, setUrl] = useState("");
    const [result, setResult] = useState("");

    useEffect(() => {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            const activeUrl = tabs[0].url || "";
            setUrl(activeUrl);

            fetch("https://phisx.abhiramverse.tech/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: activeUrl })  // Or preprocessed features
            })
                .then(res => res.json())
                .then(data => setResult(data.result));
        });
    }, []);

    return (
        <div className="p-4 text-center">
            <h1 className="text-lg font-bold">PhisX</h1>
            <p className="text-sm mt-2">URL: {url}</p>
            <p className={`mt-2 font-semibold ${result === "phishing" ? "text-red-600" : "text-green-600"}`}>
                {result.toUpperCase()}
            </p>
        </div>
    );
}

export default Popup;
