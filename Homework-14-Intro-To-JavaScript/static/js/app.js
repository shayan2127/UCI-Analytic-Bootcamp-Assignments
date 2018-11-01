// Set tableData to address Data initially
var tableData = data;

// Select the submit button
var submit = d3.select("#filter-btn")

// Get a reference to the table body
var tbody = d3.select("tbody");

submit.on("click", function() {

    // Prevent the page from refreshing
    d3.event.preventDefault();

    // Select the input element and get the raw HTML node
    var inputDate = d3.select("#datetime");

    // Get the value property of the input element
    var inputValue = inputDate.property("value");
    var filteredData = tableData.filter(function(sight) { 
  	
	  	if (sight.datetime === inputValue){

		  	console.log(filteredData);
			var row = tbody.append("tr");

			Object.entries(sight).forEach(function([key, value]) {
		    
		    var cell = tbody.append("td");

			cell.text(value);
		  	});
		};
	});

});


