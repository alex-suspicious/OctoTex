
import * as THREE from 'three';

import Stats from 'three/addons/libs/stats.module.js';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { HDRCubeTextureLoader } from 'three/addons/loaders/HDRCubeTextureLoader.js';

import { FlakesTexture } from 'three/addons/textures/FlakesTexture.js';

let container, stats;

let camera, scene, renderer;

let particleLight;
let particleLight2;
let particleLight3;
let group;
let mesh;
let newMaterial;
let rotate = true;
let yaw_angle = 0;
let yaw_angle_lerp = 0;

const textureLoader = new THREE.TextureLoader();
THREE.Cache.enabled = false;

init();
animate();

function lerp (start, end, amt){
  return (1-amt)*start+amt*end
}
const clamp = (num, min, max) => Math.min(Math.max(num, min), max);

function updateThreeMaterial() {
	if( !newMaterial || !mesh )
		return;

	if( $("#material_type").val().replace("@","") == "glass" ){
		var trans = clamp( ($("#transparencyRange").val()/1200), 0 , 1 );

		newMaterial.ior = $("#ior_constant").val()/1000.0;
		newMaterial.reflectivity = 1.0 - $("#roughnessRange").val()/1000.0;
		newMaterial.transmission = $("#transparencyRange").val()/980.0;
		newMaterial.opacity = $("#transparencyRange").val()/980.0;
		newMaterial.thickness = $("#ior_constant").val()/1000.0;
		newMaterial.sheen = trans;
		newMaterial.transparent = false;
		newMaterial.map = null;
		newMaterial.color = new THREE.Color(trans,trans,trans);
	}
	else{
		newMaterial.transmission = 0;
		newMaterial.transparent = true;
		newMaterial.color = new THREE.Color(1,1,1);
	}

	newMaterial.roughness = $("#roughnessRange").val()/1000.0;
	newMaterial.displacementScale = $("#depthRange").val()/1000.0;
	newMaterial.metalness = $("#metallic_constant").val()/1000.0;

	mesh.material = newMaterial;
}

function loadMaterial( name ) {
	const diffuse = textureLoader.load( 'processing/diffuse/'+name+'.png' );

	
	$.get( "/callback/get_material?texture=" + name, function( data ) {
		var splitted = data.split("\n");
		$("#material_type").val(splitted[0].replace("@",""));
		$("#depthRange").val( parseFloat(splitted[1].split("=")[1].replace(" ",""))*1000 );
		$("#roughnessRange").val( parseFloat(splitted[3].split("=")[1].replace(" ",""))*1000 );
		$("#transparencyRange").val( parseFloat(splitted[2].split("=")[1].replace(" ",""))*1000 );
		$("#ior_constant").val( parseFloat(splitted[4].split("=")[1].replace(" ",""))*1000 );
		$("#metallic_constant").val( parseFloat(splitted[5].split("=")[1].replace(" ",""))*1000 );
		$("#emissive_intensity").val( parseFloat(splitted[6].split("=")[1].replace(" ",""))*1000 );

		updateThreeMaterial();
		setTimeout(function() {
			updateThreeMaterial();
		},300);

		console.log(splitted)
	});

	textureLoader.load(
	    'processing/normal/'+name+'_normal.png',
	    function ( texture ) {
			const roughnessMap = textureLoader.load( 'processing/roughness/'+name+'_rough.png' );
			const displacementsMap = textureLoader.load( 'processing/displacements/'+name+'_disp.png' );

			newMaterial = new THREE.MeshPhysicalMaterial( {
				metalness: 0.0,
				roughnessMap: roughnessMap,
				clearcoat: 0,
				displacementMap: displacementsMap,
				displacementScale: 0.18,
				transparent: true,
				normalMap: texture,
				bumpMap: displacementsMap,
				map: diffuse,
				side: THREE.DoubleSide
			} );
			mesh.material = newMaterial;
	    },
	    function ( xhr ) {},
	    function ( xhr ) {
			newMaterial = new THREE.MeshPhysicalMaterial( {
				metalness: 0.0,
				roughness: 1,
				transparent: true,
				clearcoat: 0,
				map: diffuse,
				side: THREE.DoubleSide
			} );
			mesh.material = newMaterial;

			return
	    }
	);

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

	$(document).on ("click",".mesh-change", function() {
		var meshname = $(this).attr("mesh");

		group.remove(mesh);
		mesh = null;
		var geometry = null;

		if( meshname == "plane" )
			geometry = new THREE.PlaneGeometry( 3, 3, 512, 512 );
		if( meshname == "cube" )
			geometry = new THREE.BoxGeometry( 3, 3, 3,512, 512, 512 );
		if( meshname == "sphere" )
			geometry = new THREE.SphereGeometry( 2, 512, 512 );

		mesh = new THREE.Mesh( geometry );
		mesh.position.x = 0;
		mesh.position.y = 0;
		mesh.position.z = 0;
		mesh.castShadow = true;
		group.add( mesh );
		setTimeout(function() {
			updateThreeMaterial();
		},300);
	});
});

function init() {

	container = document.createElement( 'div' );
	document.body.appendChild( container );

	camera = new THREE.PerspectiveCamera( 40, window.innerWidth / window.innerHeight, 0.25, 50 );
	camera.position.z = 30;

	scene = new THREE.Scene();

	group = new THREE.Group();
	scene.add( group );

	new HDRCubeTextureLoader()
		.setPath( 'textures/cube/pisaHDR/' )
		.load( [ 'px.hdr', 'nx.hdr', 'py.hdr', 'ny.hdr', 'pz.hdr', 'nz.hdr' ],
			function ( texture ) {

				const geometry = new THREE.PlaneGeometry( 3, 3, 512, 512 );
				mesh = new THREE.Mesh( geometry );
				mesh.position.x = 0;
				mesh.position.y = 0;
				mesh.position.z = 0;
				mesh.castShadow = true;
				group.add( mesh );

				//loadMaterial("BB0778A65A4FC27D");

				scene.background = texture;
				scene.environment = texture;
			}

		);

	// LIGHTS

	particleLight = new THREE.Mesh(
		new THREE.SphereGeometry( .05, 8, 8 ),
		new THREE.MeshBasicMaterial( { color: 0xffffff } )
	);
	scene.add( particleLight );
	var particleLightLight = new THREE.PointLight( 0xffffff, 150 );
	particleLightLight.castShadow = true; 
	particleLight.add( particleLightLight );

	particleLight2 = new THREE.Mesh(
		new THREE.SphereGeometry( .05, 8, 8 ),
		new THREE.MeshBasicMaterial( { color: 0xffffff } )
	);
	scene.add( particleLight2 );

	var particleLightLight2 = new THREE.PointLight( 0xffffff, 150 );
	particleLightLight2.castShadow = true; 
	particleLight2.add( particleLightLight2 );

	particleLight3 = new THREE.Mesh(
		new THREE.SphereGeometry( .05, 8, 8 ),
		new THREE.MeshBasicMaterial( { color: 0xffffff } )
	);
	scene.add( particleLight3 );

	var particleLightLight3 = new THREE.PointLight( 0xffffff, 150 );
	particleLightLight3.castShadow = true; 
	particleLight3.add( particleLightLight3 );


	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	container.appendChild( renderer.domElement );

	//

	renderer.toneMapping = THREE.ACESFilmicToneMapping;
	renderer.toneMappingExposure = 1.2;

	// EVENTS

	const controls = new OrbitControls( camera, renderer.domElement );
	controls.minDistance = 3;
	controls.maxDistance = 30;

	window.addEventListener( 'resize', onWindowResize );
	
}

//

function onWindowResize() {

	const width = window.innerWidth;
	const height = window.innerHeight;

	camera.aspect = width / height;
	camera.updateProjectionMatrix();

	renderer.setSize( width, height );

}

//

function animate() {

	requestAnimationFrame( animate );
	render();

}

function render() {

	const timer = Date.now() * 0.000025;

	particleLight.position.x = Math.sin( timer * 7 ) * 9;
	particleLight.position.y = Math.cos( timer * 5 ) * 13;
	particleLight.position.z = Math.cos( timer * 3 ) * -14;

	particleLight2.position.x = Math.sin( timer * 3 ) * 14;
	particleLight2.position.y = Math.cos( timer * 8 ) * 12;
	particleLight2.position.z = Math.cos( timer * 4 ) * 17;

	particleLight3.position.x = Math.sin( timer * 5 ) * 20;
	particleLight3.position.y = Math.cos( timer * 9 ) * -9;
	particleLight3.position.z = Math.cos( timer * 5 ) * 12;

	if( mesh ){
		//mesh.position.y = Math.sin( timer * 30 )*0.5;
		if( rotate )
			yaw_angle += 0.02;

		yaw_angle_lerp = lerp(yaw_angle,yaw_angle_lerp,0.95)
		mesh.rotation.y = yaw_angle_lerp;
	}

	renderer.render( scene, camera );

}

function updateList() {

	$.get( "/callback/textures_list", function( data ) {
		var list = data.split(",");
		$(".textures-list").html("");

		if( list.length-1 < 1 ){
			$.get( "/notextures.html", function( data ) {
		  		$(".textures-list").append(data);
			});
			return;
		}

		for (var i = 0; i < list.length; i++) {
	  		$(".textures-list").append(
	  			`<button class="col-4 load-texture" name="`+list[i].split(".")[0]+`">
	  				<img width="128" height="128" loading="lazy" src="/processing/thumbnail/`+list[i]+`" >
	  				<p>` + list[i].split(".")[0] + `</p>
	  			</button>`
	  		);
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
					},200);

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

//303C5BD3B6882DD9
var prevHash = "";

$(function() {

    $(window).focus(function() {
			$.get("/callback/get_clipboard",function( newHash ) {
				console.log(newHash);
				if( !newHash )
					return;

				if( prevHash == newHash )
					return;

				prevHash = newHash;
				makeTextureSelected( prevHash );
				loadMaterial( prevHash );
				
				setTimeout(function() {
					makeTextureSelected( parent.attr("texture") );
					loadMaterial( parent.attr("texture") );
				},200);
			});
    });

});
