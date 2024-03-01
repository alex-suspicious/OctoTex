
let particleLight;
let particleLight2;
let particleLight3;
let group;
let mesh;
let newMaterial;
let rotate = true;
let yaw_angle = 0;
let yaw_angle_lerp = 0;




function lerp (start, end, amt){
  return (1-amt)*start+amt*end
}
const clamp = (num, min, max) => Math.min(Math.max(num, min), max);

function updateThreeMaterial() {
}

function loadMaterial( name ) {

	
	$.get( "/callback/get_material?texture=" + name, function( data ) {
		var splitted = data.split("\n");
		$("#material_type").val(splitted[0].replace("@",""));
		$("#depthRange").val( parseFloat(splitted[1].split("=")[1].replace(" ",""))*1000 );
		$("#roughnessRange").val( parseFloat(splitted[3].split("=")[1].replace(" ",""))*1000 );
		$("#transparencyRange").val( parseFloat(splitted[2].split("=")[1].replace(" ",""))*1000 );
		$("#ior_constant").val( parseFloat(splitted[4].split("=")[1].replace(" ",""))*1000 );
		$("#metallic_constant").val( parseFloat(splitted[5].split("=")[1].replace(" ",""))*1000 );

		updateThreeMaterial();
		setTimeout(function() {
			updateThreeMaterial();
		},500);

		console.log(splitted)
	});

}



function makeTextureSelected(name) {
	$(".selected-texture").removeClass("selected-texture");
	$("button[name=\""+name+"\"]").addClass("selected-texture");

	$(document).find(".need-texture").attr("texture", name);
}

$(document).ready( function () {
	$(document).on ("click", ".load-texture",function() {
		makeTextureSelected( $(this).attr("name") );
		loadMaterial( $(this).attr("name") );
	});

	$(document).on ("click", ".toggle-rotation",function() {
		rotate = !rotate;
		if( !rotate ){
			$(".toggle-rotation").removeClass("fa-hand");
			$(".toggle-rotation").addClass("fa-rotate");
		}else{
			$(".toggle-rotation").addClass("fa-hand");
			$(".toggle-rotation").removeClass("fa-rotate");
		}
	});

	$(document).on ("input",".update_material", function() {
		updateThreeMaterial();
	});

});


function updateList() {

	$.get( "/callback/textures_list", function( data ) {
		var list = data.split(",");
		$(".textures-list").html("");

		for (var i = 0; i < list.length; i++) {
	  		$(".textures-list").append(
	  			`<button class="col-4 load-texture" name="`+list[i].split(".")[0]+`">
	  				<img src="/processing/diffuse/`+list[i]+`" >
	  				<p>` + list[i].split(".")[0] + `</p>
	  			</button>`
	  		);
		}

		if( list.length-1 < 1 ){
			$.get( "/notextures.html", function( data ) {
		  		$(".textures-list").append(data);
			});
		}
	});

}

var interestingSentences = [
	"This may take some time",
	"Wait till the end",
	"It's almost done",
	"Something happening"
];

function changeWordsLoading( element ) {
	setTimeout(function() {
		if( !$(element).is(":disabled") )
			return;
		if( !$(element).html().includes("spinner-border-sm") )
			return;

		const random = Math.floor(Math.random() * interestingSentences.length);

		element.html( `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>   ` + interestingSentences[random] + `...` );
		changeWordsLoading( element )
	},5000);
}

$(document).ready( function () {
	$(document).on ("click", "button",function() {
		var callback = $(this).attr("callback");
		if( callback && !$(this).attr("prev-html") ){
			$(this).prop('disabled', true);
			if( !$(this).attr("prev-html") )
				$(this).attr("prev-html", $(this).html());

			var newText = $(this).html();
			newText = newText.replaceAll("Load", "Loading").replaceAll("Write", "Writing").replaceAll("Process", "Processing");

			$(this).html( `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ` + newText + "..." );
			var parent = $(this);

			changeWordsLoading(parent)
			
			var args = [];
			//if( parent.hasClass("need-texture") )
			//	args.push( "texture=" + parent.attr("texture-name") )
			var blackList = ["disabled", "class", "callback", "prev-html", "role", "value", "id", "aria-labelledby", "style", "src", "href"];
			$.each(this.attributes, function() {
				if(this.specified && !blackList.includes(this.name) ) {
					args.push( this.name + "=" + this.value )
				}
			});

			if(  args.length > 0 )
				args = "?" + args.join('&')
			else
				args = ""

			$.get("/callback/" + callback + args, function( data ) {
				parent.html( data );
				parent.prop('disabled', true);
				updateList();

				if( parent.hasClass("need-texture") ){
					setTimeout(function() {
						makeTextureSelected( parent.attr("texture") );
						loadMaterial( parent.attr("texture") );
					},100);

				}

				setTimeout(function() {
					parent.prop('disabled', false);
					parent.html( parent.attr("prev-html") );
					parent.attr("prev-html", "")
				},3000);
			});
		}
	});

	setTimeout(function() {
	$("input").map(function() {
		var index = $( "input" ).index( this );
		var value = localStorage.getItem('input-' + index);
		//console.log(value);

		if ( value !== null )
			$(this).val(value);
	});
	},1500);


	$(document).on("keyup", "input",function() {
		//console.log();
		var value = $(this).val();
		var index = $( "input" ).index( this );

		localStorage.setItem('input-' + index, value);
		//console.log("saved " + index + " " + value);
		//if (localStorage.getItem('input-' + index) !== null)
	});

});

updateList();