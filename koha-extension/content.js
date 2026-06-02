chrome.runtime.onMessage.addListener((data) => {
  console.log("Received from extension:", data);

  const title = data.title;

  if (!title) {
    alert("No title received from API");
    return;
  }

  // 🔍 Find Koha title field (245$a)
  let titleField = document.querySelector(
    'input[id*="245"][id*="subfield_a"]'
  );

  if (titleField) {
    titleField.value = title;
    titleField.focus();
    alert("Title autofilled!");
  } else {
    alert("Title field not found. Check selector.");
  }
});