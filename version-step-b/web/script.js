function validateFileExtension() {
  let fileInput = document.getElementById("fileToUpload");
  let file = fileInput.files[0];

  // Check if file is selected
  if (!file) {
    alert("Please select a file to upload.");
    return false; // Indicate failure to validate
  }

  let allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
  if (!allowedExtensions.exec(file.name)) {
    alert("Invalid file type. Only JPG, JPEG, PNG, and GIF files are allowed.");
    return false; // Indicate failure to validate
  } else if (file.size > 2 * 1024 * 1024) {
    // 2MB limit
    alert("File size exceeds 2MB.");
    return false; // Indicate failure to validate
  }

  return file;
}

async function encryptAndUploadFile() {
  console.log("Encrypting and uploading file...");

  let file = validateFileExtension();
  if (!file) return;

  try {
    // curl -X 'GET' 'http://localhost:8000/hello'   -H 'accept: application/json'
    response = await fetch("http://localhost:8000/hello", {
      method: "GET",
      headers: { accept: "application/json" },
    });

    let pem = response["data"];
    const encryptedData = await encryptWithpublicKey(response["data"], file);
    const formData = new FormData();
    formData.append("file", new Blob([encryptedData]), file.name);
    formData.append(
      "csrfToken",
      document.querySelector("meta[name='csrf-token']").content
    );

    // Send encrypted file to server
    fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
      credentials: "same-origin",
    })
      .then((response) => {
        if (response.ok) {
          alert("File uploaded successfully.");
        } else {
          alert("Failed to upload file.");
        }
      })
      .catch((error) => {
        alert("Failed to upload file.");
      });
  } catch (error) {
    console.error("Error:", error);
    alert("Error preparing file upload.");
  }
}

async function encryptWithpublicKey(publicKeyPem, data) {
  // Import public key
  let publicKey = await window.crypto.subtle.importKey(
    "spki",
    convertPemToBinary(publicKeyPem),
    {
      name: "RSA-OAEP",
      hash: "SHA-256",
    },
    true,
    ["encrypt"]
  );

  log("Public key imported.", publicKey);

  // Encrypt file with public key
  let encryptedFile = await window.crypto.subtle.encrypt(
    {
      name: "RSA-OAEP",
    },
    publicKey,
    new TextEncoder().encode(data)
  );

  return encryptedFile;
}

async function convertPemToBinary(pem) {
  let b64Lines = pem
    .replace("-----BEGIN PUBLIC KEY-----", "")
    .replace("-----END PUBLIC KEY-----", "")
    .replace(/\s+/g, "");
  let binaryString = window.atob(b64Lines);
  let binary = new Uint8Array(binaryString.length);

  binary.forEach((_, i) => {
    binary[i] = binaryString.charCodeAt(i);
  });

  return binary.buffer;
}
