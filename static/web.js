const choice_dropdown = document.getElementById("choice_dropdown");
const text_out = document.getElementById("text-out");
const url_input = document.getElementById("url_input");
const text_out_main= document.getElementById("text_out_main");
const current_process = document.getElementById("current_process");
function summarize() {
	const choice = choice_dropdown.options[choice_dropdown.selectedIndex].text;
	const link =url_input.value;
	console.log(link);
	if(link) {
    fetch("http://localhost:5000/summary/?link="+link+"&algorithm="+choice)
	.then(response => response.json())
	.then(data => { text_out.innerHTML=data.result;
					if(text_out.innerHTML) {
						current_process.innerText="Summary successful";
						text_out_main.style.display = "block";
					}
					})
	.catch(err => console.error(err));
	}
	
}

