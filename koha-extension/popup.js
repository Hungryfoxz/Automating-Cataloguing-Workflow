document.getElementById("fillBtn").onclick = async () => {

  document.getElementById("status").innerText = "Fetching...";

  try {
    const res = await fetch("http://localhost:8000/latest");
    const data = await res.json();

    console.log("Fetched data:", data);

    // Send to content script
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, data);
    });

    document.getElementById("status").innerText = "Done!";
  } catch (err) {
    console.error(err);
    document.getElementById("status").innerText = "Error!";
  }
};