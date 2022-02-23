function addTable() {
      
    var myTableDiv = document.getElementById("results");

    //Create an input type dynamically.
    myTableDiv.innerHTML = '';
	var element = document.createElement("TEXTAREA");
    element.rows="20" 
    element.cols="100"
    element.readOnly = true;

	myTableDiv.appendChild(element);
}