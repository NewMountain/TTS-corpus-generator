let currentRow = {{ starting_row }};
let mediaRecorder;
let audioChunks = [];

document
  .getElementById("recordButton")
  .addEventListener("click", startRecording);

document.getElementById("stopButton").addEventListener("click", stopRecording);

document
  .getElementById("acceptButton")
  .addEventListener("click", acceptRecording);

document
  .getElementById("rejectButton")
  .addEventListener("click", rejectRecording);

function fetchSentence(row) {
  document.getElementById("progressDisplay").innerText = `Sentence Number: ${
    row 
  } of 1150`;

  fetch(`/get_sentence/${row}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("sentenceArea").innerText = data.sentence;
    });
}

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", (event) => {
      audioChunks.push(event.data);
    });

    document.getElementById("recordButton").disabled = true;
    document.getElementById("stopButton").disabled = false;
  });
}

function stopRecording() {
  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach((track) => track.stop());

  mediaRecorder.onstop = () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = document.getElementById("audioPlayback");
    audio.src = audioUrl;
    audio.hidden = false;

    document.getElementById("stopButton").disabled = true;
    document.getElementById("acceptButton").disabled = false;
    document.getElementById("rejectButton").disabled = false;
  };
}

function acceptRecording() {
  const audioBlob = new Blob(audioChunks);
  const formData = new FormData();
  formData.append("audio", audioBlob);
  formData.append(
    "sentence",
    document.getElementById("sentenceArea").innerText
  );

  fetch(`/save_recording/${currentRow}`, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        currentRow++;
        fetchSentence(currentRow);
        document.getElementById("audioPlayback").hidden = true;
        document.getElementById("recordButton").disabled = false;
        document.getElementById("acceptButton").disabled = true;
      }
    });
}

function rejectRecording() {
  // Reset the audio player
  const audio = document.getElementById("audioPlayback");
  audio.src = "";
  audio.hidden = true;

  // Enable the record button for a new attempt
  document.getElementById("recordButton").disabled = false;

  // Disable the accept and reject buttons until a new recording is made
  document.getElementById("acceptButton").disabled = true;
  document.getElementById("rejectButton").disabled = true;

  // Optionally, clear the previous audio chunks if you want to start fresh
  audioChunks = [];
}

// Start the process
fetchSentence(currentRow);
