/**
 * Run Sentiment Analysis on User Input
 *
 * This function is called when the user submits text for sentiment analysis. It retrieves
 * the user's input text, sends it to the server for analysis, and displays the server's
 * response on the web page.
 */
let RunSentimentAnalysis = () => {
    // Get the text to analyze from the user input field
    textToAnalyze = document.getElementById("textToAnalyze").value;

    // Create an XMLHttpRequest to communicate with the server
    let xhttp = new XMLHttpRequest();

    // Define the callback function to handle the server's response
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Update the HTML element with the server's response
            document.getElementById("system_response").innerHTML = xhttp.responseText;
        }
    };

    // Prepare and send a GET request to the server with the user's input
    xhttp.open("GET", "emotionDetector?textToAnalyze" + "=" + textToAnalyze, true);
    xhttp.send();
}
