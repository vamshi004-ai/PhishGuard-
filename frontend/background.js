chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url) {
        fetch("https://phisx.abhiramverse.tech/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: tab.url })  // Or features if extracted
        })
            .then(res => res.json())
            .then(data => {
                if (data.result === "phishing") {
                    chrome.notifications.create({
                        type: "basic",
                        iconUrl: "icon.png",
                        title: "Phishing Alert",
                        message: "This site may be malicious. Proceed with caution."
                    });
                }
            });
    }
});
