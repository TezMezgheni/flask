const url_input = document.getElementById("url_input");
const summarize_button = document.getElementById("my_button");
const choice_dropdown = document.getElementById('choice-dropdown')
summarize_button.addEventListener("click", initializeSummary);
const youtube_div = document.getElementById("youtube");
const text_out_main_div = document.getElementById("text_out_main");
const re_summarize_element = document.getElementById('re_summarize');

function initializeSummary() {
    // Checking Dropdown and TextBox Validity Again Here
    if (/*percent_dropdown.selectedIndex > 0 || */choice_dropdown.selectedIndex > 0 || url_input.value.length > 0) {

        const text_out_content_element = document.getElementById("text-out");
        const process_element = document.getElementById("current_process");

        // Getting values of both dropdowns
        const choice=choice_dropdown.value

        // Storing URL of the URL present in the text box
        const video_link = url_input.value;
        if (video_link) {
            // Making Selection Div invisible, and text output as visible.
            youtube_div.style.display = "none";
            text_out_main_div.style.display = "block";

            // https://ytsum.herokuapp.com
            // http://127.0.0.1:5000
            // Fetch request to our server. (GET request with arguments received from popup.html
            fetch("http://127.0.0.1:5000/summary/?link=" + video_link
            +"&algorithm="+choice)
                // "&percent=" + percent + "&choice=" + choice)
                .then(response => response.json()).then(result => {
                // Result now contains the response in JSON
                // Sending result back to popup.html
                process_element.innerHTML = result.message;
                if (result.success) {
                    // If result was successfully received. Then, parse the result_response JSON
                    const response_json = (result.response);

                    // Use the values present in JSON for displaying summary.
                    text_out_content_element.innerHTML = "<b>Processed Summary:</b> " + response_json.processed_summary
                        // + "<p>In your video, there are <b>" + response_json.length_original + "</b> characters in <b>" + response_json.sentence_original + "</b> sentences."
                        // + "<br>The processed summary has <b>" + response_json.length_summary + "</b> characters in <b>" + response_json.sentence_summary + "</b> sentences."
                        // + "</br><br>";

                    // Text Beautification: Aligning Text to be justified
                    text_out_content_element.style.textAlign = "justify";
                    text_out_content_element.style.textJustify = "inter-word";
                    // Enabling re-summarize element
                    re_summarize_element.style.display = "block";
                } else {
                    // We failed: Reason is already pushed to UI in process_element (response.result_message has reason)
                    text_out_content_element.innerHTML = "We failed due to above reason.";
                    text_out_content_element.style.textAlign = "center";
                    // Enabling re-summarize element
                    re_summarize_element.style.display = "block";
                }
            }).catch(error => {
                // Network issue occurred during fetch probably. Logging and sending result backs.
                console.log(error);
                process_element.innerHTML = "A network issue was encountered. Please retry.";
                // We failed to fetch: Reason is already pushed to UI in process_element (response.result_message has reason)
                text_out_content_element.innerHTML = "We failed due to above reason.";
                text_out_content_element.style.textAlign = "center";
                // Enabling re-summarize element
                re_summarize_element.style.display = "block";
            })
        } else {
            // Alerting user that they entered wrong URL
            alert("Your YouTube video URL is invalid. Please retry.");
            url_input.value = "";
        }
    }
}