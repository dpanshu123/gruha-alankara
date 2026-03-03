document.addEventListener("DOMContentLoaded", function () {
    console.log("Gruha Alankara Loaded Successfully ");
});

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = document.getElementById("camera");
        video.srcObject = stream;
    } catch (error) {
        console.error("Camera access denied.", error);
        alert("Camera access denied!");
    }
}
