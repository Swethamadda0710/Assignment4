const input = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const predictBtn = document.getElementById("predictBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");

// Image Preview
input.addEventListener("change", function () {
    const file = input.files[0];

    if (file) {
        preview.src = URL.createObjectURL(file);
        result.innerHTML = "✅ Image Selected";
    }
});

// Predict Image
predictBtn.addEventListener("click", async function () {

    if (input.files.length === 0) {
        alert("Please upload an image.");
        return;
    }

    loading.style.display = "block";
    result.innerHTML = "";

    const formData = new FormData();
    formData.append("image", input.files[0]);

    try {

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Prediction failed!");
        }

        const data = await response.json();

        loading.style.display = "none";

        // Convert first letter to uppercase
        const label =
            data.class.charAt(0).toUpperCase() + data.class.slice(1);

        result.innerHTML = `
            <h3>Prediction : <span style="color:#4F46E5;">${label}</span></h3>
            <p><strong>Confidence :</strong> ${data.confidence}%</p>
        `;

    } catch (error) {

        loading.style.display = "none";

        result.innerHTML = `
            <p style="color:red;">
                ❌ ${error.message}
            </p>
        `;
    }

});