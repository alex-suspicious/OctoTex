function updatePlugins() {


	$.get( "/callback/plugins_list", function( data ) {
		var list = data.split(",");
		

		var first = true;

		$("#nav-tabContent-plugins").html("");
		$("#nav-tab-plugins").html("");

		function loadPluginContent(temp, htmlContent) {
			$.get("/plugin/" + temp, function(resp) {
				var updatedHtmlContent = htmlContent.replaceAll("@content", resp);
				$("#nav-tabContent-plugins").append(updatedHtmlContent);
			});
		}

		for (var i = 0; i < list.length; i++) {
			var temp = list[i].split(".")[0];
			

			var html = `<button class="nav-link nav-link-plugin" id="@name-tab" data-bs-toggle="tab" data-bs-target="#nav-@name" type="button" role="tab" aria-controls="nav-@name" aria-selected="true">@cleanname</button>`;
			var htmlContent = `<div class="tab-render-html tab-pane fade" id="nav-@name" role="tabpanel" aria-labelledby="@name-tab">@content</div>`;
			
			if( first ){
				html = html.replaceAll("nav-link nav-link-plugin","nav-link nav-link-plugin active"); 
				htmlContent = htmlContent.replaceAll("tab-pane fade","tab-pane fade show active");
			}

			first = false;
			var cleanName = temp.replace("_"," ");
			cleanName = cleanName.split(" ");

			for (let i = 0; i < cleanName.length; i++) {
			    cleanName[i] = cleanName[i][0].toUpperCase() + cleanName[i].substr(1);
			}
			cleanName = cleanName.join(" ");


			html = html.replaceAll("@cleanname",cleanName); 
			html = html.replaceAll("@name",temp); 
			htmlContent = htmlContent.replaceAll("@name",temp);

			loadPluginContent(temp, htmlContent);


		  	$("#nav-tab-plugins").append(html);
		}
	});
	

}


$(document).ready( function () {
	updatePlugins();
});