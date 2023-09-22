function updateTabs() {

	$.get( "/callback/tabs_list", function( data ) {
		var list = data.split(",");
		

		var first = true;

		$("#nav-tabContent").html("");
		$("#nav-tab").html("");

		function loadTabContent(temp, htmlContent) {
			$.get("/tabs/" + temp + ".html", function(resp) {
				var updatedHtmlContent = htmlContent.replaceAll("@content", resp);
				$("#nav-tabContent").append(updatedHtmlContent);
			});
		}

		for (var i = 0; i < list.length; i++) {
			var temp = list[i].split(".")[0];
			

			var html = `<button class="nav-link" id="@name-tab" data-bs-toggle="tab" data-bs-target="#nav-@name" type="button" role="tab" aria-controls="nav-@name" aria-selected="true">@name</button>`;
			var htmlContent = `<div class="tab-render-html tab-pane fade" id="nav-@name" role="tabpanel" aria-labelledby="@name-tab">@content</div>`;
			
			if( first ){
				html = html.replaceAll("nav-link","nav-link active"); 
				htmlContent = htmlContent.replaceAll("tab-pane fade","tab-pane fade show active");
			}

			first = false;
			var cleanName = temp;
			if( cleanName.includes("-") )
				cleanName = cleanName.split("-")[1];

			html = html.replaceAll("@name",cleanName); 
			htmlContent = htmlContent.replaceAll("@name",cleanName);

			loadTabContent(temp, htmlContent);


		  	$("#nav-tab").append(html);
		}
	});
	

}


$(document).ready( function () {
	updateTabs();
});